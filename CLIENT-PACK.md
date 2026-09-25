# Client pack

Orchestrate only with keys you own.

```json
{
  "servers": {
    "agentbridge": {
      "type": "http",
      "url": "https://manus-mcp-bridge-olive.vercel.app/mcp",
      "headers": { "Authorization": "Bearer ${BRIDGE_TOKEN}" }
    }
  }
}
```

Retired: ~~https://YOUR-CODESPACE-8000.app.github.dev/mcp~~

Four curls:
1. GET /health
2. GET /eval  (must pass:true)
3. GET /finish without token → 401
4. dry-run manus_research_steer

Never put MANUS_API_KEY in this file.
