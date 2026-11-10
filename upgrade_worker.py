import json

sd = json.load(open(r'c:\Users\abish\Downloads\Nikhil\Bodycam Bulk Footages\sidedoor_2026_cases.json', encoding='utf-8'))
code = open(r'c:\Users\abish\Downloads\Nikhil\Bodycam Bulk Footages\worker_2026_cloud.py', encoding='utf-8').read()

# Build direct MP4 and PDF lists for 06, 07, 08, 09
af_09_mp4s = [[m['url'], m['name'].split('/')[-1]] for m in sd['tier_A_direct_cloud_and_archive_packages_2h_plus'][0]['direct_mp4_files']]
af_09_pdfs = [[u, u.split('/')[-1]] for u in sd['tier_A_direct_cloud_and_archive_packages_2h_plus'][0]['pdf_documents']]

by_case = sd['tier_A_direct_cloud_and_archive_packages_2h_plus'][1]['direct_mp4_files_by_case']
all_pdfs = sd['tier_A_direct_cloud_and_archive_packages_2h_plus'][1]['pdf_documents']

af_06_mp4s = [[m['url'], m['name'].split('/')[-1]] for m in by_case['26AF01974']]
af_06_pdfs = [[u, u.split('/')[-1]] for u in all_pdfs if '26AF01974' in u or 'Bricks-and-Minifigs' in u]

af_07_mp4s = [[m['url'], m['name'].split('/')[-1]] for m in by_case['26AF02007']]
af_07_pdfs = [[u, u.split('/')[-1]] for u in all_pdfs if '26AF02007' in u or 'Bricks-and-Minifigs' in u]

af_08_mp4s = [[m['url'], m['name'].split('/')[-1]] for m in by_case['26AF02033']]
af_08_pdfs = [[u, u.split('/')[-1]] for u in all_pdfs if '26AF02033' in u or 'Bricks-and-Minifigs' in u]

# Also let's replace 2026_CASE_06..09 and 2026_CASE_25 and add 2026_CASE_30..33 in CASES_2026
# Wait: let's load CASES_2026 by exec-ing lines 67..360 of worker_2026_cloud.py
idx_start = code.find("CASES_2026 = [")
idx_end = code.find("\ndef can_write_to_drive():")
loc = {}
exec(code[idx_start:idx_end], {}, loc)
cases = loc["CASES_2026"]

for c in cases:
    cid = c["case_id"]
    if cid == "2026_CASE_06":
        c["type"] = "archive_direct"
        c["mp4_urls"] = af_06_mp4s
        c["pdf_urls"] = af_06_pdfs
        c["summary"] += " | Direct Archive.org Unredacted 8 MP4s + 11 Official Police Report & Court PDFs."
    elif cid == "2026_CASE_07":
        c["type"] = "archive_direct"
        c["mp4_urls"] = af_07_mp4s
        c["pdf_urls"] = af_07_pdfs
        c["summary"] += " | Direct Archive.org Unredacted 8 MP4s + 11 Official Police Report & Court PDFs."
    elif cid == "2026_CASE_08":
        c["type"] = "archive_direct"
        c["mp4_urls"] = af_08_mp4s
        c["pdf_urls"] = af_08_pdfs
        c["summary"] += " | Direct Archive.org Unredacted 7 MP4s + 13 Official Booking, Probable Cause & Incident Report PDFs."
    elif cid == "2026_CASE_09":
        c["type"] = "archive_direct"
        c["expected_hrs"] = 13.51
        c["mp4_urls"] = af_09_mp4s
        c["pdf_urls"] = af_09_pdfs
        c["summary"] = "Incident Date: Mar 11, 2026 | Agency: American Fork PD (UT) Case #26AF02066 | Complete 33-Camera Unredacted Axon Body 3 & Fleet 3 Archive (13.51 hrs, 26.21 GB) + Search Warrant #3352981 & 10 Court PDFs."
    elif cid == "2026_CASE_25":
        c["tier"] = "Tier 1 (>= 2.0h)"
        c["expected_hrs"] = 2.10
        c["videos"] = ["Bflsi3HMneA", "W1IJgqKFOHI"]
        c["summary"] = "Incident Date: Feb 5, 2026 | Agency: Portland Police Bureau (OR) | 2.10 hrs combined BWC across 2 full angles."

