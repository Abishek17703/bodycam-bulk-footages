#!/usr/bin/env python3
import os, sys, json, time, shutil, subprocess, urllib.request, urllib.parse, re, zipfile, threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import google.auth
import google.auth.transport.requests

SA_KEY = "/home/abishek17703/plobbo_sa_key.json"
FOLDER_2026_ID = "19L2kkkiLok94TQhdMQf2v7OEpZrqNVM0"

# Set up 6 WARP SOCKS5 proxies
PORTS = [40020, 40021, 40022, 40023, 40024, 40025]
WGCF_BIN = "/home/abishek17703/.local/bin/wgcf"
WIREPROXY_BIN = "/home/abishek17703/.local/bin/wireproxy"
os.makedirs("/tmp/wgcf_2026", exist_ok=True)
for idx, port in enumerate(PORTS):
    wdir = f"/tmp/wgcf_2026/w{idx}"
    os.makedirs(wdir, exist_ok=True)
    wconf = f"{wdir}/wireproxy.conf"
    if not os.path.exists(wconf):
        subprocess.run([WGCF_BIN, "register", "--accept-tos"], cwd=wdir, capture_output=True)
        subprocess.run([WGCF_BIN, "generate"], cwd=wdir, capture_output=True)
        if os.path.exists(f"{wdir}/wgcf-profile.conf"):
            prof = open(f"{wdir}/wgcf-profile.conf").read().strip()
            open(wconf, "w").write(prof + f"\n\n[Socks5]\nBindAddress = 127.0.0.1:{port}\n")
    if os.path.exists(wconf):
        r = subprocess.run(["pgrep", "-f", wconf], capture_output=True)
        if r.returncode != 0:
            subprocess.Popen(f"nohup {WIREPROXY_BIN} -c {wconf} > {wdir}/wp.log 2>&1 &", shell=True)

STAGING_ROOT = "/tmp/staging_2026"
os.makedirs(STAGING_ROOT, exist_ok=True)
STATUS_FILE = "/home/abishek17703/status_2026_verified.json"
LOG_FILE = "/home/abishek17703/worker_2026_progress.log"

VID_EXTS = {'.mp4', '.mov', '.mkv', '.avi', '.ts', '.m4v', '.webm'}
BAD_KW = re.compile(r'(cctv|surveillance|interview[\s_-]*room|interrogation|booking|cell[\s_-]*phone|3rd[\s_-]*party|third[\s_-]*party|pod[\s_-]*video|oemc|helicopter)', re.I)

log_lock = threading.Lock()
status_lock = threading.Lock()

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    with log_lock:
        sys.stdout.write(line)
        sys.stdout.flush()
        try:
            with open(LOG_FILE, "a") as f:
                f.write(line)
        except Exception:
            pass

def load_status():
    if os.path.exists(STATUS_FILE):
        try:
            return json.load(open(STATUS_FILE))
        except Exception:
            pass
    return {}

def save_status(st):
    with status_lock:
        with open(STATUS_FILE, "w") as f:
            json.dump(st, f, indent=2)

