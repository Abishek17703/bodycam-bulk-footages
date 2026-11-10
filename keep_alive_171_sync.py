import subprocess, base64, time, json, os

HTML_PATH = r"C:\Users\abish\.gemini\antigravity\brain\882b3be2-cdc7-4132-8a3e-0334cc030687\live_2026_dashboard.html"
JSON_PATH = r"c:\Users\abish\Downloads\Nikhil\Bodycam Bulk Footages\status_2026_verified.json"
LOG_PATH = r"c:\Users\abish\Downloads\Nikhil\Bodycam Bulk Footages\worker_2026_progress.log"

def sync_loop():
    while True:
        try:
            tok = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True, shell=True).strip()
            exp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 3300))
            rclone_conf = (
                f'[gdrive2026]\ntype = drive\nscope = drive\ntoken = {{"access_token":"{tok}","token_type":"Bearer","expiry":"{exp}"}}\nroot_folder_id = 19L2kkkiLok94TQhdMQf2v7OEpZrqNVM0\n\n'
                f'[gdrive2026_cases]\ntype = drive\nscope = drive\ntoken = {{"access_token":"{tok}","token_type":"Bearer","expiry":"{exp}"}}\nroot_folder_id = 11REjO5KBB5vWD8C6Xfid7HV1fkpWSBIB\n\n'
                f'[gdrive2026_staging]\ntype = drive\nscope = drive\ntoken = {{"access_token":"{tok}","token_type":"Bearer","expiry":"{exp}"}}\nroot_folder_id = 19L2kkkiLok94TQhdMQf2v7OEpZrqNVM0\n'
            )
            b64 = base64.b64encode(rclone_conf.encode()).decode()
            cmd = (
                f"echo '{b64}' | base64 -d > ~/.config/rclone/rclone.conf && "
                "if ! ps aux | grep -v 'bash -c' | grep -q '[w]orker_171_pure_cloud.py'; then "
                "  nohup python3 -u ~/worker_171_pure_cloud.py >> ~/worker_171_pure.log 2>&1 < /dev/null & "
                "fi && "
                "cat ~/status_171_pure.json 2>/dev/null && echo '===SPLIT===' && tail -n 100 ~/worker_171_pure.log 2>/dev/null"
            )
            out = subprocess.check_output(["gcloud", "cloud-shell", "ssh", "--authorize-session", f"--command={cmd}"], input="y\ny\n", text=True, shell=True, timeout=60)
            if "===SPLIT===" in out:
                idx1 = out.find("{")
                idx2 = out.find("===SPLIT===")
                if idx1 != -1 and idx1 < idx2:
                    j_str = out[idx1:idx2].strip()
                    with open(JSON_PATH, "w", encoding="utf-8") as f:
                        f.write(j_str)
                l_str = out[idx2+len("===SPLIT==="):].strip()
                with open(LOG_PATH, "w", encoding="utf-8") as f:
                    f.write(l_str)
        except Exception:
            pass
        time.sleep(45)

if __name__ == "__main__":
    sync_loop()
