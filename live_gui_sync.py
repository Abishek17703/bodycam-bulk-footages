import subprocess, json, time, os

HTML_PATH = r"C:\Users\abish\.gemini\antigravity\brain\882b3be2-cdc7-4132-8a3e-0334cc030687\live_2026_dashboard.html"
JSON_PATH = r"c:\Users\abish\Downloads\Nikhil\Bodycam Bulk Footages\status_2026_verified.json"
LOG_PATH = r"c:\Users\abish\Downloads\Nikhil\Bodycam Bulk Footages\worker_2026_progress.log"

COPA_CASES = [
    {
        "id": "COPA_055",
        "tier": "Tier 1 (>= 2.0h)",
        "name": "CASE_055 - Chicago PD Brandon Craig Armed Robbery OIS (Mar 9, 2026)",
        "state": "UPLOADED_TO_DRIVE",
        "vids": 42,
        "hrs": 4.85,
        "expHrs": 4.85,
        "gb": 5.12,
        "note": "Verified on Drive (RD #JK175376)"
    },
    {
        "id": "COPA_233",
        "tier": "Tier 1 (>= 2.0h)",
        "name": "CASE_233 - Chicago PD Pierre Davis Log #2026-0000349 OIS (Jan 23, 2026)",
        "state": "UPLOADED_TO_DRIVE",
        "vids": 20,
        "hrs": 3.40,
        "expHrs": 3.40,
        "gb": 2.35,
        "note": "Verified on Drive (RD #JK125616)"
    }
]

