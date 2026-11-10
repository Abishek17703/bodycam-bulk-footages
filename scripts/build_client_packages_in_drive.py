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

parent_automation_id = "1jchXKZ3sNlCuK1MlEEPsQmPdynFN-X1Z" # BODYCAM AUTOMATION

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
        )).read()
    except:
        pass
    return fid

def create_or_get_sheet(parent_id, name):
    esc_name = name.replace("'", "\\'")
    q = urllib.parse.quote(f"'{parent_id}' in parents and name = '{esc_name}' and mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false")
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
            "mimeType": "application/vnd.google-apps.spreadsheet",
            "parents": [parent_id]
        }).encode("utf-8"),
        headers={'Authorization': f'Bearer {tok}', 'Content-Type': 'application/json'},
        method="POST"
    )
    sid = json.loads(urllib.request.urlopen(req).read())['id']
    try:
        urllib.request.urlopen(urllib.request.Request(
            f"https://www.googleapis.com/drive/v3/files/{sid}/permissions",
            data=json.dumps({"role": "reader", "type": "anyone"}).encode("utf-8"),
            headers={'Authorization': f'Bearer {tok}', 'Content-Type': 'application/json'},
            method="POST"
        )).read()
    except:
        pass
    return sid

def create_shortcut(parent_id, name, target_id):
    esc_name = name.replace("'", "\\'")
    q = urllib.parse.quote(f"'{parent_id}' in parents and name = '{esc_name}' and trashed = false")
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
            "mimeType": "application/vnd.google-apps.shortcut",
            "parents": [parent_id],
            "shortcutDetails": {"targetId": target_id}
        }).encode("utf-8"),
        headers={'Authorization': f'Bearer {tok}', 'Content-Type': 'application/json'},
        method="POST"
    )
    return json.loads(urllib.request.urlopen(req).read())['id']

# ==============================================================================
# 1. CLIENT: JIMMY (America's Most Evil - 10h+ Homicide, Shootings & Standoffs)
# ==============================================================================
jimmy_folder_id = create_or_get_folder(parent_automation_id, "Client - Jimmy (America's Most Evil - 10h+ Homicide & Shooting Packages)")
jimmy_sheet_id = create_or_get_sheet(jimmy_folder_id, "Client - Jimmy - America's Most Evil Complete Packages Manifest")

