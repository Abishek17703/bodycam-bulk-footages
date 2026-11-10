import os
import sys
import json
import urllib.request
import urllib.parse
import yt_dlp
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

scratch = r'C:\Users\abish\.gemini\antigravity\brain\882b3be2-cdc7-4132-8a3e-0334cc030687\scratch'
adc = json.load(open(os.path.expandvars(r'%APPDATA%\gcloud\legacy_credentials\abishek17703@gmail.com\adc.json')))
saved = json.load(open(os.path.join(scratch, 'tok_bodyacamfootages.json')))

def get_token():
    return json.loads(urllib.request.urlopen(urllib.request.Request(
        'https://oauth2.googleapis.com/token',
        data=urllib.parse.urlencode({
            'client_id': adc['client_id'],
            'client_secret': adc['client_secret'],
            'refresh_token': saved['refresh_token'],
            'grant_type': 'refresh_token'
        }).encode()
    )).read())['access_token']

tok = get_token()
parent_automation_id = "1jchXKZ3sNlCuK1MlEEPsQmPdynFN-X1Z"  # BODYCAM AUTOMATION

def create_or_get_folder(parent_id, name):
    esc_name = name.replace("'", "\\'")
    q = urllib.parse.quote(f"'{parent_id}' in parents and name = '{esc_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false")
    ex = json.loads(urllib.request.urlopen(urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files?q={q}&fields=files(id,name)",
        headers={'Authorization': f'Bearer {tok}'}
    )).read()).get("files", [])
    if ex:
        return ex[0]['id']
    req = urllib.request.Request(
        "https://www.googleapis.com/drive/v3/files?fields=id,name",
        data=json.dumps({
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id]
        }).encode("utf-8"),
        headers={'Authorization': f'Bearer {tok}', 'Content-Type': 'application/json'},
        method="POST"
    )
    fid = json.loads(urllib.request.urlopen(req).read())['id']
    try:
        urllib.request.urlopen(urllib.request.Request(
            f"https://www.googleapis.com/drive/v3/files/{fid}/permissions",
            data=json.dumps({"role": "reader", "type": "anyone"}).encode("utf-8"),
            headers={'Authorization': f'Bearer {tok}', 'Content-Type': 'application/json'},
            method="POST"
        ))
    except Exception:
        pass
    return fid

def list_files_in_folder(folder_id):
    q = urllib.parse.quote(f"'{folder_id}' in parents and trashed = false")
    return json.loads(urllib.request.urlopen(urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files?q={q}&fields=files(id,name,size,mimeType)",
        headers={'Authorization': f'Bearer {tok}'}
    )).read()).get("files", [])

def upload_local_mp4(folder_id, local_path, target_name):
    tok_now = get_token()
    existing = [f for f in list_files_in_folder(folder_id) if f['name'] == target_name and int(f.get('size', 0)) > 100000]
    if existing:
        print(f"  [Already in Drive] {target_name} ({existing[0].get('size')} bytes)")
        return existing[0]['id']

    fsize = os.path.getsize(local_path)
    init_req = urllib.request.Request(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable",
        data=json.dumps({"name": target_name, "parents": [folder_id]}).encode("utf-8"),
        headers={
            'Authorization': f'Bearer {tok_now}',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Upload-Content-Type': 'video/mp4',
            'X-Upload-Content-Length': str(fsize)
        },
        method="POST"
    )
    with urllib.request.urlopen(init_req) as resp:
        upload_url = resp.headers['Location']

    with open(local_path, 'rb') as f:
        data = f.read()
    put_req = urllib.request.Request(
        upload_url,
        data=data,
        headers={'Content-Length': str(fsize), 'Content-Type': 'video/mp4'},
        method="PUT"
    )
    res = json.loads(urllib.request.urlopen(put_req, timeout=300).read())
    print(f"  [Uploaded] {target_name} ({fsize // (1024*1024)} MB) -> {res.get('id')}")
    return res.get('id')

luke_root_id = create_or_get_folder(parent_automation_id, "Client - Luke B (10 Direct Raw Bodycam Cases)")
print("Luke B Root Folder:", luke_root_id)

cases = [
    ("01 - Row 07 - Pasadena PD CA - Ricardo Guade Andrade Fatal OIS (23m Raw)", "Pasadena PD, CA", "Row 7", ["eqwHXVraRsA"]),
    ("02 - Row 08 - Del Norte County Sheriff CA - Robert Anderson OIS (31m Official Raw)", "Del Norte County Sheriff, CA", "Row 8", ["K98M1K8MHHg", "yad2L_B-eiY"]),
    ("03 - Row 12 - Monroe County Sheriff FL - Darla Rachel Vidal Erratic Driving Arrest (53m Raw)", "Monroe County Sheriff, FL", "Row 12", ["JnD_zN-NfpI", "ZRvM7XMTY_k"]),
    ("04 - Row 13 - Norton Shores PD MI - Paul Ferguson & Timothy Ferguson Case (3h Raw BWC & Interrogation)", "Norton Shores PD, MI", "Row 13", ["8NREDFp9eWI", "nV0vDONtLJg"]),
    ("05 - Row 27 - Volusia Sheriff FL - Paddleboard Pursuit in River (18m Raw)", "Volusia Sheriff, FL", "Row 27", ["DVrcFFG37Kc"]),
    ("06 - Row 28 - Flagler County Sheriff FL - Fake Urine Whizzinator in Patrol Car (17m Raw)", "Flagler County Sheriff, FL", "Row 28", ["cp-OgukXjKc", "TjmSUOFwfFM"]),
    ("07 - Row 29 - Hillsborough County Sheriff FL - Fake Cop Pulls Over Undercover Deputy (9m Raw)", "Hillsborough County Sheriff, FL", "Row 29", ["ReL1WEm9bAg", "rzQJTFR4Du0"]),
    ("08 - Row 32 - Hillsborough County Sheriff FL - Canadian Woman With 12 Fake IDs (Raw)", "Hillsborough County Sheriff, FL", "Row 32", ["C6PwuT_an6w"]),
    ("09 - Row 37 - Florida Sheriff - Man Throws Bible at Deputies & Barricades in Bathroom (14m Raw)", "Florida Law Enforcement", "Row 37", ["iaUknq69d8A"]),
    ("10 - Row 38 - Volusia County Sheriff FL - Man Crashes Through Daytona Airport Gate (7m Raw)", "Volusia County Sheriff, FL", "Row 38", ["nc-m-mOusJs"]),
]

