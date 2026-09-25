# Client pack

Orchestrate only with keys you own. Theft is not a feature.

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

Retired (do not use):

~~`https://YOUR-CODESPACE-8000.app.github.dev/mcp`~~ — Codespace hostage. Quota and idle timeout kill the URL.

Never put `MANUS_API_KEY` in this file. Bridge token only.

Four curls: `/health` → `user_me_status==200` → `credits_ok` → dry-run `manus_research_steer`.
