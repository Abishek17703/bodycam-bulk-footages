---
name: bodycam-low-token-workflow
description: >-
  Ultra-low-token workflow for Bodycam Bulk Footages, FOIA harvesting, Google Drive/Sheets
  packaging, Trello task updates, and Snapchat/YouTube edit-style analysis. Use whenever
  auditing case sheets, searching for raw unwatermarked bodycam footage, packaging client
  deliverables in Drive, updating Trello cards on the Nikhil board, or producing/analyzing
  Snapchat and YouTube bodycam videos.
---

# Bodycam Bulk Footages — Max Low-Token Workflow Skill

This skill enforces **minimum token consumption** across all Bodycam, FOIA, Drive, Trello, and Video Production tasks in `c:\Users\abish\Downloads\Nikhil\Bodycam Bulk Footages`.

---

## 1. Core Token-Saving Rules (Mandatory)

1. **Write-Don't-Inline for Multi-Line Python**:
   - Write scripts to a file (`write_file`) or invoke `scripts/low_token_ops.py` rather than passing complex regexes inside PowerShell `python -c "..."` strings (avoids PowerShell quote/bracket escaping errors and wasted retry turns).
2. **Cap All Script Output (`<50 lines`)**:
   - Never print raw HTML, full JSON (`__NEXT_DATA__`), or full transcripts to stdout. Filter in Python and print only compact 1-line summaries per item.
3. **One Contact Sheet Image (`tile=4x3`) Instead of Multiple Frames**:
   - When visually inspecting a video (watermark check, edit-style check, BWC verification), use `YouTube Storyboard (sb1.jpg)` or a single `ffmpeg` tiled grid (`fps=1/4,scale=360:-1,tile=4x3`) so **1 `read_file` image call inspects 12 timestamps at once**.
4. **Parallel Batching via `ThreadPoolExecutor`**:
   - Audit 50+ sheet rows, URLs, or Drive folders in a single multi-threaded Python run rather than sequential tool calls.
5. **Public Sheet Reads via Direct CSV Export**:
   - Read shared Google Sheets via `https://docs.google.com/spreadsheets/d/<SHEET_ID>/export?format=csv` before loading OAuth credentials.
6. **Trello Ultra-Short Format**:
   - Never write greetings (`Hi [Name]`), mentions, or long bullet lists on Trello cards.
   - Wait for user confirmation before calling `trelloWriteCard`.
   - Format comments in 2–3 lines max:
     ```text
     <Count> <Case Type> — all videos verified:
     Folder: https://drive.google.com/drive/folders/<FOLDER_ID>
     Sheet: https://docs.google.com/spreadsheets/d/<SHEET_ID>
     ```

---

## 2. Pre-Indexed IDs & Credentials (Do Not Re-Query)

### Google Drive & OAuth Tokens
- **Master Drive Folder (`BODYCAM AUTOMATION`)**: `1jchXKZ3sNlCuK1MlEEPsQmPdynFN-X1Z`
- **OAuth Tokens** (never use `abishek17703@gmail.com` quota):
  - `tok_bodyacamfootages.json` (`bodyacamfootages@gmail.com`)
  - `tok_bodycamfoia948.json` (`bodycamfoia948@gmail.com`)
- **Delivered Client Packages**:
  - **Aafilas (50 Black Women Cases 2026)**: Folder `1URGt02iopgiAUouU43p4P-7eNzTxbrGq` | Sheet `109KNTvx_BOGpQAo3KodG-eMMRICWQCZNg60xnzbWJ8A`
  - **Jimmy (14 US Homicide/Shooting 10h+ Packages)**: Folder `1imu3lXCXNtSeTRcX-1flu4F-UIVxUal8` | Sheet `1xMUFpZCSO1CcohKegnIvwdkoUW3TbgiXNjZzUnEhN7M`
  - **Risenorth (12 Fraud & Airport Cases)**: Folder `14G14GcLgTwhuoqtO9wrskT46oSis4pyx` | Sheet `1jC640lnQLpra4Syx_iNm3tZtSk3sbYYJTpK9_6tHLrY`
  - **Luke B (10 Direct Raw Bodycam Cases)**: Folder `13_8FcB8M2U0lkK6a6VQmHLotxL9s9hKd` | Manifest Sheet `1-vxBqbvztU5ceKZ5UvsWGBbb2tcuc9SolLgh1mJ8Mrg` | Original Sheet `1_1PYagHnPozitdWG_uKczs5q6BB7HRbPdFUHURJLfZc`
- **Workflow Google Docs**:
  - **Bodycam Video Production Automation**: `1NSUwXr2TrMHUxC9d9INt7D8ywqX0TMU8QfQ7wd75VF0`
  - **Snapchat Video Production Automation**: `1xzU3MbBwtzc_sHQETNM-p_SdKtJXvVTu07Aih3JbuNM`

### Trello Board (`Nikhil`) ARIs
- **Board**: `ari:cloud:trello::board/workspace/648029bc4c724413f9038d78/6aed5e8d614253809d91826c`
- **Lists**:
  - `On priority`: `ari:cloud:trello::list/workspace/648029bc4c724413f9038d78/6aed84c7b578a092793a3b5d`
  - `Today`: `ari:cloud:trello::list/workspace/648029bc4c724413f9038d78/6aed5e9c2ec61861856061e5`
  - `Tomorrow`: `ari:cloud:trello::list/workspace/648029bc4c724413f9038d78/6aed5ea5a1401722bc995dcb`
  - `This week`: `ari:cloud:trello::list/workspace/648029bc4c724413f9038d78/6aed5ea97ec187e04d904b1c`
  - `Later`: `ari:cloud:trello::list/workspace/648029bc4c724413f9038d78/6aed5eb59bbf95f6b30aeb88`
  - `FEEDBACK DISCUSSION`: `ari:cloud:trello::list/workspace/648029bc4c724413f9038d78/6aed8519e100d35144894f8e`
  - `DELIVERED`: `ari:cloud:trello::list/workspace/648029bc4c724413f9038d78/6aed8523629ab0d416c3fdda`
