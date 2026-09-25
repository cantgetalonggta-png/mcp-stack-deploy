# Out of Codespace quota — reuse an old/empty one

GitHub API shows **0** Codespaces for this token (create blocked).

## Option A — Existing Codespace on live-online-agent-swarm

```bash
# In the running Codespace terminal:
cd /workspaces/live-online-agent-swarm   # or your path
git pull origin main
bash mcp-stack/scripts/pull-and-run-in-existing-codespace.sh
# Ports → forward 8000 → Private
```

## Option B — Empty Codespace on any of your repos

```bash
git clone https://github.com/cantgetalonggta-png/mcp-stack-deploy.git
cd mcp-stack-deploy
bash scripts/start-bridge.sh
```

## Option C — Vercel (preferred, no Codespace)

1. Re-auth Grok **Vercel** connector for team scope `echo-ec69` / `team_kgQcPVmumwtmK3MdAGlxKJtg`
2. Or in Vercel dashboard: Import `cantgetalonggta-png/mcp-stack-deploy`, root dir `manus-mcp-bridge`
3. Env: `BRIDGE_TOKEN`, `MANUS_API_KEY`
4. Deploy → URL becomes MCP `https://<project>.vercel.app/mcp`

## Option D — Local / WSL (already have agent stacks)

Same as Option B without Codespace.
