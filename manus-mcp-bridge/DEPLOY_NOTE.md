# mcp-http-bridge / manus-mcp-bridge v1.5.0

- Root directories that work: `mcp-http-bridge` OR `manus-mcp-bridge` (identical content).
- Autoresearch: experiment → synthesize → steer (dry-run default).
- Endpoints: `/health` `/eval` `/research` `/mcp`
- Vercel project `manus-mcp-bridge` should set **Root Directory** to `mcp-http-bridge` if linked to ma-os-12-console, or `manus-mcp-bridge` on mcp-stack-deploy.
- Authentication: set `ssoProtection: null` in project settings UI if API 403.