- **Active Open Cards**:
  - `LUKE B`: `ari:cloud:trello::card/workspace/648029bc4c724413f9038d78/6aedd76540f005be08785815`
  - `FOIA AI AGENT IMPLEMENTATION`: `ari:cloud:trello::card/workspace/648029bc4c724413f9038d78/6aedfa78f3a51693a26f5d43`
  - `AI WORKFLOW - SNAPCHAT`: `ari:cloud:trello::card/workspace/648029bc4c724413f9038d78/6aedffb20d9a25d41c322e64`
  - `Ai Workflow Finalisation : Bodycam`: `ari:cloud:trello::card/workspace/648029bc4c724413f9038d78/6aeda69e64e880009360863e`

---

## 3. Pre-Analyzed Video Edit Styles (Do Not Re-Download)

### Snapchat Reference Styles (`AI WORKFLOW - SNAPCHAT`)
1. **`@staycurioustv` (Vertical Show Episode — `3–5 min`, `9:16`)**:
   - **Structure**: Multi-subject chapter format (`One Hit Wonders, Where Are They Now?`).
   - **Visuals**: Freeze-frame subject intro with giant bold **cyan/teal uppercase title** (`GOTYE`) + camera-shutter/paper-rip wipe transition; cuts every `1.5–2.5s` with continuous `100%→112%` slow zoom.
   - **Subtitles**: Small single-line white sans-serif (`Inter/Helvetica Bold`, thin black outline) at lower-middle (`3–5 words` per line).
   - **Audio**: Continuous fast-paced narrator voiceover with ducked music/clip audio.
2. **`@t.fugitive` (Snapchat Spotlight Viral Clip — `30–60s`, `9:16`)**:
   - **Structure**: Zero-intro hook starting at `0.0s` right in the action.
   - **Subtitles**: All-caps **Comic/Burbank bold** in **Yellow (`#FFE600`) / White / Green** with thick `3–4px` black stroke placed dead-center, color-coded by speaker.
   - **Audio**: Original clip audio upfront + subtle background bed + hard jump-cuts removing pauses `>0.5s`.

### YouTube Bodycam Reference Styles (`Ai Workflow Finalisation : Bodycam`)
1. **`@DrInsanityCrime` (`35–57m` Long-form True Crime / Interrogation)**:
   - **Hook**: `0:00–0:35` tense interrogation/BWC exchange → deep narrator hook.
   - **Visuals**: Dark blue/black 3D particle wave canvas for 911/audio calls, floating 3D evidence cards (missing posters, detective badges), teal subject lower-thirds (`Name, Age`), bottom-left date/place stamp, white/cyan captions inside a solid black box.
2. **`@CodeBlueCam` (`15–25m` Mid-form BWC + `30–60s` Shorts)**:
   - **Hook**: `0:00–0:20` rapid action montage → **3D Google Earth satellite fly-in** with glowing red/blue radar dots.
   - **Visuals**: Red tactical HUD tracking boxes (`130 MPH`), circular spotlight dimmers on distant suspects, top-left officer camera tag (`Deputy Royston`), semi-transparent black pill captions color-coded by speaker (White=Officer, Red/Yellow=Suspect, Cyan=Dispatch). Shorts use `9:16` center-crop over blurred background with narrator setup.
3. **`@MidwestSafety` (`18–35m` Mid-form BWC + `15–45s` Shorts)**:
   - **Hook**: Immediate narrator + on-screen callout at `0.0s` (no raw cold open) with animated **red arrow + uppercase label (`BACKS UP INTO TREE`)**.
   - **Visuals**: Top-left blue pill (`OFFICER #1`) and map pin (`📍 City, State`), two-tone box subtitles (white text with **bold red action keywords**). Shorts pin a permanent **red banner headline** at the top third (`Referee attacks player`) for the entire clip.
4. **`@redfilechannel` (`25–48m` Psychological Interrogation / BWC)**:
   - **Hook**: Plays suspect's 911 call / excuse first (`0:00–0:30`), then narrator exposes how digital/forensic evidence contradicts their story.
   - **Visuals**: Dark 3D isometric building/crime-scene render with left/right caller-dispatcher portraits connected by a live cyan/white audio waveform and floating transcript text; red circular callouts on weapons/holsters; top-left red `RED FILE` watermark.

---

## 4. Helper Script (`scripts/low_token_ops.py`)

Run single-command low-token operations via:
```powershell
python ".agents/skills/bodycam-low-token-workflow/scripts/low_token_ops.py" <subcommand> [args]
```
Subcommands:
- `sheet-csv <sheet_id>`: Prints compact row summary of any public Google Sheet.
- `audit-sheet-videos <sheet_id>`: Concurrently scans all article URLs in a Google Sheet for direct `.mp4`, `.m3u8`, Wikimedia, or YouTube embeds.
- `yt-check <video_id_or_query>`: Checks YouTube video metadata / oEmbed author / storyboard availability with zero bloat.
- `video-grid <mp4_path> <out_jpg>`: Generates a single `4x3` contact sheet image (`tile=4x3`) for 1-call visual inspection.
