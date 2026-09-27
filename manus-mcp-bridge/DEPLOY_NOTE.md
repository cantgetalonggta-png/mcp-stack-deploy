# manus-mcp-bridge deploy notes

## Required Vercel project wiring (human once)

Project **manus-mcp-bridge** under team **echo-ec69** MUST:

1. Git repository: `cantgetalonggta-png/mcp-stack-deploy` (NOT ma-os-12-console)
2. Root Directory: `manus-mcp-bridge`
3. Deployment Protection → Vercel Authentication: **Off** (public /health /eval)
4. Env (Sensitive as needed):
   - `BRIDGE_TOKEN` (optional; empty = open bridge tools)
   - `MANUS_API_KEY` (optional; without it degrade_label=no_key_local_only)

Wrong-repo deploys from ma-os-12-console pushes will ERROR.

## Public endpoints

- `GET /` — index
- `GET /health` — probe + chip
- `GET /eval` — pass/fail checks
- `GET /research?phase=experiment|synthesize|steer` — autoresearch cycle (dry)
- `GET|POST /mcp` — MCP tool list / dispatch (auth if BRIDGE_TOKEN set)

## Version

1.4.0 — research_steer expanded with experiment → synthesize → steer phases.