CASES_2026 = [
    {
        "case_id": "2026_CASE_01",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 3.31,
        "category": "Officer Involved Shootings & Critical Incidents",
        "folder": "CASE_2026_01 - San Diego PD 8800 Jamacha Rd OIS (Jan 22 2026)",
        "type": "sdpd",
        "portal_url": "https://www.sandiego.gov/police/data-transparency/mandated-disclosures/case?id=1-22-2026+8800+Jamacha+Rd&cat=Officer+Involved+Shootings",
        "summary": "Incident Date: Jan 22, 2026 | Agency: San Diego Police Dept (CA) | SB 16 / AB 748 Release | 3.31 hrs pure BWC (11 Officer BWC MP4s; 7 CCTV/cell clips excluded)."
    },
    {
        "case_id": "2026_CASE_02",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 2.64,
        "category": "DUI & Traffic Stops",
        "folder": "CASE_2026_02 - Abriana Velez Island Heights NJ DWI Arrest (Feb 14 2026)",
        "type": "youtube",
        "videos": [
            "TOnR1Soo1zA"
        ],
        "summary": "Incident Date: Feb 14, 2026 | Agency: Island Heights PD / Toms River (NJ) | Cit #39:4-50 | 2.64 hrs uncut BWC/dashcam | NJ OPRA arrest report & Alcotest 0.19% BAC."
    },
    {
        "case_id": "2026_CASE_03",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 4.2,
        "category": "Homicide & Major Felony Investigations",
        "folder": "CASE_2026_03 - State of Ohio v Caleb Carl Flynn Tipp City Homicide BWC (Feb 16-18 2026)",
        "type": "youtube",
        "videos": [
            "bylCTu5kwek",
            "oj5-YYH0gOo"
        ],
        "summary": "Incident Date: Feb 16-18, 2026 | Agency: Tipp City PD / Miami County (OH) | 4.20 hrs BWC package + 1.77h raw scene BWC."
    },
    {
        "case_id": "2026_CASE_04",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 2.64,
        "category": "SWAT & Tactical Raids",
        "folder": "CASE_2026_04 - Unlicensed Dental Clinic Raid Axon Body 4 (Feb 19 2026)",
        "type": "youtube",
        "videos": [
            "1CEW0VzlB7U"
        ],
        "summary": "Incident Date: Feb 19, 2026 | Axon Body 4 D01A2690Q 2026-02-19 | 2.64 hrs single-video uncut BWC."
    },
    {
        "case_id": "2026_CASE_05",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 2.26,
        "category": "DUI & Traffic Stops",
        "folder": "CASE_2026_05 - Belleville NJ Repeat DWI Arrest Patrolman Miller (Feb 21 2026)",
        "type": "youtube",
        "videos": [
            "-rvKdmOk03s",
            "A3-DuY4XDn0"
        ],
        "summary": "Incident Date: Feb 21, 2026 | Agency: Belleville PD (NJ) | 2.26 hrs across 2 linked OPRA BWC releases."
    },
    {
        "case_id": "2026_CASE_06",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 2.68,
        "category": "Trespass & Commercial Investigations",
        "folder": "CASE_2026_06 - American Fork PD UT Case 26AF01974 Day 1 BWC (Mar 8 2026)",
        "type": "archive_direct",
        "videos": [
            "hzZsOR-zcRg",
            "wQWZBoP0fHg",
            "m1rAbGFnxPQ",
            "YsXmsl7iZcA",
            "P9UVbM3EuWU",
            "YvYv5GsfPnE",
            "SAq41fFZRx0",
            "uPX3gRtuSxY"
        ],
        "summary": "Incident Date: Mar 8, 2026 | Agency: American Fork PD (UT) Case #26AF01974 | 2.68 hrs pure BWC/dashcam (Utah GRAMA release). | Direct Archive.org Unredacted 8 MP4s + 11 Official Police Report & Court PDFs.",
        "mp4_urls": [
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF01974%20-%20Bodycam_Dashcam/Richardson%20%281%20BD%2C%202%20DC%29/26AF01974%20-%20Richardson%20BC/Axon_Body_3_Video_2026-03-08_1314_X60A9891Y.mp4",
                "Axon_Body_3_Video_2026-03-08_1314_X60A9891Y.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF01974%20-%20Bodycam_Dashcam/Richardson%20%281%20BD%2C%202%20DC%29/26AF01974%20-%20Richardson%20DC/Axon_Fleet_3_Front_Camera_Video_2026-03-08_1313.mp4",
                "Axon_Fleet_3_Front_Camera_Video_2026-03-08_1313.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF01974%20-%20Bodycam_Dashcam/Richardson%20%281%20BD%2C%202%20DC%29/26AF01974%20-%20Richardson%20DC/Axon_Fleet_3_Interior_Camera_Video_2026-03-08_1313.mp4",
                "Axon_Fleet_3_Interior_Camera_Video_2026-03-08_1313.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF01974%20-%20Bodycam_Dashcam/Strong%20%281%20BD%29/26AF01974%20-%20Strong/Axon_Body_3_Video_2026-03-08_1316_X60A9919X.mp4",
                "Axon_Body_3_Video_2026-03-08_1316_X60A9919X.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF01974%20-%20Bodycam_Dashcam/Tonga%20%284%20BD%29/26AF01974%20-%20Tonga/Axon_Body_3_Video_2026-03-08_1255_X60AF8422.mp4",
                "Axon_Body_3_Video_2026-03-08_1255_X60AF8422.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF01974%20-%20Bodycam_Dashcam/Tonga%20%284%20BD%29/26AF01974%20-%20Tonga/Axon_Body_3_Video_2026-03-08_1312_X60AF8422.mp4",
                "Axon_Body_3_Video_2026-03-08_1312_X60AF8422.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF01974%20-%20Bodycam_Dashcam/Tonga%20%284%20BD%29/26AF01974%20-%20Tonga/Axon_Body_3_Video_2026-03-08_1351_X60AF8422.mp4",
                "Axon_Body_3_Video_2026-03-08_1351_X60AF8422.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF01974%20-%20Bodycam_Dashcam/Tonga%20%284%20BD%29/26AF01974%20-%20Tonga/Axon_Body_3_Video_2026-03-08_1441_X60AF8422.mp4",
                "Axon_Body_3_Video_2026-03-08_1441_X60AF8422.mp4"
            ]
        ],
        "pdf_urls": [
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/American-Fork-Police-26AF01974-Trespass-Incident-Report.pdf",
                "American-Fork-Police-26AF01974-Trespass-Incident-Report.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Complaint.pdf",
                "Bricks-and-Minifigs-Case-260200029-Complaint.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-A-LEGO-Email.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-A-LEGO-Email.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-B-Franchise-Agreement.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-B-Franchise-Agreement.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter-1.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter-1.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Motion-To-Stay-Compel-Mediation-Arbitration.pdf",
                "Bricks-and-Minifigs-Case-260200029-Motion-To-Stay-Compel-Mediation-Arbitration.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Verified-Complaint.pdf",
                "Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Verified-Complaint.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Utah-Case-260402353-Temporary-Restraining-Order-TRO.pdf",
                "Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Utah-Case-260402353-Temporary-Restraining-Order-TRO.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Errata.pdf",
                "Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Errata.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Filing-Receipt.pdf",
                "Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Filing-Receipt.pdf"
            ]
        ]
    },
    {
        "case_id": "2026_CASE_07",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 6.63,
        "category": "Trespass & Commercial Investigations",
        "folder": "CASE_2026_07 - American Fork PD UT Case 26AF02007 Day 2 BWC (Mar 9 2026)",
        "type": "archive_direct",
        "videos": [
            "UvmzV3J1-0k",
            "-7_yMWnznS0",
            "JyKEc9mLjpA",
            "ND9m3KdwrZY",
            "WXLk6vE0I3A",
            "EsABWzx6yC8",
            "LInf03-KUyc",
            "LKOfwaC3jx4"
        ],
        "summary": "Incident Date: Mar 9, 2026 | Agency: American Fork PD (UT) Case #26AF02007 | 6.63 hrs unredacted BWC/dashcam + 3.34h full BWC. | Direct Archive.org Unredacted 8 MP4s + 11 Official Police Report & Court PDFs.",
        "mp4_urls": [
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02007%20-%20Bodycam_Dashcam/Bibeau%20%281%20BC%29/26AF02007%20-%20Bibeau/Axon_Body_3_Video_2026-03-09_1942_X60A9475Y.mp4",
                "Axon_Body_3_Video_2026-03-09_1942_X60A9475Y.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02007%20-%20Bodycam_Dashcam/Fraughton%20%283%20BC%29/26AF02007%20-%20Fraughton/Axon_Body_3_Video_2026-03-09_1840_X60AA0290.mp4",
                "Axon_Body_3_Video_2026-03-09_1840_X60AA0290.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02007%20-%20Bodycam_Dashcam/Fraughton%20%283%20BC%29/26AF02007%20-%20Fraughton/Axon_Body_3_Video_2026-03-09_1905_X60AA0290.mp4",
                "Axon_Body_3_Video_2026-03-09_1905_X60AA0290.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02007%20-%20Bodycam_Dashcam/Fraughton%20%283%20BC%29/26AF02007%20-%20Fraughton/Axon_Body_3_Video_2026-03-09_1920_X60AA0290.mp4",
                "Axon_Body_3_Video_2026-03-09_1920_X60AA0290.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02007%20-%20Bodycam_Dashcam/Hawkins%20%282%20BC%2C%202%20DC%29/26AF02077%20-%20Hawkins%20BC/Axon_Body_3_Video_2026-03-09_1835_X60A9378Z.mp4",
                "Axon_Body_3_Video_2026-03-09_1835_X60A9378Z.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02007%20-%20Bodycam_Dashcam/Hawkins%20%282%20BC%2C%202%20DC%29/26AF02077%20-%20Hawkins%20BC/Axon_Body_3_Video_2026-03-09_1918_X60A9378Z.mp4",
                "Axon_Body_3_Video_2026-03-09_1918_X60A9378Z.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02007%20-%20Bodycam_Dashcam/Hawkins%20%282%20BC%2C%202%20DC%29/26AF02077%20-%20Hawkins%20DC/Axon_Fleet_3_Front_Camera_Video_2026-03-09_1917.mp4",
                "Axon_Fleet_3_Front_Camera_Video_2026-03-09_1917.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02007%20-%20Bodycam_Dashcam/Hawkins%20%282%20BC%2C%202%20DC%29/26AF02077%20-%20Hawkins%20DC/Axon_Fleet_3_Interior_Camera_Video_2026-03-09_1917.mp4",
                "Axon_Fleet_3_Interior_Camera_Video_2026-03-09_1917.mp4"
            ]
        ],
        "pdf_urls": [
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/American-Fork-Police-26AF02007-Harassment-Incident-Report.pdf",
                "American-Fork-Police-26AF02007-Harassment-Incident-Report.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Complaint.pdf",
                "Bricks-and-Minifigs-Case-260200029-Complaint.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-A-LEGO-Email.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-A-LEGO-Email.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-B-Franchise-Agreement.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-B-Franchise-Agreement.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter-1.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter-1.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Motion-To-Stay-Compel-Mediation-Arbitration.pdf",
                "Bricks-and-Minifigs-Case-260200029-Motion-To-Stay-Compel-Mediation-Arbitration.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Verified-Complaint.pdf",
                "Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Verified-Complaint.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Utah-Case-260402353-Temporary-Restraining-Order-TRO.pdf",
                "Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Utah-Case-260402353-Temporary-Restraining-Order-TRO.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Errata.pdf",
                "Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Errata.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Filing-Receipt.pdf",
                "Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Filing-Receipt.pdf"
            ]
        ]
    },
    {
        "case_id": "2026_CASE_08",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 4.14,
        "category": "Trespass & Commercial Investigations",
        "folder": "CASE_2026_08 - American Fork PD UT Case 26AF02033 RecklessBen Trespass Arrest (Mar 10 2026)",
        "type": "archive_direct",
        "videos": [
            "jSWa8tJdJMI",
            "fLFR52k56rM",
            "kqBatNeLI9E",
            "DNy4qxyg75Y",
            "16waVRC6txc",
            "sbtYgXiq7JM",
            "ZzDhOasQCx0"
        ],
        "summary": "Incident Date: Mar 10, 2026 | Agency: American Fork PD (UT) Case #26AF02033 | 4.14 hrs pure BWC/dashcam. | Direct Archive.org Unredacted 7 MP4s + 13 Official Booking, Probable Cause & Incident Report PDFs.",
        "mp4_urls": [
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02033%20-%20Bodycam_Dashcam/Canizalez%20%281%20BC%29/26AF02033%20-%20Canizalez/Axon_Body_3_Video_2026-03-10_1533_X60AJ090V.mp4",
                "Axon_Body_3_Video_2026-03-10_1533_X60AJ090V.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02033%20-%20Bodycam_Dashcam/Pitt%20%281%20BC%29/26AF02033%20-%20Pitt/Axon_Body_3_Video_2026-03-10_1542_X60A9445Z.mp4",
                "Axon_Body_3_Video_2026-03-10_1542_X60A9445Z.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02033%20-%20Bodycam_Dashcam/Somerville%20%282%20BC%29/26AF02033%20-%20Somerville/Axon_Body_3_Video_2026-03-10_1540_X60A9525X.mp4",
                "Axon_Body_3_Video_2026-03-10_1540_X60A9525X.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02033%20-%20Bodycam_Dashcam/Somerville%20%282%20BC%29/26AF02033%20-%20Somerville/Axon_Body_3_Video_2026-03-10_1718_X60A9525X.mp4",
                "Axon_Body_3_Video_2026-03-10_1718_X60A9525X.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02033%20-%20Bodycam_Dashcam/Sumbot%20%282%20BC%29/26AF02033%20-%20Sumbot/Axon_Body_3_Video_2026-03-10_1528_X60A9352Z.mp4",
                "Axon_Body_3_Video_2026-03-10_1528_X60A9352Z.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02033%20-%20Bodycam_Dashcam/Sumbot%20%282%20BC%29/26AF02033%20-%20Sumbot/Axon_Body_3_Video_2026-05-26_1319_X60A9352Z.mp4",
                "Axon_Body_3_Video_2026-05-26_1319_X60A9352Z.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02033%20-%20Bodycam_Dashcam/Valadez%2C%20M%20%281%20DC%29/26AF02033%20-%20Valadez%2C%20M/Axon_Fleet_3_Interior_Camera_Video_2026-03-10_1950.mp4",
                "Axon_Fleet_3_Interior_Camera_Video_2026-03-10_1950.mp4"
            ]
        ],
        "pdf_urls": [
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/American-Fork-Police-26AF02033-Booking-Sheet.pdf",
                "American-Fork-Police-26AF02033-Booking-Sheet.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/American-Fork-Police-26AF02033-Probable-Cause-Statement.pdf",
                "American-Fork-Police-26AF02033-Probable-Cause-Statement.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/American-Fork-Police-26AF02033-Stalking-Harassment-Incident-Report.pdf",
                "American-Fork-Police-26AF02033-Stalking-Harassment-Incident-Report.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Complaint.pdf",
                "Bricks-and-Minifigs-Case-260200029-Complaint.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-A-LEGO-Email.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-A-LEGO-Email.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-B-Franchise-Agreement.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-B-Franchise-Agreement.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter-1.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter-1.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Motion-To-Stay-Compel-Mediation-Arbitration.pdf",
                "Bricks-and-Minifigs-Case-260200029-Motion-To-Stay-Compel-Mediation-Arbitration.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Verified-Complaint.pdf",
                "Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Verified-Complaint.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Utah-Case-260402353-Temporary-Restraining-Order-TRO.pdf",
                "Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Utah-Case-260402353-Temporary-Restraining-Order-TRO.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Errata.pdf",
                "Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Errata.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Filing-Receipt.pdf",
                "Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Filing-Receipt.pdf"
            ]
        ]
    },
    {
        "case_id": "2026_CASE_09",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 13.51,
        "category": "SWAT & Tactical Raids",
        "folder": "CASE_2026_09 - American Fork PD UT Case 26AF02066 Airbnb Search Warrant Raid (Mar 11 2026)",
        "type": "archive_direct",
        "videos": [
            "bZZaQMuQw9c",
            "_6iT8g2u4xM",
            "Ek_4kGUKez0",
            "0rwdsjUlATc",
            "1EgLvaosyEo",
            "Un4zfNws5kY",
            "hwbkP-CrnoU",
            "Iu-0UlVwILk"
        ],
        "summary": "Incident Date: Mar 11, 2026 | Agency: American Fork PD (UT) Case #26AF02066 | Complete 33-Camera Unredacted Axon Body 3 & Fleet 3 Archive (13.51 hrs, 26.21 GB) + Search Warrant #3352981 & 10 Court PDFs.",
        "mp4_urls": [
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Adamson%20%282%20BC%29/26AF02066%20-%20Adamson/Axon_Body_3_Video_2026-03-11_1508_X60A9488Y.mp4",
                "Axon_Body_3_Video_2026-03-11_1508_X60A9488Y.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Adamson%20%282%20BC%29/26AF02066%20-%20Adamson/Axon_Body_3_Video_2026-03-11_1748_X60A9488Y.mp4",
                "Axon_Body_3_Video_2026-03-11_1748_X60A9488Y.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Gonzalez%20%281%20BC%2C%202%20DC%29/26AF02066%20-%20Gonzalez%20BC/Axon_Body_3_Video_2026-03-11_1747_X60AH450S.mp4",
                "Axon_Body_3_Video_2026-03-11_1747_X60AH450S.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Gonzalez%20%281%20BC%2C%202%20DC%29/26AF02066%20-%20Gonzalez%20DC/Axon_Fleet_3_Front_Camera_Video_2026-03-11_1757.mp4",
                "Axon_Fleet_3_Front_Camera_Video_2026-03-11_1757.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Gonzalez%20%281%20BC%2C%202%20DC%29/26AF02066%20-%20Gonzalez%20DC/Axon_Fleet_3_Interior_Camera_Video_2026-03-11_1757.mp4",
                "Axon_Fleet_3_Interior_Camera_Video_2026-03-11_1757.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Jensen%20%281%20BC%29/26AF02066%20-%20Jensen/Axon_Body_3_Video_2026-03-11_1747_X60AA1310.mp4",
                "Axon_Body_3_Video_2026-03-11_1747_X60AA1310.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Laycock%20%281%20BC%2C%201%20DC%29/26AF02066%20-%20Laycock%20BC/Axon_Body_3_Video_2026-03-11_1747_X6032265P.mp4",
                "Axon_Body_3_Video_2026-03-11_1747_X6032265P.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Laycock%20%281%20BC%2C%201%20DC%29/26AF02066%20-%20Laycock%20DC/Axon_Fleet_3_Interior_Camera_Video_2026-03-11_1754.mp4",
                "Axon_Fleet_3_Interior_Camera_Video_2026-03-11_1754.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Lott%20%281%20BC%29/26AF02066%20-%20Lott/Axon_Body_3_Video_2026-03-11_1748_X60AA0390.mp4",
                "Axon_Body_3_Video_2026-03-11_1748_X60AA0390.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Neil%20%281%20BC%29/26AF02066%20-%20Neil/Axon_Body_3_Video_2026-03-11_1516_X60AA0420.mp4",
                "Axon_Body_3_Video_2026-03-11_1516_X60AA0420.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Nicosia%20%2811%20BC%29/26AF02066%20-%20Nicosia/Axon_Body_3_Video_2026-03-11_1551_X60A9522X.mp4",
                "Axon_Body_3_Video_2026-03-11_1551_X60A9522X.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Nicosia%20%2811%20BC%29/26AF02066%20-%20Nicosia/Axon_Body_3_Video_2026-03-11_1612_X60A9522X.mp4",
                "Axon_Body_3_Video_2026-03-11_1612_X60A9522X.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Nicosia%20%2811%20BC%29/26AF02066%20-%20Nicosia/Axon_Body_3_Video_2026-03-11_1642_X60A9522X.mp4",
                "Axon_Body_3_Video_2026-03-11_1642_X60A9522X.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Nicosia%20%2811%20BC%29/26AF02066%20-%20Nicosia/Axon_Body_3_Video_2026-03-11_1740_X60A9522X.mp4",
                "Axon_Body_3_Video_2026-03-11_1740_X60A9522X.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Nicosia%20%2811%20BC%29/26AF02066%20-%20Nicosia/Axon_Body_3_Video_2026-03-11_1828_X60A9522X.mp4",
                "Axon_Body_3_Video_2026-03-11_1828_X60A9522X.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Nicosia%20%2811%20BC%29/26AF02066%20-%20Nicosia/Axon_Body_3_Video_2026-03-11_1834_X60A9522X.mp4",
                "Axon_Body_3_Video_2026-03-11_1834_X60A9522X.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Nicosia%20%2811%20BC%29/26AF02066%20-%20Nicosia/Axon_Body_3_Video_2026-03-11_1913_X60A9522X.mp4",
                "Axon_Body_3_Video_2026-03-11_1913_X60A9522X.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Nicosia%20%2811%20BC%29/26AF02066%20-%20Nicosia/Axon_Body_3_Video_2026-03-11_1926_X60A9522X.mp4",
                "Axon_Body_3_Video_2026-03-11_1926_X60A9522X.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Nicosia%20%2811%20BC%29/26AF02066%20-%20Nicosia/Axon_Body_3_Video_2026-03-11_1955_X60A9522X.mp4",
                "Axon_Body_3_Video_2026-03-11_1955_X60A9522X.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Nicosia%20%2811%20BC%29/26AF02066%20-%20Nicosia/Axon_Body_3_Video_2026-03-11_2001_X60A9522X.mp4",
                "Axon_Body_3_Video_2026-03-11_2001_X60A9522X.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Nicosia%20%2811%20BC%29/26AF02066%20-%20Nicosia/Axon_Body_3_Video_2026-03-11_2009_X60A9522X.mp4",
                "Axon_Body_3_Video_2026-03-11_2009_X60A9522X.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Richardson%20%287%20BC%2C%202%20DC%29/26AF02066%20-%20Richardson%20BC/Axon_Body_3_Video_2026-03-11_1508_X60A9891Y.mp4",
                "Axon_Body_3_Video_2026-03-11_1508_X60A9891Y.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Richardson%20%287%20BC%2C%202%20DC%29/26AF02066%20-%20Richardson%20BC/Axon_Body_3_Video_2026-03-11_1542_X60A9891Y.mp4",
                "Axon_Body_3_Video_2026-03-11_1542_X60A9891Y.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Richardson%20%287%20BC%2C%202%20DC%29/26AF02066%20-%20Richardson%20BC/Axon_Body_3_Video_2026-03-11_1552_X60A9891Y.mp4",
                "Axon_Body_3_Video_2026-03-11_1552_X60A9891Y.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Richardson%20%287%20BC%2C%202%20DC%29/26AF02066%20-%20Richardson%20BC/Axon_Body_3_Video_2026-03-11_1747_X60A9891Y.mp4",
                "Axon_Body_3_Video_2026-03-11_1747_X60A9891Y.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Richardson%20%287%20BC%2C%202%20DC%29/26AF02066%20-%20Richardson%20BC/Axon_Body_3_Video_2026-03-11_1814_X60A9891Y.mp4",
                "Axon_Body_3_Video_2026-03-11_1814_X60A9891Y.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Richardson%20%287%20BC%2C%202%20DC%29/26AF02066%20-%20Richardson%20BC/Axon_Body_3_Video_2026-03-11_1818_X60A9891Y.mp4",
                "Axon_Body_3_Video_2026-03-11_1818_X60A9891Y.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Richardson%20%287%20BC%2C%202%20DC%29/26AF02066%20-%20Richardson%20BC/Axon_Body_3_Video_2026-03-11_1847_X60A9891Y.mp4",
                "Axon_Body_3_Video_2026-03-11_1847_X60A9891Y.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Richardson%20%287%20BC%2C%202%20DC%29/26AF02066%20-%20Richardson%20DC/Axon_Fleet_3_Interior_Camera_Video_2026-03-11_1527.mp4",
                "Axon_Fleet_3_Interior_Camera_Video_2026-03-11_1527.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Richardson%20%287%20BC%2C%202%20DC%29/26AF02066%20-%20Richardson%20DC/Axon_Fleet_3_Interior_Camera_Video_2026-03-11_1756.mp4",
                "Axon_Fleet_3_Interior_Camera_Video_2026-03-11_1756.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Tonga%20%282%20BC%2C%201%20DC%29/26AF02066%20-%20Tonga/Axon_Body_3_Video_2026-03-11_1700_X60AF8422.mp4",
                "Axon_Body_3_Video_2026-03-11_1700_X60AF8422.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Tonga%20%282%20BC%2C%201%20DC%29/26AF02066%20-%20Tonga/Axon_Body_3_Video_2026-03-11_1747_X60AF8422.mp4",
                "Axon_Body_3_Video_2026-03-11_1747_X60AF8422.mp4"
            ],
            [
                "https://archive.org/download/american-fork-pd-unredacted-body-dashcam-6-3-26-220-pm/American%20Fork%20PD%20-%20Unredacted%20Body%20%26%20Dashcam%206-3-26%20220PM/26AF02066%20-%20Bodycam_Dashcam/Tonga%20%282%20BC%2C%201%20DC%29/26AF02066%20-%20Tonga/Axon_Fleet_3_Interior_Camera_Video_2026-03-11_2013.mp4",
                "Axon_Fleet_3_Interior_Camera_Video_2026-03-11_2013.mp4"
            ]
        ],
        "pdf_urls": [
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/American-Fork-Police-Warrant-3352981-Search-Warrant.pdf",
                "American-Fork-Police-Warrant-3352981-Search-Warrant.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Complaint.pdf",
                "Bricks-and-Minifigs-Case-260200029-Complaint.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-A-LEGO-Email.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-A-LEGO-Email.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-B-Franchise-Agreement.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-B-Franchise-Agreement.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter-1.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter-1.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter.pdf",
                "Bricks-and-Minifigs-Case-260200029-Exhibit-D-Termination-Letter.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-Case-260200029-Motion-To-Stay-Compel-Mediation-Arbitration.pdf",
                "Bricks-and-Minifigs-Case-260200029-Motion-To-Stay-Compel-Mediation-Arbitration.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Verified-Complaint.pdf",
                "Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Verified-Complaint.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Utah-Case-260402353-Temporary-Restraining-Order-TRO.pdf",
                "Bricks-and-Minifigs-v-Benjamin-Paul-Schneider-Reckless-Ben-Utah-Case-260402353-Temporary-Restraining-Order-TRO.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Errata.pdf",
                "Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Errata.pdf"
            ],
            [
                "https://archive.org/download/reckless-ben-BAM-bodycam-docs/Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Filing-Receipt.pdf",
                "Bricks-and-Minifigs-v-Reckless-Ben-Bryan-Mansell-Utah-Case-260402353-Filing-Receipt.pdf"
            ]
        ]
    },
    {
        "case_id": "2026_CASE_10",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 6.32,
        "category": "DUI & Traffic Stops",
        "folder": "CASE_2026_10 - Eldrick Tiger Woods Martin County FL Rollover Crash and DUI Arrest (Mar 27 2026)",
        "type": "youtube",
        "videos": [
            "ll2OAuH-Rh4",
            "1w9iwOxrLNc"
        ],
        "summary": "Incident Date: Mar 27, 2026 | Agency: Martin County Sheriff's Office / Jupiter Island PD (FL) | 6.32 hrs combined BWC (Pt 1 2.10h + Pt 2 4.22h)."
    },
    {
        "case_id": "2026_CASE_11",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 2.05,
        "category": "Officer Involved Shootings & Critical Incidents",
        "folder": "CASE_2026_11 - San Diego PD 1600 Island Avenue OIS (Apr 15 2026)",
        "type": "sdpd",
        "portal_url": "https://www.sandiego.gov/police/data-transparency/mandated-disclosures/case?id=04-15-2026+1600+Island+Avenue&cat=Officer+Involved+Shootings",
        "summary": "Incident Date: Apr 15, 2026 | Agency: San Diego Police Dept (CA) | SB 16 / AB 748 Release | 2.05 hrs pure BWC across 10 Officer BWC MP4s (witness cell clip excluded)."
    },
    {
        "case_id": "2026_CASE_12",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 2.1,
        "category": "Officer Involved Shootings & Critical Incidents",
        "folder": "CASE_2026_12 - Sacramento Sheriff Case 26-204373 I-80 Antelope Rd OIS (Jul 5 2026)",
        "type": "dropbox_zip",
        "zip_url": "https://www.dropbox.com/scl/fo/cauc43k7wvndp57f4lxip/AK7WIBug-8FMpFMgxE0WQOI?rlkey=5e7rbnxa4yg5c2gwia12jl1t3&st=diad27g6&dl=1",
        "summary": "Incident Date: Jul 5, 2026 | Agency: Sacramento County Sheriff's Office (CA) Case #26-204373 | William Kreuzer OIS | 3.23 GB multi-deputy BWC & 911 audio archive."
    },
    {
        "case_id": "2026_CASE_13",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 3.4,
        "category": "Domestic & Warrant Investigations",
        "folder": "CASE_2026_13 - Kroy Biermann and KJ Biermann Jr Milton Alpharetta GA BWC Series (Aug 17-22 2026)",
        "type": "youtube",
        "videos": [
            "7PD9TLFEzXE",
            "TH5eYGyLDYo",
            "cR59ZyB8WA8"
        ],
        "summary": "Incident Date: Aug 17-22, 2026 | Agency: Milton / Alpharetta PD (GA) | 3.40 hrs across 3 Georgia Open Records Act BWC releases."
    },
    {
        "case_id": "2026_CASE_14",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 2.95,
        "category": "Theft & Follow-Up Investigations",
        "folder": "CASE_2026_14 - Alleigha Botner Miami County OH BWC Series (Aug 28 2026)",
        "type": "youtube",
        "videos": [
            "LXZ--DdCc98",
            "17N8Q9WwZ6Y"
        ],
        "summary": "Incident Date: Aug 28, 2026 | Agency: Miami County / Tipp City PD (OH) | 2.95 hrs across 2 Ohio Public Records Act BWC releases."
    },
    {
        "case_id": "2026_CASE_15",
        "tier": "Tier 2 (1.0h-1.95h)",
        "expected_hrs": 1.87,
        "category": "DUI & Traffic Stops",
        "folder": "CASE_2026_15 - Somerville NJ Chief of Detectives 5-Car Crash DWI Arrest (Mar 20 2026)",
        "type": "youtube",
        "videos": [
            "JFY1QjORd1U"
        ],
        "summary": "Incident Date: Mar 20, 2026 | Agency: Somerville PD (NJ) | 1.87 hrs pure BWC."
    },
    {
        "case_id": "2026_CASE_16",
        "tier": "Tier 2 (1.0h-1.95h)",
        "expected_hrs": 1.66,
        "category": "DUI & Traffic Stops",
        "folder": "CASE_2026_16 - West New York NJ Suspended License Double Limit DWI (May 3 2026)",
        "type": "youtube",
        "videos": [
            "66z-K-PDLXk"
        ],
        "summary": "Incident Date: May 3, 2026 | Agency: West New York PD (NJ) | 1.66 hrs pure BWC."
    },
    {
        "case_id": "2026_CASE_17",
        "tier": "Tier 2 (1.0h-1.95h)",
        "expected_hrs": 1.57,
        "category": "DUI & Traffic Stops",
        "folder": "CASE_2026_17 - Highlands NJ Husband and Wife Both Arrested for DWI (Jun 30 2026)",
        "type": "youtube",
        "videos": [
            "QKQXjP9JE10"
        ],
        "summary": "Incident Date: Jun 30, 2026 | Agency: Highlands PD (NJ) | 1.57 hrs pure BWC."
    },
    {
        "case_id": "2026_CASE_18",
        "tier": "Tier 2 (1.0h-1.95h)",
        "expected_hrs": 1.45,
        "category": "Trespass & Commercial Investigations",
        "folder": "CASE_2026_18 - Delayed Flight Dispute and Arrest at Airport Gate (Mar 16 2026)",
        "type": "youtube",
        "videos": [
            "FKJ4p4U3IQk"
        ],
        "summary": "Incident Date: Mar 16, 2026 | Airport Law Enforcement | 1.45 hrs pure BWC."
    },
    {
        "case_id": "2026_CASE_19",
        "tier": "Tier 2 (1.0h-1.95h)",
        "expected_hrs": 1.42,
        "category": "Domestic & Warrant Investigations",
        "folder": "CASE_2026_19 - Elizabeth NJ Campaign Manager Assaults Officers at Woodruff Circle Park (Jun 2 2026)",
        "type": "youtube",
        "videos": [
            "YRhCHpll1Bw"
        ],
        "summary": "Incident Date: Jun 2, 2026 | Agency: Elizabeth PD (NJ) | 1.42 hrs pure BWC."
    },
    {
        "case_id": "2026_CASE_20",
        "tier": "Tier 2 (1.0h-1.95h)",
        "expected_hrs": 1.27,
        "category": "DUI & Traffic Stops",
        "folder": "CASE_2026_20 - Sofia Barranco UCF Police DUI Arrest (Jan 17 2026)",
        "type": "youtube",
        "videos": [
            "_-s3Wkt4onQ"
        ],
        "summary": "Incident Date: Jan 17, 2026 | Agency: University of Central Florida PD (FL) | 1.27 hrs pure BWC."
    },
    {
        "case_id": "2026_CASE_21",
        "tier": "Tier 2 (1.0h-1.95h)",
        "expected_hrs": 1.19,
        "category": "Vehicle Pursuits & PIT Maneuvers",
        "folder": "CASE_2026_21 - NFL Player James Pearce Jr Doral FL Police Chase and Arrest (Feb 7 2026)",
        "type": "youtube",
        "videos": [
            "P-GuP8IO86I"
        ],
        "summary": "Incident Date: Feb 7, 2026 | Agency: Doral PD (FL) | 1.19 hrs pure BWC."
    },
    {
        "case_id": "2026_CASE_22",
        "tier": "Tier 2 (1.0h-1.95h)",
        "expected_hrs": 1.19,
        "category": "DUI & Traffic Stops",
        "folder": "CASE_2026_22 - West New York NJ 5200 Kennedy Blvd DWI Checkpoint Arrest (Feb 22 2026)",
        "type": "youtube",
        "videos": [
            "3UE1MALWPEo"
        ],
        "summary": "Incident Date: Feb 22, 2026 | Agency: West New York PD (NJ) | 1.19 hrs pure BWC."
    },
    {
        "case_id": "2026_CASE_23",
        "tier": "Tier 2 (1.0h-1.95h)",
        "expected_hrs": 1.18,
        "category": "Domestic & Warrant Investigations",
        "folder": "CASE_2026_23 - West New York NJ 580 67th St Mini Cooper Road Rage Fight Arrest (Apr 1 2026)",
        "type": "youtube",
        "videos": [
            "7UHkELlJ2Nc"
        ],
        "summary": "Incident Date: Apr 1, 2026 | Agency: West New York PD (NJ) | 1.18 hrs pure BWC."
    },
    {
        "case_id": "2026_CASE_24",
        "tier": "Tier 2 (1.0h-1.95h)",
        "expected_hrs": 1.13,
        "category": "DUI & Traffic Stops",
        "folder": "CASE_2026_24 - Tony Romo Texas OWI Traffic Stop and Arrest (Jul 23 2026)",
        "type": "youtube",
        "videos": [
            "duGZ2tPZrf8"
        ],
        "summary": "Incident Date: Jul 23, 2026 | Texas Law Enforcement | 1.13 hrs pure BWC."
    },
    {
        "case_id": "2026_CASE_25",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 2.1,
        "category": "Officer Involved Shootings & Critical Incidents",
        "folder": "CASE_2026_25 - Portland Police Bureau OR Officer-Involved Shooting BWC (Feb 5 2026)",
        "type": "youtube",
        "videos": [
            "Bflsi3HMneA",
            "W1IJgqKFOHI"
        ],
        "summary": "Incident Date: Feb 5, 2026 | Agency: Portland Police Bureau (OR) | 2.10 hrs combined BWC across 2 full angles."
    },
    {
        "case_id": "2026_CASE_26",
        "tier": "Tier 2 (1.0h-1.95h)",
        "expected_hrs": 1.06,
        "category": "Theft & Follow-Up Investigations",
        "folder": "CASE_2026_26 - Voorhees Township NJ Boscovs Sisters Shoplifting Arrest (Feb 26 2026)",
        "type": "youtube",
        "videos": [
            "FVMbiAxzgNo"
        ],
        "summary": "Incident Date: Feb 26, 2026 | Agency: Voorhees Township PD (NJ) | 1.06 hrs pure BWC."
    },
    {
        "case_id": "2026_CASE_27",
        "tier": "Tier 2 (1.0h-1.95h)",
        "expected_hrs": 1.05,
        "category": "DUI & Traffic Stops",
        "folder": "CASE_2026_27 - ShaCarri Richardson Orange County FL 104 MPH Speeding Arrest (Jan 29 2026)",
        "type": "youtube",
        "videos": [
            "QjzAtwGcRUg"
        ],
        "summary": "Incident Date: Jan 29, 2026 | Agency: Orange County Sheriff's Office (FL) | 1.05 hrs pure BWC."
    },
    {
        "case_id": "2026_CASE_28",
        "tier": "Tier 2 (1.0h-1.95h)",
        "expected_hrs": 1.05,
        "category": "Officer Involved Shootings & Critical Incidents",
        "folder": "CASE_2026_28 - Sacramento Sheriff Case 26-49615 Bruceville Rd OIS (Feb 16 2026)",
        "type": "dropbox_zip",
        "zip_url": "https://www.dropbox.com/scl/fo/ifkg6o1jrbsyl6ys7ex6u/AI-Q4h7sMa2hgNzC1XjYjLM?rlkey=1qnkzm2s1xl5z1fnynak3rpfs&st=mrr35oyq&dl=1",
        "summary": "Incident Date: Feb 16, 2026 | Agency: Sacramento County Sheriff's Office (CA) Case #26-49615 | 1.54 GB multi-deputy BWC archive."
    },
    {
        "case_id": "2026_CASE_29",
        "tier": "Tier 2 (1.0h-1.95h)",
        "expected_hrs": 1.04,
        "category": "Officer Involved Shootings & Critical Incidents",
        "folder": "CASE_2026_29 - Sacramento Sheriff Case 26-61709 Block New Hope Rd OIS (Feb 27 2026)",
        "type": "dropbox_zip",
        "zip_url": "https://www.dropbox.com/scl/fo/yyb1mjo641egin8fvihy2/ALN8knFrBl6-MB4J0_OyDNI?rlkey=nct7xjgh91fi48onawce41phz&st=18657fij&dl=1",
        "summary": "Incident Date: Feb 27, 2026 | Agency: Sacramento County Sheriff's Office (CA) Case #26-61709 | 1.53 GB multi-deputy BWC archive."
    },
    {
        "case_id": "2026_CASE_30",
        "tier": "Tier 1 (>= 2.0h)",
        "expected_hrs": 1.98,
        "category": "Homicide & Major Felony Investigations",
        "folder": "CASE_2026_30 - Caleb Carl Flynn Tipp City OH Police Interviews Pt 2 (Feb 16 2026)",
        "type": "youtube",
        "videos": [
            "yGKbvS9lyoE"
        ],
        "summary": "Incident Date: Feb 16, 2026 | Agency: Tipp City PD / Miami County (OH) | Supplemental 1.98h (7,144s) police interviews BWC package for Caleb Carl Flynn homicide investigation."
    },
    {
        "case_id": "2026_CASE_31",
        "tier": "Tier 2 (Agency Portal)",
        "expected_hrs": 0.5,
        "category": "Officer Involved Shootings & Critical Incidents",
        "folder": "CASE_2026_31 - Sacramento Sheriff Case 26-215320 Andrea Blvd OIS (Jul 15 2026)",
        "type": "dropbox_zip",
        "zip_url": "https://www.dropbox.com/scl/fo/9tzrccmtc1o43rv6v1nee/APWPfIXD9AnwWxLpkJySUic?rlkey=cu3mfhvdaac8p4p4sezk19j96&st=5do5v71i&dl=1",
        "summary": "Incident Date: Jul 15, 2026 | Agency: Sacramento County Sheriff's Office (CA) Case #26-215320 | Direct Dropbox ZIP archive containing Deputy ICC MP4 + 911 & Radio Audio."
    },
    {
        "case_id": "2026_CASE_32",
        "tier": "Tier 2 (Agency Portal)",
        "expected_hrs": 1.5,
        "category": "Officer Involved Shootings & Critical Incidents",
        "folder": "CASE_2026_32 - San Diego PD 2026 AB748 Critical Incident Disclosures (Jan-Sep 2026)",
        "type": "archive_direct",
        "mp4_urls": [
            [
                "https://sdpdsb1421.sandiego.gov/AB%20748/2026/01-21-2026%202900%20Balboa/Video/San+Diego+PD+-+OIS+121626++2900+Balboa.mp4",
                "01-21-2026 2900 Balboa (AB 748).mp4"
            ],
            [
                "https://sdpdsb1421.sandiego.gov/AB%20748/2026/01-22-2026%20Jamacha%20Road/Video/San+Diego+PD+-+OIS+012226+Jamacha.mp4",
                "01-22-2026 Jamacha Road (AB 748 Briefing Video).mp4"
            ],
            [
                "https://sdpdsb1421.sandiego.gov/AB%20748/2026/04-15-2026%2016th%20and%20Island/Video/San+Diego+PD+-+OIS+041526+16th+and+Island+FINAL+1+%281%29.mp4",
                "04-15-2026 16th and Island (AB 748 Briefing Video).mp4"
            ],
            [
                "https://sdpdsb1421.sandiego.gov/AB%20748/2026/05-06-2026%20Derby%20Farms/Video/San+Diego+PD+-+OIS+050626+Steeple+Chase+-+Derby+Farms+FINAL+1+%281%29.mp4",
                "05-06-2026 Derby Farms (AB 748).mp4"
            ],
            [
                "https://sdpdsb1421.sandiego.gov/AB%20748/2026/06-23-2026%201600%206th%20Avenue/Video/San+Diego+PD+-+OIS+062326+1600+6th+Avenue+.mp4",
                "06-23-2026 1600 6th Avenue (AB 748).mp4"
            ],
            [
                "https://sdpdsb1421.sandiego.gov/AB%20748/2026/06-30-2026%204700%20Pacific%20Hwy/Video/San+Diego+PD+-+OIS+063026+4700+Pac+Highway+FINAL+3+%281%29.mp4",
                "06-30-2026 4700 Pacific Hwy (AB 748).mp4"
            ],
            [
                "https://sdpdsb1421.sandiego.gov/AB%20748/2026/07-29-2026%20Beyer%20and%20Del%20Sur/Video/San+Diego+PD+-+OIS+072926+Beyer+and+Del+Sur+Blvd+FINAL+2+%281%29.mp4",
                "07-29-2026 Beyer and Del Sur (AB 748).mp4"
            ],
            [
                "https://sdpdsb1421.sandiego.gov/AB%20748/2026/08-25-2026%20Nipoma%20Street/Video/San+Diego+PD+-+OIS+082526+2758+Nipoma+Street+FINAL+1.mp4",
                "08-25-2026 Nipoma Street (AB 748).mp4"
            ],
            [
                "https://sdpdsb1421.sandiego.gov/AB%20748/2026/09-16-2026%204000%2030t%20Street/Video/San+Diego+PD+-+OIS+091626+4000+30th+Street+FINAL+1.mp4",
                "09-16-2026 4000 30th Street (AB 748).mp4"
            ]
        ],
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
        "videos": [
            "7N-0Wl49B8Q",
            "i1SbyVi9mZM"
        ],
        "summary": "Incident Dates: May 23, 2026 (Roselle Park PD NJ DWI Crash) & Jun 19, 2026 (Manalapan PD NJ Arrest) | 1.15 hrs combined NJ OPRA BWC."
    }
]