tmp_dl_dir = os.path.join(scratch, "luke_b_dl")
os.makedirs(tmp_dl_dir, exist_ok=True)

import imageio_ffmpeg
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

manifest_rows = [["Case #", "Luke B Sheet Row", "Case Folder Name", "Agency", "Videos Uploaded", "Drive Folder Link"]]

for idx, (folder_name, agency, sheet_row, vids) in enumerate(cases, 1):
    sub_id = create_or_get_folder(luke_root_id, folder_name)
    print(f"\n[{idx}/10] {folder_name} -> {sub_id}")
    uploaded_count = 0
    for vid in vids:
        target_mp4 = f"{sheet_row.replace(' ', '')}_{vid}.mp4"
        existing = [f for f in list_files_in_folder(sub_id) if f['name'] == target_mp4 and int(f.get('size', 0)) > 100000]
        if existing:
            print(f"  Already present: {target_mp4}")
            uploaded_count += 1
            continue
        local_mp4 = os.path.join(tmp_dl_dir, target_mp4)
        if not os.path.exists(local_mp4) or os.path.getsize(local_mp4) < 100000:
            ydl_opts = {
                'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
                'outtmpl': local_mp4,
                'merge_output_format': 'mp4',
                'ffmpeg_location': ffmpeg_exe,
                'quiet': True,
                'no_warnings': True,
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([f"https://www.youtube.com/watch?v={vid}"])
            except Exception as e:
                print(f"  Download err for {vid}: {e}")
                continue
        if os.path.exists(local_mp4) and os.path.getsize(local_mp4) > 100000:
            upload_local_mp4(sub_id, local_mp4, target_mp4)
            uploaded_count += 1
            try:
                os.remove(local_mp4)
            except Exception:
                pass
    manifest_rows.append([
        f"Case {idx:02d}",
        sheet_row,
        folder_name,
        agency,
        str(uploaded_count),
        f"https://drive.google.com/drive/folders/{sub_id}"
    ])

# Create Google Sheet Manifest inside Luke B Root Folder
tok_now = get_token()
sheet_title = "Luke B - 10 Direct Raw Bodycam Cases Manifest"
esc_st = sheet_title.replace("'", "\\'")
q_sh = urllib.parse.quote(f"'{luke_root_id}' in parents and name = '{esc_st}' and mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false")
ex_sh = json.loads(urllib.request.urlopen(urllib.request.Request(
    f"https://www.googleapis.com/drive/v3/files?q={q_sh}&fields=files(id,name)",
    headers={'Authorization': f'Bearer {tok_now}'}
)).read()).get("files", [])

if ex_sh:
    sheet_id = ex_sh[0]['id']
else:
    req = urllib.request.Request(
        "https://www.googleapis.com/drive/v3/files?fields=id",
        data=json.dumps({
            "name": sheet_title,
            "mimeType": "application/vnd.google-apps.spreadsheet",
            "parents": [luke_root_id]
        }).encode("utf-8"),
        headers={'Authorization': f'Bearer {tok_now}', 'Content-Type': 'application/json'},
        method="POST"
    )
    sheet_id = json.loads(urllib.request.urlopen(req).read())['id']
    try:
        urllib.request.urlopen(urllib.request.Request(
            f"https://www.googleapis.com/drive/v3/files/{sheet_id}/permissions",
            data=json.dumps({"role": "reader", "type": "anyone"}).encode("utf-8"),
            headers={'Authorization': f'Bearer {tok_now}', 'Content-Type': 'application/json'},
            method="POST"
        ))
    except Exception:
        pass

val_req = urllib.request.Request(
    f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/A1?valueInputOption=USER_ENTERED",
    data=json.dumps({"values": manifest_rows}).encode("utf-8"),
    headers={'Authorization': f'Bearer {tok_now}', 'Content-Type': 'application/json'},
    method="PUT"
)
urllib.request.urlopen(val_req)
print("\n=== LUKE B PACKAGE COMPLETE ===")
print("Drive Folder:", f"https://drive.google.com/drive/folders/{luke_root_id}")
print("Manifest Sheet:", f"https://docs.google.com/spreadsheets/d/{sheet_id}")
