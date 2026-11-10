import sys
import os
import csv
import io
import re
import json
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')


def read_sheet_csv(sheet_id):
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        text = resp.read().decode('utf-8', errors='replace')
    return list(csv.reader(io.StringIO(text)))


def cmd_sheet_csv(sheet_id):
    rows = read_sheet_csv(sheet_id)
    for i, r in enumerate(rows, 1):
        if any(r):
            compact = [c[:80].replace('\n', ' ') for c in r[:6]]
            print(f'R{i:02d}: {compact}')


def _scan_url(idx, row):
    if len(row) < 3:
        return idx, '', []
    title = row[0][:50]
    raw_url = row[2].split('?utm_source')[0].strip()
    if not raw_url.startswith('http'):
        return idx, title, []
    hits = []
    if 'youtube.com' in raw_url or 'youtu.be' in raw_url:
        hits.append(f'DIRECT_YT:{raw_url}')
    if 'wikimedia.org' in raw_url:
        hits.append(f'WIKIMEDIA:{raw_url}')
    try:
        req = urllib.request.Request(raw_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        for yid in set(re.findall(r'(?:youtube\.com/embed/|watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})', html)):
            hits.append(f'YT:{yid}')
        for mp4 in list(set(re.findall(r'https://[^\s"\'<>]+?\.mp4', html)))[:2]:
            hits.append(f'MP4:{mp4}')
    except Exception as e:
        hits.append(f'ERR:{type(e).__name__}')
    return idx, title, hits


def cmd_audit_sheet_videos(sheet_id):
    rows = read_sheet_csv(sheet_id)
    results = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = [ex.submit(_scan_url, i + 1, rows[i]) for i in range(1, len(rows)) if any(rows[i])]
        for f in as_completed(futs):
            results.append(f.result())
    for idx, title, hits in sorted(results):
        if hits:
            print(f'R{idx:02d} | {title} -> {", ".join(hits)}')


def cmd_yt_check(query_or_id):
    import yt_dlp
    target = query_or_id if query_or_id.startswith(('http', 'ytsearch')) else f'https://www.youtube.com/watch?v={query_or_id}'
    with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
        try:
            info = ydl.extract_info(target, download=False)
            entries = info.get('entries', [info])
            for e in entries[:5]:
                print(f"[{e.get('id')}] {e.get('title')} | {e.get('uploader') or e.get('channel')} | {e.get('duration')}s")
        except Exception:
            u = f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={query_or_id}&format=json'
            with urllib.request.urlopen(u, timeout=8) as r:
                d = json.loads(r.read().decode())
                print(f"[{query_or_id}] {d.get('title')} | {d.get('author_name')}")


def cmd_video_grid(mp4_path, out_jpg):
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        ffmpeg_exe = 'ffmpeg'
    subprocess.run([
        ffmpeg_exe, '-y', '-i', mp4_path,
        '-vf', 'fps=1/4,scale=360:-1,tile=4x3',
        '-frames:v', '1', out_jpg
    ], capture_output=True, check=True)
    print(f'Grid saved: {out_jpg} ({os.path.getsize(out_jpg)} bytes)')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: low_token_ops.py <sheet-csv|audit-sheet-videos|yt-check|video-grid> <arg1> [arg2]')
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == 'sheet-csv':
        cmd_sheet_csv(sys.argv[2])
    elif cmd == 'audit-sheet-videos':
        cmd_audit_sheet_videos(sys.argv[2])
    elif cmd == 'yt-check':
        cmd_yt_check(sys.argv[2])
    elif cmd == 'video-grid':
        cmd_video_grid(sys.argv[2], sys.argv[3])
