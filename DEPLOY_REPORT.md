# Deploy report — automated

| Item | Result |
|------|--------|
| GitHub user | `cantgetalonggta-png` |
| New repo | https://github.com/cantgetalonggta-png/mcp-stack-deploy |
| Manus bridge | `manus-mcp-bridge/server.py` (FastAPI, `/mcp`, `/health`) |
| Devcontainer | Yes — port 8000, postStart starts bridge |
| MCP JSON | `mcp.servers.json` + `.cursor/mcp.json` |
| Status publish | `docs/SYSTEM_STATUS_PUBLISHED.md` |
| Secrets in git | **None** |
| Supabase Grok tools | Still not exposed via connector search (native re-auth still needed in Grok UI) |
| Manus live URL | Unknown until Codespace runs + port forward |

## Blocked only on human confirm (if needed)

- Codespace secrets `MANUS_API_KEY` / `BRIDGE_TOKEN` values (must stay in GitHub secret store)
- Real `project_ref` for Supabase MCP query string
- Optional: whether Manus API base is not `https://api.manus.im`

Everything else is committed and ready to open as Codespace.