# Add new side-door cases if not already in cases
existing_ids = {c["case_id"] for c in cases}
new_cases = [
    {
        "case_id": "2026_CASE_30",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 1.98,
        "category": "Homicide & Major Felony Investigations",
        "folder": "CASE_2026_30 - Caleb Carl Flynn Tipp City OH Police Interviews Pt 2 (Feb 16 2026)",
        "type": "youtube",
        "videos": ["yGKbvS9lyoE"],
        "summary": "Incident Date: Feb 16, 2026 | Agency: Tipp City PD / Miami County (OH) | Supplemental 1.98h (7,144s) police interviews BWC package for Caleb Carl Flynn homicide investigation."
    },
    {
        "case_id": "2026_CASE_31",
        "tier": "Tier 2 (Agency Portal)",
        "expected_hrs": 0.50,
        "category": "Officer Involved Shootings & Critical Incidents",
        "folder": "CASE_2026_31 - Sacramento Sheriff Case 26-215320 Andrea Blvd OIS (Jul 15 2026)",
        "type": "dropbox_zip",
        "zip_url": "https://www.dropbox.com/scl/fo/9tzrccmtc1o43rv6v1nee/APWPfIXD9AnwWxLpkJySUic?rlkey=cu3mfhvdaac8p4p4sezk19j96&st=5do5v71i&dl=1",
        "summary": "Incident Date: Jul 15, 2026 | Agency: Sacramento County Sheriff's Office (CA) Case #26-215320 | Direct Dropbox ZIP archive containing Deputy ICC MP4 + 911 & Radio Audio."
    },
    {
        "case_id": "2026_CASE_32",
        "tier": "Tier 2 (Agency Portal)",
        "expected_hrs": 1.50,
        "category": "Officer Involved Shootings & Critical Incidents",
        "folder": "CASE_2026_32 - San Diego PD 2026 AB748 Critical Incident Disclosures (Jan-Sep 2026)",
        "type": "archive_direct",
        "mp4_urls": [[d["mp4_url"], d["case_name"].replace("/", "-") + ".mp4"] for d in sd["tier_B_untouched_2026_agency_portal_disclosures_all_durations"][1]["direct_mp4_disclosures"]],
        "pdf_urls": [],
        "summary": "Incident Dates: Jan 21, 2026 to Sep 16, 2026 | Agency: San Diego Police Dept (CA) | 9 Direct AB 748 Critical Incident Video Disclosures from sdpdsb1421.sandiego.gov."
    },
    {
        "case_id": "2026_CASE_33",
        "tier": "Tier 2 (1.0h-1.95h)",
        "expected_hrs": 1.15,
        "category": "DUI & Traffic Stops",
        "folder": "CASE_2026_33 - Manalapan and Roselle Park NJ Municipal BWC Disclosures (May-Jun 2026)",
        "type": "youtube",
        "videos": ["7N-0Wl49B8Q", "i1SbyVi9mZM"],
        "summary": "Incident Dates: May 23, 2026 (Roselle Park PD NJ DWI Crash) & Jun 19, 2026 (Manalapan PD NJ Arrest) | 1.15 hrs combined NJ OPRA BWC."
    }
]
for nc in new_cases:
    if nc["case_id"] not in existing_ids:
        cases.append(nc)

new_cases_str = "CASES_2026 = " + json.dumps(cases, indent=4) + "\n"
code = code[:idx_start] + new_cases_str + code[idx_end:]

archive_handler = '''    elif ctype == "archive_direct":
        for p_url, p_fn in case.get("pdf_urls", []):
            dst = os.path.join(docs_dir, p_fn)
            if not os.path.exists(dst):
                subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", "-o", dst, p_url], timeout=300)
        for m_url, m_fn in case.get("mp4_urls", []):
            dst = os.path.join(vids_dir, m_fn)
            if not os.path.exists(dst):
                subprocess.run(["aria2c", "-x", "8", "-s", "8", "-d", vids_dir, "-o", m_fn, m_url], timeout=1800)
            if os.path.exists(dst):
                info = probe_video(dst)
                if info:
                    v_cnt += 1
                    tot_dur += info["dur"]
                    tot_sz += os.path.getsize(dst)
                    st[cid]["videos"] = v_cnt
                    st[cid]["hours"] = round(tot_dur / 3600, 2)
                    st[cid]["size_gb"] = round(tot_sz / (1024**3), 2)
                    st[cid]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_status(st)
                    log(f"  [ARCHIVE {cid}] Downloaded {m_fn} ({os.path.getsize(dst)/1e6:.1f} MB, {info['dur']/60:.1f}m)")
'''

if 'elif ctype == "archive_direct":' not in code:
    code = code.replace('    elif ctype == "sdpd":', archive_handler + '\n    elif ctype == "sdpd":')

with open(r'c:\Users\abish\Downloads\Nikhil\Bodycam Bulk Footages\worker_2026_cloud.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Successfully upgraded worker_2026_cloud.py with Archive.org direct S3/HTTP links and side-door cases! Total cases:", len(cases))
