# mcp-stack-deploy

Automated MCP stack for **cantgetalonggta-png**:

- GitHub Copilot MCP (`https://api.githubcopilot.com/mcp/`)
- Manus HTTP MCP bridge (Codespaces-ready)
- Supabase MCP URL template
- System status publication (refs 1–8)

**No secrets in this repository.** Use GitHub Codespaces secrets.

## Quick start (Codespace)

1. Open this repo → **Code** → **Codespaces** → Create codespace on `main`
2. Repo **Settings → Secrets and variables → Codespaces** add:
   - `MANUS_API_KEY`
   - `BRIDGE_TOKEN` (or let start script generate ephemeral)
3. Bridge listens on port **8000**. In **Ports** panel set visibility (Private recommended).
4. Copy the forwarded URL, e.g. `https://<name>-8000.app.github.dev`
5. Point client MCP config at `https://<name>-8000.app.github.dev/mcp` with  
   `Authorization: Bearer <BRIDGE_TOKEN>`

## Local run

```bash
cd manus-mcp-bridge
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export BRIDGE_TOKEN=... MANUS_API_KEY=...
python server.py
```

Health: `curl -s http://localhost:8000/health`

## Client configs

| File | Client |
|------|--------|
| `mcp.servers.json` | Generic / Grok-adjacent publish |
| `.cursor/mcp.json` | Cursor |

## Vercel projects linked to this account

- `ma-os-12-console` (`prj_Ozz5MVxosia5r1JLxa5ah8Lb4ZV7`)
- `strand-osint-mesh` (`prj_LjAxbC9jdFsKAoRBVVcJeKcY0Yx5`)

## What only you can do (cannot be fully automated from Grok)

1. Paste real Codespace URL into client MCP config
2. Add Codespace secrets in GitHub UI
3. Re-auth Grok **Supabase** connector if tools still do not appear
4. Confirm Manus API base URL if different from default

## Deployed by

Grok agent automation · 2026-09-25