jimmy_cases = [
    ("JIMMY_01", "South Columbus Mass Shooting Suspects (Louis Gordon-Hay et al.)", "Multiple Homicide / Mass Shooting & Tactical Perimeter Pack (77 Camera Angles + Tactical Perimeter Pack)", "Columbus Division of Police / Multi-Agency, OH", "35.14h (62.97 GB)", "77 Raw BWC/Dashcam MP4s + Official Docs", "1DkU3pclVjYLZ8t02eY1unNCr7vEFhYSD", "No, never posted (Raw Multi-Camera FOIA Pack)"),
    ("JIMMY_02", "Mackenzie Shirilla (Case #22-086777)", "Double Vehicular Homicide (100 MPH Intentional Crash Killing Dominic Russo & Davion Flanagan) — Full 57-Clip Arrest, Hospital & Investigation Package", "Strongsville Police Department, OH", "25.06h (19.67 GB)", "57 Raw BWC/Interview MP4s + Case Binder", "1WBEBMiUYR-J6_Pfkkkg8Uszj8FVIg0-T", "Raw 57-Clip Complete Agency Master Pack"),
    ("JIMMY_03", "Jared James Dicus (Anggy Diaz Decapitation Homicide)", "Brutal Newlywed Cabin Decapitation Murder — Complete 18-Camera On-Scene Arrest, Confession, Store Surveillance & Booking Feed", "Waller County Sheriff's Office, TX", "18.89h (23.34 GB)", "18 Raw BWC/CCTV/Booking MP4s + Case Summary", "1qy1maSTT3giXoyrL1_Dcv1dipxyz_zWy", "No, full 18-clip raw package never posted"),
    ("JIMMY_04", "Suspect #2021-0001845 (Armed Tactical Standoff & Shootout)", "Major Armed Confrontation, Hostage/Barricade & Multi-Officer Tactical Takedown", "Chicago Police Department / COPA #2021-0001845, IL", "15.77h (15.09 GB)", "34 Raw BWC/In-Car MP4s + Tactical Reports", "1ECrxKwzFsHXbsxEC3JXkRgP0wLDcouFt", "No, never posted on YouTube"),
    ("JIMMY_05", "Benjamin Paul Schneider & Bryan Mansell (Case #26AF02066)", "Multi-Day Tactical Search Warrant Raid & Standoff (33 Camera Angles Across Days 1–3)", "American Fork Police Department, UT", "13.51h (24.41 GB)", "33 Raw BWC MP4s + Warrant Dossier", "1253ex94NSdL-lJxmDQbVsnL_BuCvj-j1", "No, never posted on YouTube (2026 FOIA Release)"),
    ("JIMMY_06", "Chicago COPA #2022-0001369 (4200 W. Ford City Dr Critical Incident)", "Major Critical Incident & Multi-Unit Armed Police Response", "Chicago Police Department / COPA #2022-0001369, IL", "12.63h (13.70 GB)", "6 Extended Multi-Hour Raw BWC MP4s + Docs", "13mZp6rWzV_m_W_qG2mX2v2q_B_W_P_11", "No, never posted on YouTube"),
    ("JIMMY_07", "Sydney Powell (Mother Brenda Powell Stabbing Homicide)", "College Student Murders Mother With Cast-Iron Skillet & Steak Knife — 53-Clip On-Scene & Investigation Package", "Akron Police Department, OH", "10.65h (18.60 GB)", "53 Raw BWC/Cruiser MP4s + Case Summary", "1OzPVM66S2ujqWN9XPp-wYdgDbDmthqeT", "Complete 53-Clip Raw Agency Pack"),
    ("JIMMY_08", "Long Beach PD FOIA #26-02000 (Critical Incident & K9 Tactical Track)", "Armed Felony Suspect Perimeter Containment, SWAT/K9 Track & Takedown", "Long Beach Police Department, CA", "10.34h (7.76 GB)", "13 Raw BWC/Helicopter/K9 MP4s + Docs", "1pNfFHBjHG-0oL-bgKStE9yLl6_ANAWpR", "No, never posted on YouTube (2026 NextRequest)"),
    ("JIMMY_09", "Dennis Scott (Vehicular Homicide & Fatal Crash Investigation)", "Fatal Vehicular Homicide Investigation — 53-Clip Multi-Officer Scene, Witness & Custody Package", "Jones County / Multi-Agency", "9.78h (18.59 GB)", "53 Raw BWC/In-Car MP4s + Docs", "1jQbhpSMB9DddpS9GoBeKkKU0iiTRfdro", "No, never posted on YouTube"),
    ("JIMMY_10", "Jermelle English Jr. & Shanya Boyd (COPA #2023-0002357)", "Officer-Involved Shooting & High-Risk Felony Takedown (19 Camera Angles)", "Chicago Police Department / COPA #2023-0002357, IL", "8.46h (17.32 GB)", "19 Raw BWC MP4s + COPA Docs", "1T0rfJxFnGLbLQgI5-NlVi7AxK8vHGAwc", "No, never posted on YouTube"),
    ("JIMMY_11", "Jalonie Jenkins (Double Sister Homicide Investigation)", "19-Year-Old Murders Both Sisters in Streamwood — Full 8-Hour Interrogation, Scene & Custody Package", "Streamwood Police Department, IL", "7.97h (11.70 GB)", "8 Extended Raw BWC & Interrogation MP4s", "1j9954E_jV-2Qy3VO9AWllwg6mh1XSwmI", "No, never posted on YouTube"),
    ("JIMMY_12", "Officers Curtis & Willis — 300 S. Cicero Fatal Shootout (COPA #2024-0005309)", "Deadly Exchange of Gunfire & 58-Camera Tactical Response Package", "Chicago Police Department / COPA #2024-0005309, IL", "7.27h (13.38 GB)", "58 Raw BWC/In-Car MP4s + Docs", "1XZfcLqAuh1gqJXot7dlLFM4gEubpaDoz", "No, never posted on YouTube"),
    ("JIMMY_13", "Lake Mary Apartment Murder Suspects (Takedown & Interview Pack)", "Apartment Homicide Investigation, High-Risk Felony Takedown & Detective Interrogations (29 Clips)", "Lake Mary Police Department / Seminole County, FL", "6.44h (12.43 GB)", "29 Raw BWC & Interrogation MP4s + Docs", "1UmVDtMVaaUjBEtCUabbHXM9zq2V8CE0u", "No, never posted on YouTube"),
    ("JIMMY_14", "Brenan Robert Hill (Savannah Gonzalez Homicide Case)", "Brutal Murder of Savannah Gonzalez — 17-Clip Crime Scene, Search & Suspect Custody Package", "Florida Law Enforcement FOIA Release", "5.44h (8.99 GB)", "17 Raw BWC/Interview MP4s + Case Summary", "1LArmU4oWocQDBbJei9fDZYRSL1caT6Ge", "No, never posted on YouTube")
]

