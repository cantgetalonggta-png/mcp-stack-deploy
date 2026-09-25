---
name: mcp-http-bridge
description: Production HTTP MCP gateway pattern — Bearer client auth, typed tool catalogue, allowlisted upstream proxy, Vercel deploy, health plane. Use when building MCP servers, agent API glue, Claude Cursor Codex bridges, or productizing custom connectors.
---

# MCP HTTP Bridge

Ship a secure HTTP MCP endpoint so Claude, Cursor, Codex, or Grok-compatible clients can call a customer's API without months of glue.

## Architecture

```
MCP Client → Authorization: Bearer BRIDGE_TOKEN
          → GET/POST /mcp (tool list or call)
          → Server injects upstream API key from env
          → Allowlisted upstream (e.g. only /v2/*)
```

## Required components

1. **Auth gate** — missing Bearer → 401; wrong → 403. Optional: no token in pure local dev only.
2. **Tool catalogue** — each tool has `name`, `description`, `inputSchema` (JSON Schema).
3. **First-class tools** — named wrappers for common ops (create, list, detail, stop).
4. **Allowlisted proxy** — reject `..` and non-prefix paths; never open proxy the internet.
5. **Upstream injection** — store real API keys only in encrypted platform env (Vercel encrypted/sensitive).
6. **Health** — `/health` returns version, `*_configured` flags (booleans only), tool name list, unix `ts`.
7. **Deploy** — FastAPI (or equivalent) on Vercel serverless; rootDirectory monorepo pattern; `pip install -r requirements.txt`.
8. **Client pack** — MCP servers JSON snippet for the buyer.

## Minimal client config

```json
{
  "servers": {
    "my-bridge": {
      "type": "http",
      "url": "https://YOUR-BRIDGE.vercel.app/mcp",
      "headers": {
        "Authorization": "Bearer ${BRIDGE_TOKEN}"
      }
    }
  }
}
```

## Security checklist

- [ ] No secrets in git or HTML
- [ ] Keys only in env / secret manager
- [ ] Path allowlist enforced
- [ ] Rate limit plan for multi-tenant (per-token later)
- [ ] Revoke bridge tokens when clients leave

## Deploy notes (operator)

- Repo pattern: `mcp-stack-deploy` / `manus-mcp-bridge`
- GitHub push → Vercel `create_deployment` with `gitSource` + `rootDirectory`
- Omit invalid `vercel.json` keys (e.g. top-level `public`)
- Force new deploy with `forceNew=1` when env changes

## Cross-skill links

- `manus-api` when upstream is Manus
- `api-key-management` for secrets
- `deployment-automation` for release discipline
- `agentbridge-launch` for commercial packaging
