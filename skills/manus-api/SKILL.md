---
name: manus-api
description: Manus API v2 integration for agents — auth with x-manus-api-key, task lifecycle, projects, skills, usage, and HTTP MCP bridge pattern. Use for Manus tasks, open.manus.ai, task.create, user.me, manus bridge, or Manus agent automation.
---

# Manus API

Authoritative live docs (prefer over memory):

- Index: https://open.manus.ai/docs/llms.txt
- OpenAPI: https://open.manus.ai/docs/v2/openapi_v2.json
- Auth: https://open.manus.ai/docs/v2/authentication.md

## Authentication

| Header | Value | Use |
|--------|--------|-----|
| `x-manus-api-key` | API key | Own integrations / bridges |
| `Authorization: Bearer {token}` | OAuth2 access token | Open App on behalf of user |

Base URL: `https://api.manus.ai`

Create keys: Manus Developers settings (shown once). Never commit keys. Store encrypted (e.g. Vercel env).

## Core workflow

1. `GET /v2/user.me` — identity (no OAuth scope)
2. `POST /v2/task.create` — body includes `message.content`
3. Poll `GET /v2/task.detail` / `task.listMessages` until terminal
4. Multi-turn: `POST /v2/task.sendMessage`
5. Confirm pending actions: `POST /v2/task.confirmAction`
6. Stop: `POST /v2/task.stop`

## High-value endpoints

```
GET  /v2/user.me
POST /v2/task.create | GET task.list | GET task.detail | POST task.sendMessage
POST /v2/task.confirmAction | POST task.stop | POST task.update | POST task.delete
GET  /v2/task.listMessages
GET  /v2/project.list | POST project.create
GET  /v2/skill.list
GET  /v2/usage.availableCredits | usage.list
POST /v2/file.upload | GET file.detail
POST /v2/webhook.create | GET webhook.list
```

Before inventing request bodies, fetch `https://open.manus.ai/docs/v2/<operation>.md`.

## Operator live bridge (reference)

- Health: `https://manus-mcp-bridge-olive.vercel.app/health`
- MCP: `https://manus-mcp-bridge-olive.vercel.app/mcp`
- Client auth: `Authorization: Bearer $BRIDGE_TOKEN`
- Upstream: bridge injects `x-manus-api-key` from env

## Rules

1. Live docs win over memory.
2. Never put `MANUS_API_KEY` or `BRIDGE_TOKEN` in git, logs, or URLs.
3. Rate limits are per user across keys — cap long research tasks.
4. Prefer allowlisted proxy over open passthrough.
5. On 401 unauthenticated, rotate key; do not reassemble partial keys from chat.