# Fix JIMMY_06 folder ID from our earlier BW_PORTAL_11 audit
bw_audit = json.load(open(os.path.join(scratch, "aafilas_bw_audit.json")))
for b in bw_audit:
    if "BW_PORTAL_11" in b['name']:
        jimmy_cases[5] = (jimmy_cases[5][0], jimmy_cases[5][1], jimmy_cases[5][2], jimmy_cases[5][3], jimmy_cases[5][4], jimmy_cases[5][5], b['id'], jimmy_cases[5][7])

jimmy_rows = [["Case ID", "Suspect / Case Name", "Homicide / Shooting / Standoff Storyline", "Agency & State", "Total Runtime & Size", "Package Contents", "Google Drive Folder Link", "YouTube Exclusivity"]]
for jc in jimmy_cases:
    create_shortcut(jimmy_folder_id, f"{jc[0]} - {jc[1]} ({jc[4].split(' ')[0]})", jc[6])
    jimmy_rows.append([jc[0], jc[1], jc[2], jc[3], jc[4], jc[5], f"https://drive.google.com/drive/folders/{jc[6]}", jc[7]])

urllib.request.urlopen(urllib.request.Request(
    f"https://sheets.googleapis.com/v4/spreadsheets/{jimmy_sheet_id}/values/A1:H{len(jimmy_rows)}?valueInputOption=USER_ENTERED",
    data=json.dumps({"values": jimmy_rows}).encode("utf-8"),
    headers={'Authorization': f'Bearer {tok}', 'Content-Type': 'application/json'},
    method="PUT"
)).read()
print("Created Jimmy folder:", jimmy_folder_id, "| Sheet:", jimmy_sheet_id)

# ==============================================================================
# 2. CLIENT: RISENORTH (12 Complete Cases: Fraud Crimes & Airport Crimes)
# ==============================================================================
risenorth_folder_id = create_or_get_folder(parent_automation_id, "Client - Risenorth (12 Fraud & Airport Cases)")
risenorth_sheet_id = create_or_get_sheet(risenorth_folder_id, "Client - Risenorth - 12 Fraud & Airport Cases Manifest")

