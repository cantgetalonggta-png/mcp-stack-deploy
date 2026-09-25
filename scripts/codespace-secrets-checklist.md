# Codespace secrets (set in GitHub repo → Settings → Secrets and variables → Codespaces)

| Name | Required | Purpose |
|------|----------|---------|
| `MANUS_API_KEY` | Yes for upstream | Manus API authentication |
| `BRIDGE_TOKEN` | Strongly recommended | Clients → bridge Bearer token |
| `SUPABASE_ACCESS_TOKEN` | Optional | If using Supabase MCP outside Grok |
| `SUPABASE_PROJECT_REF` | Optional | project_ref for MCP URL |

Never commit values. After adding secrets, rebuild/restart Codespace.
