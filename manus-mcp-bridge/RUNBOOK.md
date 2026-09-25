# Four-curl runbook (generated contract)

1. `curl -sS https://manus-mcp-bridge-olive.vercel.app/health`
2. Confirm `user_me_status` is 200 and `chip` is green.
3. Confirm `credits_ok` true.
4. Dry-run steer: POST /mcp `manus_research_steer` with `dry_run=true`.

If any fail, do not open a lead. Health is no-store. Gray chip means unknown, never fake green.