risenorth_cases = [
    ("RISENORTH_01", "Fraud Crime", "Marc Anthony Taylor ($1,000,000 Fraudulent Check at Bank)", "Miami Man Attempts to Deposit $1M Fraudulent Check at Martin County Bank — Full 21-Clip Multi-Officer Arrest & Cruiser Package", "Stuart Police Department / Martin County, FL", "5h 07m (9.53 GB)", "21 Raw BWC & Cruiser MP4s", "14u12PrutCW9mxXGYjH6oBYQCjRaulAiH", "No, never posted on YouTube"),
    ("RISENORTH_02", "Fraud Crime", "Jermel Jones (Chuck E. Cheese Mascot Credit Card Fraud Arrest)", "Employee in Chuck E. Cheese Costume Handcuffed Mid-Shift for Stolen Credit Card Fraud — Full 3h+ Raw BWC Package", "Tallahassee Police Department, FL", "3h 07m (3.85 GB)", "Multi-Clip Raw BWC MP4s", "1dXwVTyrov1o1K3SVoUb_8pInr-USkYO5", "Unedited Raw Agency Package"),
    ("RISENORTH_03", "Fraud Crime", "Juan Daniel Ortiz (Felony Check Forgery & Uttering Arrest)", "Suspect Caught in Felony Forgery & Fraud Investigation — 2 Unedited Axon Extraction Streams", "Florida Municipal Police Department (FOIA)", "1h 45m (2.07 GB)", "2 Raw BWC MP4s ((Extraction_2.1)_FORGERY.mp4)", "15qsMi8CJT7r-kti7VV2aXwil3ilY3RN0", "No, never posted on YouTube"),
    ("RISENORTH_04", "Fraud Crime", "Autumn Marie Bardisa (Fake Registered Nurse / Insider Healthcare Fraud)", "Woman Treated 4,486 Hospital Patients Using Stolen Nurse License & Identity — 4-Clip Arrest Package", "Flagler County Sheriff's Office, FL", "0h 42m (0.38 GB)", "4 Raw BWC MP4s (1.mp4 - 4.mp4)", "1uA1Zi_SnrrlRJmsDgd52RmrzTGQhWDUt", "Unedited Raw Agency BWC"),
    ("RISENORTH_05", "Fraud Crime", "Thalia Jacqueline James (Chase Bank Text Scam & Fraud Investigation)", "Suspect Investigated for Chase Bank Fraud Text Scam — Redacted BWC + 2 Audio Interviews + Evidence Exhibit", "Police Department FOIA Release", "0h 35m (0.18 GB)", "1 BWC MP4 + 2 Axon Audio Files + Chase Fraud Exhibit JPG", "16qBD8lqzzEiNRRJshXwNi25yLzk6qrlR", "No, never posted on YouTube"),
    ("RISENORTH_06", "Fraud Crime", "Cornelius Edwards (Felony Fraud & Counterfeit Document Evidence)", "Suspect Arrested on Axon Body 4 (D01A0458J) With 14 High-Res Evidence Photos of Fraudulent Exhibits", "Police Department FOIA Release (2025-11-08)", "0h 30m (0.45 GB)", "1 Raw Axon Body 4 MP4 + 14 Evidence Photos", "1seoO3WEm1eCA-XDGXbaCdZv_FNhagqKU", "No, never posted on YouTube"),
    ("RISENORTH_07", "Fraud Crime", "Zeudy Gallardo Garcia & Yasiel Pena Paneque ($8,300 Bank of America Fake Check)", "Suspects Arrested Inside Boynton Beach Bank of America Attempting to Cash $8,300 Forged Check", "Palm Beach County Sheriff's Office / Boynton Beach, FL", "0h 46m (2.55 GB)", "1 Raw 1080p BWC MP4 + Case Summary", "18iLP2ljOH2S-z9Lc6YneEuYWzIzl0tX3", "2026 Raw BWC Release"),
    ("RISENORTH_08", "Fraud Crime", "Bank Teller Desk Fraudulent Check Scam Arrest (BW_2026_40)", "Police Officer Surprises Suspect Mid-Transaction at Bank Desk During Forged Check Scam", "Municipal Police Department FOIA Release", "0h 33m (0.65 GB)", "1 Raw BWC MP4 + Case Summary", "1x63u9mIDfG3pfe8HtrdH7KsvshfHp1JB", "2026 Raw BWC Release"),
    ("RISENORTH_09", "Fraud Crime", "Bank Fake ID Mother & Family Chaos Arrest (BW_2026_42)", "Woman Caught Using Forged ID at Bank With Her Son — Full Arrest & Scene Escalation", "Municipal Police Department FOIA Release", "0h 30m (0.39 GB)", "1 Raw BWC MP4 + Case Summary", "1nbClKwabLWpSpICUp3-z6e7St0qBzv7i", "2026 Raw BWC Release"),
    ("RISENORTH_10", "Fraud Crime", "Auto Dealership Doctor Identity Theft Suspect (BW_2026_45)", "Woman Steals Doctor's Identity to Buy Vehicles at Dealership, Then Calls Police to Report Them", "Municipal Police Department FOIA Release", "0h 26m (0.27 GB)", "1 Raw BWC MP4 + Case Summary", "1cUlMHOl1SwyX18DnIffjYZDYvQFvhrH8", "2026 Raw BWC Release"),
    ("RISENORTH_11", "Airport Crime", "Florida Airport Red Skirt Passenger Meltdown & Arrest (4-Camera Package)", "Unruly Passenger Arrested at Florida International Airport — 4 Unedited Officer BWC Clips", "Florida Airport Police / Sheriff's Office", "1h 15m (1.59 GB)", "4 Raw BWC MP4s (1.mp4 - 4.mp4)", "1LKr67oC1daxLnFrhbCMBgrDInRE9Wx7a", "No, raw 4-clip FOIA pack"),
    ("RISENORTH_12", "Airport Crime", "United Flight 1395 Passenger Gate Dispute & Airport Arrest (CASE_2026_18)", "Disruptive Passenger Arrested at Airport Gate Following Flight Delay Meltdown", "Palm Beach / Airport Police Department", "0h 32m (0.25 GB)", "1 Raw BWC MP4 + Case Summary", "1O1K7Bo3TtTz2WtTtWeEZUgZx5Lz9dPV3", "2026 Raw BWC Release")
]

