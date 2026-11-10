import os, sys, json, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

adc = json.load(open(os.path.expandvars(r'%APPDATA%\gcloud\legacy_credentials\abishek17703@gmail.com\adc.json')))
scratch = os.path.dirname(__file__)

saved = json.load(open(os.path.join(scratch, "tok_bodyacamfootages.json")))
tok = json.loads(urllib.request.urlopen(urllib.request.Request(
    'https://oauth2.googleapis.com/token',
    data=urllib.parse.urlencode({
        'client_id': adc['client_id'],
        'client_secret': adc['client_secret'],
        'refresh_token': saved['refresh_token'],
        'grant_type': 'refresh_token'
    }).encode()
)).read())['access_token']

def gdrive_query(q, fields="files(id,name,mimeType,size,videoMediaMetadata,shortcutDetails)"):
    items = []
    page_token = None
    while True:
        url = f"https://www.googleapis.com/drive/v3/files?q={urllib.parse.quote(q)}&pageSize=100&fields=nextPageToken,{fields}"
        if page_token:
            url += f"&pageToken={urllib.parse.quote(page_token)}"
        res = json.loads(urllib.request.urlopen(urllib.request.Request(
            url, headers={'Authorization': f'Bearer {tok}'}
        )).read())
        items.extend(res.get("files", []))
        page_token = res.get("nextPageToken")
        if not page_token:
            break
    return items

def count_videos_recursive(folder_id):
    vids = []
    ch = gdrive_query(f"'{folder_id}' in parents and trashed = false")
    for c in ch:
        mt = c.get('mimeType', '')
        if mt == 'application/vnd.google-apps.folder':
            sub = gdrive_query(f"'{c['id']}' in parents and trashed = false")
            for s in sub:
                smt = s.get('mimeType', '')
                if ('video' in smt or s['name'].lower().endswith('.mp4')) and int(s.get('size', 0)) > 100000:
                    vids.append(s)
        elif ('video' in mt or c['name'].lower().endswith('.mp4')) and int(c.get('size', 0)) > 100000:
            vids.append(c)
    total_bytes = sum(int(v.get('size', 0)) for v in vids)
    total_ms = sum(int(v.get('videoMediaMetadata', {}).get('durationMillis', 0)) for v in vids)
    hr = round(total_ms / 3600000.0, 2) if total_ms > 0 else round((total_bytes / (1024**3)) / 0.75, 2)
    return len(vids), round(total_bytes / (1024**3), 2), hr, [v['name'] for v in vids[:3]]

# 1. Verify AAFILAS sheet (109KNTvx_BOGpQAo3KodG-eMMRICWQCZNg60xnzbWJ8A)
aafilas_vals = json.loads(urllib.request.urlopen(urllib.request.Request(
    "https://sheets.googleapis.com/v4/spreadsheets/109KNTvx_BOGpQAo3KodG-eMMRICWQCZNg60xnzbWJ8A/values/A2:E55",
    headers={'Authorization': f'Bearer {tok}'}
)).read()).get("values", [])

print(f"=== 1. VERIFYING AAFILAS ({len(aafilas_vals)} rows) ===")
aafilas_ok = 0
for r in aafilas_vals:
    cid = r[1]
    fid = r[3].split("/")[-1]
    vcnt, gb, hr, sample = count_videos_recursive(fid)
    status = "OK" if vcnt > 0 and gb > 0 else "EMPTY/FAIL"
    if status == "OK":
        aafilas_ok += 1
    else:
        print(f"  [FAIL] {cid} | {r[2]} | vids={vcnt} | gb={gb}")
print(f"AAFILAS VERIFIED: {aafilas_ok} / {len(aafilas_vals)} HAVE ACTUAL MP4 VIDEOS > 0 BYTES")

# 2. Verify JIMMY sheet (1xMUFpZCSO1CcohKegnIvwdkoUW3TbgiXNjZzUnEhN7M)
jimmy_vals = json.loads(urllib.request.urlopen(urllib.request.Request(
    "https://sheets.googleapis.com/v4/spreadsheets/1xMUFpZCSO1CcohKegnIvwdkoUW3TbgiXNjZzUnEhN7M/values/A2:H20",
    headers={'Authorization': f'Bearer {tok}'}
)).read()).get("values", [])

print(f"\n=== 2. VERIFYING JIMMY ({len(jimmy_vals)} rows) ===")
jimmy_ok = 0
for r in jimmy_vals:
    cid = r[0]
    fid = r[6].split("/")[-1]
    vcnt, gb, hr, sample = count_videos_recursive(fid)
    status = "OK" if vcnt > 0 and gb > 0 else "EMPTY/FAIL"
    if status == "OK":
        jimmy_ok += 1
    print(f"  [{status}] {cid} | {r[1][:40]} | vids={vcnt} | {gb} GB | {hr}h | sample={sample[:2]}")
print(f"JIMMY VERIFIED: {jimmy_ok} / {len(jimmy_vals)} HAVE ACTUAL MP4 VIDEOS > 0 BYTES")

# 3. Verify RISENORTH sheet (1jC640lnQLpra4Syx_iNm3tZtSk3sbYYJTpK9_6tHLrY)
risenorth_vals = json.loads(urllib.request.urlopen(urllib.request.Request(
    "https://sheets.googleapis.com/v4/spreadsheets/1jC640lnQLpra4Syx_iNm3tZtSk3sbYYJTpK9_6tHLrY/values/A2:I20",
    headers={'Authorization': f'Bearer {tok}'}
)).read()).get("values", [])

print(f"\n=== 3. VERIFYING RISENORTH ({len(risenorth_vals)} rows) ===")
risenorth_ok = 0
for r in risenorth_vals:
    cid = r[0]
    fid = r[7].split("/")[-1]
    vcnt, gb, hr, sample = count_videos_recursive(fid)
    status = "OK" if vcnt > 0 and gb > 0 else "EMPTY/FAIL"
    if status == "OK":
        risenorth_ok += 1
    print(f"  [{status}] {cid} [{r[1]}] | {r[2][:40]} | vids={vcnt} | {gb} GB | {hr}h | sample={sample[:2]}")
print(f"RISENORTH VERIFIED: {risenorth_ok} / {len(risenorth_vals)} HAVE ACTUAL MP4 VIDEOS > 0 BYTES")