def can_write_to_drive():
    return True

def setup_rclone():
    pass

def probe_video(fp):
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height:format=duration",
             "-of", "json", fp], timeout=45
        ).decode("utf-8", errors="ignore")
        d = json.loads(out)
        streams = d.get("streams", [])
        if not streams: return None
        return {
            "w": int(streams[0].get("width", 0)),
            "h": int(streams[0].get("height", 0)),
            "dur": float(d.get("format", {}).get("duration", 0.0))
        }
    except Exception:
        return None

def download_yt(vid, vids_dir, w_idx):
    existing = [x for x in os.listdir(vids_dir) if f"[{vid}]" in x and x.endswith(".mp4") and not re.search(r'\.f\d+\.', x)]
    if existing:
        fp = os.path.join(vids_dir, existing[0])
        info = probe_video(fp)
        if info and info["dur"] > 0:
            return True, info["dur"], os.path.getsize(fp)
    port = PORTS[w_idx % len(PORTS)]
    tmp_dir = f"/tmp/yt2026_{w_idx}_{vid}"
    shutil.rmtree(tmp_dir, ignore_errors=True)
    os.makedirs(tmp_dir, exist_ok=True)
    out_tmpl = os.path.join(tmp_dir, f"%(title).100B [{vid}].%(ext)s")
    for attempt in range(3):
        cmd = [
            "/home/abishek17703/.local/bin/yt-dlp",
            "--extractor-args", "youtube:player_client=android,web",
            "-f", "136+140/298+140/18/bestvideo[height>=720][height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height>=720]/best",
            "--merge-output-format", "mp4", "--concurrent-fragments", "32",
            "--downloader", "aria2c", "--downloader-args", "aria2c:-x 16 -s 16 -k 1M",
            "--retries", "15", "--fragment-retries", "15", "--no-part", "--no-playlist",
            "-o", out_tmpl, f"https://www.youtube.com/watch?v={vid}"
        ]
        if attempt > 0:
            p = PORTS[(w_idx + attempt) % len(PORTS)]
            cmd[1:1] = ["--proxy", f"socks5://127.0.0.1:{p}"]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3600)
        dl = [x for x in os.listdir(tmp_dir) if x.endswith(".mp4") and not re.search(r'\.f\d+\.', x)]
        if dl:
            fp = os.path.join(tmp_dir, dl[0])
            info = probe_video(fp)
            if info and info["dur"] > 0:
                sz = os.path.getsize(fp)
                shutil.move(fp, os.path.join(vids_dir, dl[0]))
                shutil.rmtree(tmp_dir, ignore_errors=True)
                log(f"  [YT {vid}] Downloaded {dl[0]} ({sz/1e6:.1f} MB, {info['dur']/60:.1f}m)")
                return True, info["dur"], sz
    shutil.rmtree(tmp_dir, ignore_errors=True)
    log(f"  [YT {vid}] FAILED after retries")
    return False, 0.0, 0