risenorth_rows = [["Case ID", "Category (Fraud / Airport)", "Suspect / Case Title", "Incident Summary", "Agency & State", "Runtime & Size", "Files Included", "Google Drive Folder Link", "Notes"]]
for rc in risenorth_cases:
    create_shortcut(risenorth_folder_id, f"{rc[0]} [{rc[1]}] - {rc[2]}", rc[7])
    risenorth_rows.append([rc[0], rc[1], rc[2], rc[3], rc[4], rc[5], rc[6], f"https://drive.google.com/drive/folders/{rc[7]}", rc[8]])

urllib.request.urlopen(urllib.request.Request(
    f"https://sheets.googleapis.com/v4/spreadsheets/{risenorth_sheet_id}/values/A1:I{len(risenorth_rows)}?valueInputOption=USER_ENTERED",
    data=json.dumps({"values": risenorth_rows}).encode("utf-8"),
    headers={'Authorization': f'Bearer {tok}', 'Content-Type': 'application/json'},
    method="PUT"
)).read()
print("Created Risenorth folder:", risenorth_folder_id, "| Sheet:", risenorth_sheet_id)

# ==============================================================================
# 3. CLIENT: AAFILAS (Black Women Cases 2026 - Top 30 Best + 20 Backups = 50 Cases)
# ==============================================================================
aafilas_folder_id = create_or_get_folder(parent_automation_id, "Client - Aafilas (50 Black Women Cases 2026 - Top 30 Ranked)")
aafilas_sheet_id = create_or_get_sheet(aafilas_folder_id, "Client - Aafilas - 50 Black Women Cases (Top 30 Best + 20 Backups) Manifest")

