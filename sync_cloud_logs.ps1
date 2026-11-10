while ($true) {
    try {
        $token = (gcloud auth print-access-token).Trim()
        $expiry = (Get-Date).AddMinutes(55).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
        $rcloneConf = "[gdrive2026]`ntype = drive`nscope = drive`ntoken = {`"access_token`":`"$token`",`"token_type`":`"Bearer`",`"expiry`":`"$expiry`"}`nroot_folder_id = 19L2kkkiLok94TQhdMQf2v7OEpZrqNVM0`n`n[gdrive2026_cases]`ntype = drive`nscope = drive`ntoken = {`"access_token`":`"$token`",`"token_type`":`"Bearer`",`"expiry`":`"$expiry`"}`nroot_folder_id = 11REjO5KBB5vWD8C6Xfid7HV1fkpWSBIB`n`n[gdrive2026_staging]`ntype = drive`nscope = drive`ntoken = {`"access_token`":`"$token`",`"token_type`":`"Bearer`",`"expiry`":`"$expiry`"}`nroot_folder_id = 19L2kkkiLok94TQhdMQf2v7OEpZrqNVM0`n"
        $b64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($rcloneConf))
        gcloud cloud-shell ssh --authorize-session --command="echo '$b64' | base64 -d > ~/.config/rclone/rclone.conf && cat ~/worker_2026_progress.log" > "c:\Users\abish\Downloads\Nikhil\Bodycam Bulk Footages\worker_2026_progress.log" 2>$null
        gcloud cloud-shell ssh --authorize-session --command="cat ~/status_2026_verified.json" > "c:\Users\abish\Downloads\Nikhil\Bodycam Bulk Footages\status_2026_verified.json" 2>$null
    } catch {}
    Start-Sleep -Seconds 30
}