def update_once():
    try:
        tok = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True, shell=True).strip()
        exp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 3300))
        rclone_conf = (
            f'[gdrive2026]\ntype = drive\nscope = drive\ntoken = {{"access_token":"{tok}","token_type":"Bearer","expiry":"{exp}"}}\nroot_folder_id = 19L2kkkiLok94TQhdMQf2v7OEpZrqNVM0\n\n'
            f'[gdrive2026_cases]\ntype = drive\nscope = drive\ntoken = {{"access_token":"{tok}","token_type":"Bearer","expiry":"{exp}"}}\nroot_folder_id = 11REjO5KBB5vWD8C6Xfid7HV1fkpWSBIB\n\n'
            f'[gdrive2026_staging]\ntype = drive\nscope = drive\ntoken = {{"access_token":"{tok}","token_type":"Bearer","expiry":"{exp}"}}\nroot_folder_id = 19L2kkkiLok94TQhdMQf2v7OEpZrqNVM0\n'
        )
        import base64
        b64 = base64.b64encode(rclone_conf.encode()).decode()
        cmd = (
            f"echo '{b64}' | base64 -d > ~/.config/rclone/rclone.conf && "
            "if ! pgrep -f worker_171_pure_cloud.py > /dev/null; then "
            "  which rclone > /dev/null || (sudo apt-get update -qq && sudo apt-get install -y -qq aria2 ffmpeg rclone > /dev/null 2>&1); "
            "  nohup python3 -u ~/worker_171_pure_cloud.py >> ~/worker_171_pure.log 2>&1 < /dev/null & "
            "fi && "
            "cat ~/status_171_pure.json && echo '===SPLIT===' && tail -n 80 ~/worker_171_pure.log"
        )
        out = subprocess.check_output(["gcloud", "cloud-shell", "ssh", "--authorize-session", f"--command={cmd}"], input="y\n", text=True, shell=True, timeout=60)
        if "===SPLIT===" not in out:
            return
        idx1 = out.find("{")
        idx2 = out.find("===SPLIT===")
        j_str = out[idx1:idx2].strip()
        l_str = out[idx2+len("===SPLIT==="):].strip()

        with open(JSON_PATH, "w", encoding="utf-8") as f:
            f.write(j_str)
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            f.write(l_str)

        st = json.loads(j_str)
        cases_list = list(COPA_CASES)
        for k, v in st.items():
            state = v.get("state", "PENDING")
            hrs = float(v.get("hours", 0.0))
            exp_hrs = float(v.get("expected_hrs", 1.0))
            vids = int(v.get("videos", 0))
            gb = float(v.get("size_gb", 0.0))
            if state == "UPLOADED_TO_DRIVE":
                note = f"Uploaded at {v.get('uploaded_at', v.get('updated_at', ''))}"
            elif state == "DOWNLOADING":
                note = f"Downloading in Cloud Shell (Updated {v.get('updated_at', '')[-8:]})"
            else:
                note = "Queued"
            cases_list.append({
                "id": k,
                "tier": v.get("tier", ""),
                "name": v.get("folder", k),
                "state": state,
                "vids": vids,
                "hrs": hrs,
                "expHrs": exp_hrs,
                "gb": gb,
                "note": note
            })

        up_cases = [c for c in cases_list if c["state"] == "UPLOADED_TO_DRIVE"]
        dl_cases = [c for c in cases_list if c["state"] == "DOWNLOADING"]
        pd_cases = [c for c in cases_list if c["state"] == "PENDING"]

        up_hrs = sum(c["hrs"] for c in up_cases)
        up_gb = sum(c["gb"] for c in up_cases)
        dl_hrs = sum(c["hrs"] for c in dl_cases)
        total_exp = sum(c["expHrs"] for c in cases_list)
        up_pct = min(100, round((len(up_cases) / len(cases_list)) * 100, 1))
        dl_pct = min(100 - up_pct, round((len(dl_cases) / len(cases_list)) * 100, 1))

        # Deduplicate consecutive identical log lines
        raw_lines = [line.strip() for line in l_str.splitlines() if line.strip()]
        dedup_lines = []
        for line in raw_lines:
            if not dedup_lines or dedup_lines[-1] != line:
                dedup_lines.append(line)
        dedup_lines = dedup_lines[-35:]

        now_str = time.strftime("%H:%M:%S")
        html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="20">
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-3">
  <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-xl p-4 shadow-sm flex flex-col gap-3">
    <div class="flex flex-wrap items-center justify-between gap-2 border-b border-[var(--border)] pb-3">
      <div>
        <div class="flex items-center gap-2">
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <h2 class="text-[var(--foreground)] font-semibold text-base">2026 Bodycam Automation — Cloud Shell Live Monitor</h2>
        </div>
        <p class="text-[var(--muted-foreground)] text-xs mt-0.5">Auto-refreshing every 20s (Last synced: <strong>{now_str}</strong>) • 0 MB Local Internet</p>
      </div>
      <div class="flex items-center gap-2 text-xs">
        <span class="px-2.5 py-1 rounded-md bg-emerald-500/15 text-emerald-400 font-medium border border-emerald-500/30">{len(up_cases)} Uploaded ({up_hrs:.2f}h / {up_gb:.2f} GB)</span>
        <span class="px-2.5 py-1 rounded-md bg-amber-500/15 text-amber-400 font-medium border border-amber-500/30">{len(dl_cases)} Active ({dl_hrs:.2f}h Staged)</span>
        <span class="px-2.5 py-1 rounded-md bg-[var(--secondary)] text-[var(--muted-foreground)] font-medium border border-[var(--border)]">{len(pd_cases)} Pending ({100 - up_pct:.1f}%)</span>
      </div>
    </div>

    <div class="flex flex-col gap-1">
      <div class="flex justify-between text-xs">
        <span class="text-[var(--muted-foreground)] font-medium">Overall 2026 Cases Uploaded: <strong class="text-[var(--foreground)]">{len(up_cases)} / {len(cases_list)} Cases ({up_pct}%)</strong></span>
        <span class="text-[var(--foreground)] font-semibold">{up_hrs:.2f} hrs Uploaded ({up_gb:.2f} GB on Drive)</span>
      </div>
      <div class="w-full h-2.5 bg-[var(--secondary)] rounded-full overflow-hidden flex">
        <div class="bg-emerald-500 h-full transition-all duration-500" style="width: {up_pct}%"></div>
        <div class="bg-amber-500 h-full transition-all duration-500" style="width: {dl_pct}%"></div>
      </div>
    </div>

    <div class="flex items-center justify-between gap-2 pt-1">
      <div class="flex gap-1.5" id="tabs">
        <button onclick="setFilter('ALL')" id="tab-ALL" class="px-3 py-1 rounded-lg text-xs font-medium bg-[var(--primary)] text-[var(--primary-foreground)] transition">All ({len(cases_list)})</button>
        <button onclick="setFilter('UPLOADED_TO_DRIVE')" id="tab-UPLOADED_TO_DRIVE" class="px-3 py-1 rounded-lg text-xs font-medium bg-[var(--secondary)] text-[var(--secondary-foreground)] transition">✅ Uploaded ({len(up_cases)})</button>
        <button onclick="setFilter('DOWNLOADING')" id="tab-DOWNLOADING" class="px-3 py-1 rounded-lg text-xs font-medium bg-[var(--secondary)] text-[var(--secondary-foreground)] transition">⚡ Active ({len(dl_cases)})</button>
        <button onclick="setFilter('PENDING')" id="tab-PENDING" class="px-3 py-1 rounded-lg text-xs font-medium bg-[var(--secondary)] text-[var(--secondary-foreground)] transition">⏳ Pending ({len(pd_cases)})</button>
        <button onclick="setFilter('LOGS')" id="tab-LOGS" class="px-3 py-1 rounded-lg text-xs font-medium bg-[var(--secondary)] text-[var(--secondary-foreground)] transition">🖥 Live Log</button>
      </div>
    </div>

    <div id="cases-container" class="overflow-y-auto max-h-60 border border-[var(--border)] rounded-lg divide-y divide-[var(--border)] bg-[var(--background)]"></div>
    <div id="logs-container" class="hidden overflow-y-auto max-h-60 border border-[var(--border)] rounded-lg bg-black/90 text-emerald-400 font-mono text-xs p-3 space-y-1"></div>
  </div>

  <script>
    const casesData = {json.dumps(cases_list)};
    const logLines = {json.dumps(dedup_lines)};
    let currentFilter = localStorage.getItem('dash2026_tab') || 'ALL';

    function render() {{
      const casesContainer = document.getElementById('cases-container');
      const logsContainer = document.getElementById('logs-container');
      ['ALL', 'DOWNLOADING', 'UPLOADED_TO_DRIVE', 'PENDING', 'LOGS'].forEach(tab => {{
        const btn = document.getElementById('tab-' + tab);
        if (tab === currentFilter) {{
          btn.className = "px-3 py-1 rounded-lg text-xs font-medium bg-[var(--primary)] text-[var(--primary-foreground)] transition";
        }} else {{
          btn.className = "px-3 py-1 rounded-lg text-xs font-medium bg-[var(--secondary)] text-[var(--secondary-foreground)] hover:opacity-90 transition";
        }}
      }});

      if (currentFilter === 'LOGS') {{
        casesContainer.classList.add('hidden');
        logsContainer.classList.remove('hidden');
        logsContainer.innerHTML = logLines.map(l => {{
          let color = "text-emerald-400";
          if (l.includes("DRIVE UPLOAD COMPLETE") || l.includes("STAGED")) color = "text-cyan-300 font-semibold";
          else if (l.includes("Starting")) color = "text-amber-300";
          return `<div class="${{color}}">${{l}}</div>`;
        }}).join('');
        logsContainer.scrollTop = logsContainer.scrollHeight;
        return;
      }}

      logsContainer.classList.add('hidden');
      casesContainer.classList.remove('hidden');
      const filtered = currentFilter === 'ALL' ? casesData : casesData.filter(c => c.state === currentFilter);
      casesContainer.innerHTML = filtered.map(c => {{
        let badge = '';
        let pct = Math.min(100, Math.round((c.hrs / Math.max(0.1, c.expHrs)) * 100));
        if (c.state === 'UPLOADED_TO_DRIVE') {{
          badge = `<span class="px-2 py-0.5 rounded text-xs font-medium bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">✅ Uploaded</span>`;
        }} else if (c.state === 'DOWNLOADING') {{
          badge = `<span class="px-2 py-0.5 rounded text-xs font-medium bg-amber-500/15 text-amber-400 border border-amber-500/30">⚡ Active (${{pct}}%)</span>`;
        }} else {{
          badge = `<span class="px-2 py-0.5 rounded text-xs font-medium bg-[var(--secondary)] text-[var(--muted-foreground)] border border-[var(--border)]">⏳ Queued</span>`;
        }}
        return `
          <div class="p-2.5 flex items-center justify-between gap-3 hover:bg-[var(--secondary)]/40 transition">
            <div class="min-w-0 flex-1">
              <div class="flex items-center gap-2">
                <span class="text-xs font-semibold text-[var(--foreground)] truncate">${{c.name}}</span>
              </div>
              <div class="flex items-center gap-3 mt-1 text-xs text-[var(--muted-foreground)]">
                <span>${{c.tier}}</span>
                <span>•</span>
                <span>${{c.vids}} Videos (${{c.hrs.toFixed(2)}}h / ${{c.expHrs.toFixed(2)}}h)</span>
                <span>•</span>
                <span>${{c.gb.toFixed(2)}} GB</span>
                <span>•</span>
                <span class="text-[var(--foreground)]">${{c.note}}</span>
              </div>
            </div>
            <div class="flex items-center gap-2 shrink-0">${{badge}}</div>
          </div>
        `;
      }}).join('');
    }}

    function setFilter(f) {{
      currentFilter = f;
      localStorage.setItem('dash2026_tab', f);
      render();
    }}
    render();
  </script>
</body>
</html>"""
        with open(HTML_PATH, "w", encoding="utf-8") as f:
            f.write(html)
    except Exception as e:
        pass

if __name__ == "__main__":
    update_once()
    while True:
        time.sleep(20)
        update_once()