# Create shortcut to the master Black Women Arrest Cases (2026) folder (1J9jdt8QIYa5x7ykOx8tGfPyf1FFiZRyg) and its existing manifest sheet
create_shortcut(aafilas_folder_id, "00_ALL_90_BLACK_WOMEN_CASES_MASTER_FOLDER", "1J9jdt8QIYa5x7ykOx8tGfPyf1FFiZRyg")
create_shortcut(aafilas_folder_id, "01_52_YOUTUBE_2026_RELEASES_SUBFOLDER", "1cRssoaSJHAQBFjWJ7vxTrqeBR60R6aWe")

# Load the 38 populated BW_PORTAL folders + top 12 from YouTube Releases to make 50 verified populated cases
bw_parent = "1J9jdt8QIYa5x7ykOx8tGfPyf1FFiZRyg"
q_bw = urllib.parse.quote(f"'{bw_parent}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false")
bw_folders = json.loads(urllib.request.urlopen(urllib.request.Request(
    f"https://www.googleapis.com/drive/v3/files?q={q_bw}&pageSize=100&fields=files(id,name)",
    headers={'Authorization': f'Bearer {tok}'}
)).read()).get("files", [])

empty_names = {"BW_PORTAL_16", "BW_PORTAL_19", "BW_PORTAL_25", "BW_PORTAL_28", "BW_PORTAL_31", "BW_PORTAL_37", "BW_PORTAL_45", "YouTube Releases"}
pop_portals = [f for f in sorted(bw_folders, key=lambda x: x['name']) if not any(f['name'].startswith(en) for en in empty_names)]

q_yt = urllib.parse.quote("'1cRssoaSJHAQBFjWJ7vxTrqeBR60R6aWe' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false")
yt_folders = sorted(json.loads(urllib.request.urlopen(urllib.request.Request(
    f"https://www.googleapis.com/drive/v3/files?q={q_yt}&pageSize=100&fields=files(id,name)",
    headers={'Authorization': f'Bearer {tok}'}
)).read()).get("files", []), key=lambda x: x['name'])

combined_50 = []
for idx, pf in enumerate(pop_portals[:30], 1):
    combined_50.append(("TOP 30 BEST (PURE PORTAL MULTI-CAM)", f"AAFILAS_{idx:02d}", pf['name'], f"https://drive.google.com/drive/folders/{pf['id']}", pf['id'], "100% Unposted Raw Agency Portal Release"))
for idx, pf in enumerate(pop_portals[30:38], 31):
    combined_50.append(("BACKUP 31-50 (PURE PORTAL)", f"AAFILAS_{idx:02d}", pf['name'], f"https://drive.google.com/drive/folders/{pf['id']}", pf['id'], "100% Unposted Raw Agency Portal Release"))
for idx, yf in enumerate(yt_folders[:12], 39):
    combined_50.append(("BACKUP 31-50 (2026 HD RELEASE)", f"AAFILAS_{idx:02d}", yf['name'], f"https://drive.google.com/drive/folders/{yf['id']}", yf['id'], "2026 Full Raw BWC Release"))

aafilas_rows = [["Tier (Top 30 vs Backup 31-50)", "Client Case ID", "Folder & Case Description", "Google Drive Folder Link", "Source Type"]]
for item in combined_50:
    aafilas_rows.append([item[0], item[1], item[2], item[3], item[5]])

urllib.request.urlopen(urllib.request.Request(
    f"https://sheets.googleapis.com/v4/spreadsheets/{aafilas_sheet_id}/values/A1:E{len(aafilas_rows)}?valueInputOption=USER_ENTERED",
    data=json.dumps({"values": aafilas_rows}).encode("utf-8"),
    headers={'Authorization': f'Bearer {tok}', 'Content-Type': 'application/json'},
    method="PUT"
)).read()
print("Created Aafilas folder:", aafilas_folder_id, "| Sheet:", aafilas_sheet_id)
