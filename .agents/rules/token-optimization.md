# Workspace Token Optimization Rules

- **Activate `bodycam-low-token-workflow` skill** for Drive, Sheets, Trello, FOIA, or Video Edit-Style tasks instead of re-discovering folder IDs, Trello ARIs, or channel styles.
- **Cap command output to `<50 lines`**: Filter HTML, JSON, and CSV data inside Python before printing to stdout.
- **Write scripts to files** instead of complex inline PowerShell `python -c` commands to avoid escaping errors and retry turns.
- **Inspect videos via 1 contact-sheet image (`tile=4x3` or storyboard `sb1.jpg`)** rather than reading multiple individual frames.
- **Batch all network/Drive/Sheet checks** with `ThreadPoolExecutor` in a single script execution.
- **Keep Trello comments to 2–3 lines max** with no greetings or `@mentions`, and always wait for user confirmation before updating Trello.
