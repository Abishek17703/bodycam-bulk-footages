# Bodycam Bulk Footages & Automation Workspace

This repository powers the **Bodycam Bulk Footages** project in **Antigravity Cloud (Remote Agents)**.

## Included Customizations & Skills
- **`.agents/skills/bodycam-low-token-workflow/SKILL.md`**: Low-token workflow skill with pre-stored Google Drive folder IDs, Trello board/list ARIs, and CLI helper instructions.
- **`.agents/skills/bodycam-low-token-workflow/scripts/low_token_ops.py`**: Token-efficient CLI helper (`sheet-summary`, `drive-list`, `url-Probe`, `yt-meta`).
- **`.agents/rules/token-optimization.md`**: Workspace rule enforcing low-token execution.

## Folder Structure
- `scripts/` — Automation scripts for auditing client sheets, probing FOIA portals, packaging raw bodycam deliverables in Google Drive, and syncing Google Docs.
- `docs/` — Reference workflow documents (`snapchat_workflow_doc.md`, `updated_bodycam_doc.md`) and audit manifests.
- `*.json` / `*.csv` / `*.md` — Master case manifests (`master_2026_clean_manifest.json`, `deduplicated_cases_manifest.json`, `portal_backdoor_manifest.json`, etc.).

## Key Cloud Resources
- **Master Google Drive Folder (`BODYCAM AUTOMATION`)**: `1jchXKZ3sNlCuK1MlEEPsQmPdynFN-X1Z`
- **Bodycam Production Doc**: `1NSUwXr2TrMHUxC9d9INt7D8ywqX0TMU8QfQ7wd75VF0`
- **Snapchat Production Doc**: `1xzU3MbBwtzc_sHQETNM-p_SdKtJXvVTu07Aih3JbuNM`