def sync_case_to_drive(case, case_dir, st):
    cid = case["case_id"]
    if not can_write_to_drive():
        return False
    remote_dest = f"gdrive2026:{case['category']}/{case['folder']}"
    log(f"  [DRIVE UPLOAD] Uploading {cid} -> {remote_dest} ...")
    r = subprocess.run([
        "rclone", "move", case_dir, remote_dest,
        "--transfers", "16", "--checkers", "16", "--drive-chunk-size", "128M", "--drive-upload-cutoff", "128M", "--fast-list", "--delete-empty-src-dirs"
    ], capture_output=True, text=True)
    if r.returncode == 0:
        shutil.rmtree(case_dir, ignore_errors=True)
        st[cid]["state"] = "UPLOADED_TO_DRIVE"
        st[cid]["uploaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_status(st)
        log(f"  [DRIVE UPLOAD COMPLETE] {cid} uploaded and local staging freed!")
        return True
    else:
        log(f"  [DRIVE UPLOAD ERROR] {cid}: {r.stderr[:200]}")
        return False

def process_case(case, idx, st):
    cid = case["case_id"]
    if st.get(cid, {}).get("state") == "UPLOADED_TO_DRIVE" and st.get(cid, {}).get("videos", 0) > 0:
        return

    cat_dir = os.path.join(STAGING_ROOT, case["category"])
    case_dir = os.path.join(cat_dir, case["folder"])
    vids_dir = os.path.join(case_dir, "Videos")
    docs_dir = os.path.join(case_dir, "Documents")
    os.makedirs(vids_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)

    st[cid] = {
        "case_id": cid,
        "tier": case["tier"],
        "folder": case["folder"],
        "expected_hrs": case["expected_hrs"],
        "state": "DOWNLOADING",
        "videos": 0,
        "hours": 0.0,
        "size_gb": 0.0,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_status(st)

    with open(os.path.join(docs_dir, "Official_Case_Documentation_Summary.txt"), "w") as f:
        f.write(case["summary"] + "\n")

    ctype = case["type"]
    tot_dur, tot_sz, v_cnt = 0.0, 0, 0
    log(f"=== Starting {cid}: {case['folder']} ({ctype}) ===")

    if ctype == "youtube":
        with ThreadPoolExecutor(max_workers=3) as v_ex:
            vfuts = [v_ex.submit(download_yt, vid, vids_dir, idx + j) for j, vid in enumerate(case["videos"])]
            for vfut in as_completed(vfuts):
                ok, dur, sz = vfut.result()
                if ok:
                    v_cnt += 1
                    tot_dur += dur
                    tot_sz += sz
                    st[cid]["videos"] = v_cnt
                    st[cid]["hours"] = round(tot_dur / 3600, 2)
                    st[cid]["size_gb"] = round(tot_sz / (1024**3), 2)
                    st[cid]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_status(st)

    elif ctype == "archive_direct":
        for p_url, p_fn in case.get("pdf_urls", []):
            dst = os.path.join(docs_dir, p_fn)
            if not os.path.exists(dst):
                subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", "-o", dst, p_url], timeout=300)
        mp4_list = case.get("mp4_urls", [])
        def dl_arch_one(item):
            m_url, m_fn = item
            dst = os.path.join(vids_dir, m_fn)
            if not os.path.exists(dst):
                subprocess.run(["aria2c", "-x", "16", "-s", "16", "-k", "1M", "--file-allocation=none", "-q", "-d", vids_dir, "-o", m_fn, m_url], timeout=1800)
            if os.path.exists(dst):
                info = probe_video(dst)
                if info:
                    sz = os.path.getsize(dst)
                    log(f"  [ARCHIVE {cid}] Downloaded {m_fn} ({sz/1e6:.1f} MB, {info['dur']/60:.1f}m)")
                    if len(mp4_list) > 6:
                        remote_vids = f"gdrive2026:{case['category']}/{case['folder']}/Videos"
                        subprocess.run(["rclone", "move", dst, remote_vids, "--drive-chunk-size", "128M", "--transfers", "8"], capture_output=True)
                    return True, info["dur"], sz
            return False, 0.0, 0

        with ThreadPoolExecutor(max_workers=4) as a_ex:
            afuts = [a_ex.submit(dl_arch_one, item) for item in mp4_list]
            for afut in as_completed(afuts):
                ok, dur, sz = afut.result()
                if ok:
                    v_cnt += 1
                    tot_dur += dur
                    tot_sz += sz
                    st[cid]["videos"] = v_cnt
                    st[cid]["hours"] = round(tot_dur / 3600, 2)
                    st[cid]["size_gb"] = round(tot_sz / (1024**3), 2)
                    st[cid]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    save_status(st)

    elif ctype == "sdpd":
        req = urllib.request.Request(case["portal_url"], headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", errors="ignore")
        pdfs = re.findall(r'href=["\']([^"\']+\.pdf)["\']', html, re.I)
        mp4s = re.findall(r'href=["\']([^"\']+\.mp4)["\']', html, re.I)
        for p in pdfs:
            u = p.replace("\n", "").replace("\r", "")
            parts = urllib.parse.urlsplit(u)
            clean_u = urllib.parse.urlunsplit((parts.scheme, parts.netloc, urllib.parse.quote(urllib.parse.unquote(parts.path), safe="/+-.,_()"), parts.query, ""))
            fn = urllib.parse.unquote(parts.path.split("/")[-1]).replace("+", " ")
            dst = os.path.join(docs_dir, fn)
            if not os.path.exists(dst):
                subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", "-o", dst, clean_u], timeout=300)
        for m in mp4s:
            if "body" not in m.lower() and "bwc" not in m.lower():
                continue
            u = m.replace("\n", "").replace("\r", "")
            parts = urllib.parse.urlsplit(u)
            clean_u = urllib.parse.urlunsplit((parts.scheme, parts.netloc, urllib.parse.quote(urllib.parse.unquote(parts.path), safe="/+-.,_()"), parts.query, ""))
            fn = urllib.parse.unquote(parts.path.split("/")[-1]).replace("+", " ")
            dst = os.path.join(vids_dir, fn)
            if not os.path.exists(dst):
                subprocess.run(["aria2c", "-x", "8", "-s", "8", "-d", vids_dir, "-o", fn, clean_u], timeout=1800)
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

    elif ctype == "dropbox_zip":
        tmp_zip = f"/tmp/{cid}.zip"
        subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", "-o", tmp_zip, case["zip_url"]], timeout=1800)
        if os.path.exists(tmp_zip) and zipfile.is_zipfile(tmp_zip):
            with zipfile.ZipFile(tmp_zip, 'r') as zf:
                for member in zf.namelist():
                    if member.endswith("/"): continue
                    base_fn = os.path.basename(member)
                    if not base_fn or BAD_KW.search(base_fn): continue
                    ext = os.path.splitext(base_fn)[1].lower()
                    target_sub = vids_dir if ext in VID_EXTS else docs_dir
                    dst_p = os.path.join(target_sub, base_fn)
                    with zf.open(member) as src, open(dst_p, "wb") as out_f:
                        shutil.copyfileobj(src, out_f)
                    if ext in VID_EXTS:
                        info = probe_video(dst_p)
                        if info:
                            v_cnt += 1
                            tot_dur += info["dur"]
                            tot_sz += os.path.getsize(dst_p)
            os.remove(tmp_zip)
            st[cid]["videos"] = v_cnt
            st[cid]["hours"] = round(tot_dur / 3600, 2)
            st[cid]["size_gb"] = round(tot_sz / (1024**3), 2)
            st[cid]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_status(st)

    st[cid]["state"] = "STAGED_ON_CLOUD"
    st[cid]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_status(st)
    log(f"*** STAGED {cid}: {v_cnt} BWC videos, {tot_dur/3600:.2f} hrs, {tot_sz/(1024**3):.2f} GB ***")
    sync_case_to_drive(case, case_dir, st)

def main():
    for pkg in ["ffmpeg", "aria2", "rclone"]:
        if shutil.which(pkg if pkg != "aria2" else "aria2c") is None:
            subprocess.run("mkdir -p ~/.cloudshell && touch ~/.cloudshell/no-apt-get-warning && sudo apt-get update -qq && sudo apt-get install -y -qq ffmpeg aria2 rclone", shell=True)
            break
    st = load_status()
    for done_id in ["2026_CASE_01", "2026_CASE_02", "2026_CASE_04"]:
        if done_id in st:
            st[done_id]["state"] = "UPLOADED_TO_DRIVE"
    for c in CASES_2026:
        cid = c["case_id"]
        if cid not in st:
            st[cid] = {
                "case_id": cid,
                "tier": c["tier"],
                "folder": c["folder"],
                "expected_hrs": c["expected_hrs"],
                "state": "PENDING",
                "videos": 0,
                "hours": 0.0,
                "size_gb": 0.0
            }
    save_status(st)
    log(f"Starting Headless Cloud Shell 2026 Worker ({len(CASES_2026)} cases)...")
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = [ex.submit(process_case, c, i, st) for i, c in enumerate(CASES_2026)]
        for fut in as_completed(futs):
            try:
                fut.result()
            except Exception as e:
                log(f"Worker error: {e}")

    for _ in range(120):
        pending_sync = [c for c in CASES_2026 if st.get(c["case_id"], {}).get("state") == "STAGED_ON_CLOUD"]
        if not pending_sync:
            break
        if can_write_to_drive():
            for c in pending_sync:
                case_dir = os.path.join(STAGING_ROOT, c["category"], c["folder"])
                if os.path.exists(case_dir):
                    sync_case_to_drive(c, case_dir, st)
        time.sleep(30)

if __name__ == "__main__":
    main()
