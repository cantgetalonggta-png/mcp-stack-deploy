---
name: manus-api
description: Official-aligned Manus API v2 integration for Grok — auth, tasks, projects, skills, webhooks, files, usage. Uses live docs at open.manus.ai and the deployed manus-mcp-bridge on Vercel. Triggers on Manus API, task.create, manus skill, open.manus.ai, x-manus-api-key, manus bridge.
---

# Manus API skill (Grok)

Authoritative docs (always prefer live pages over memory):

- Index: https://open.manus.ai/docs/llms.txt
- OpenAPI: https://open.manus.ai/docs/v2/openapi_v2.json
- Auth: https://open.manus.ai/docs/v2/authentication.md
- Official skill install (Codex etc.): `npx skills add https://open.manus.ai/docs`

## Authentication

| Header | Value | Use |
|--------|--------|-----|
| `x-manus-api-key` | API key | Own integrations / this bridge |
| `Authorization: Bearer {token}` | OAuth2 access token | Open App / third-party on behalf of user |

Base URL: **`https://api.manus.ai`**

Create keys: https://manus.im/app#settings/developers (shown once; store in secrets only).

## Deployed bridge (this account)

| Item | Value |
|------|--------|
| MCP URL | `https://manus-mcp-bridge-olive.vercel.app/mcp` |
| Health | `https://manus-mcp-bridge-olive.vercel.app/health` |
| Client auth | `Authorization: Bearer $BRIDGE_TOKEN` (Vercel env) |
| Upstream | Bridge injects `x-manus-api-key` from `MANUS_API_KEY` |
| Repo | https://github.com/cantgetalonggta-png/mcp-stack-deploy |

Do **not** commit API keys. Prefer Vercel encrypted env / Codespace secrets.

## Core workflow

1. **Identity** — `GET /v2/user.me` (no OAuth scope required)
2. **Create task** — `POST /v2/task.create` with `message.content`
3. **Poll** — `GET /v2/task.detail` / `task.list` until terminal status (see task-lifecycle.md)
4. **Confirm actions** — `POST /v2/task.confirmAction` when agent needs approval
5. **Multi-turn** — `POST /v2/task.sendMessage`
6. **Stop** — `POST /v2/task.stop`

## Endpoint map (v2 OpenAPI)

```
GET  /v2/user.me
POST /v2/task.create | GET task.list | GET task.detail | POST task.sendMessage
POST /v2/task.confirmAction | POST task.stop | POST task.update | POST task.delete
GET  /v2/task.listMessages
GET  /v2/project.list | POST project.create
GET  /v2/skill.list
GET  /v2/agent.list | GET agent.detail | POST agent.update
POST /v2/file.upload | GET file.detail | POST file.delete
POST /v2/webhook.create | GET webhook.list | POST webhook.delete | GET webhook.publicKey
GET  /v2/usage.availableCredits | usage.list | usage.teamLog | usage.teamStatistic
GET  /v2/connector.list | browser.onlineList
GET  /v2/website.status | website.listCheckpoints | POST website.publish | website.update
```

Before generating request bodies, fetch the matching `https://open.manus.ai/docs/v2/<operation>.md` page or OpenAPI path schema.

## Minimal cURL patterns

```bash
# Who am I
curl -s -H "x-manus-api-key: $MANUS_API_KEY" \
  https://api.manus.ai/v2/user.me

# Create task
curl -s -X POST https://api.manus.ai/v2/task.create \
  -H "Content-Type: application/json" \
  -H "x-manus-api-key: $MANUS_API_KEY" \
  -d '{"message":{"content":"hello"}}'

# Via bridge (client token)
curl -s -X POST https://manus-mcp-bridge-olive.vercel.app/mcp \
  -H "Authorization: Bearer $BRIDGE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"manus_status"}'
```

## Agent rules

1. Treat live Manus docs + OpenAPI as source of truth; re-fetch when unsure.
2. Never put `MANUS_API_KEY` or `BRIDGE_TOKEN` in git, logs, or user-facing URLs.
3. Prefer the Vercel bridge for MCP clients; call `api.manus.ai` directly only when the bridge is insufficient.
4. On `401 unauthenticated`, rotate key in Developers settings and update Vercel env — do not guess joins of partial keys.
5. Rate limits are **per user** across all keys — see rate-limits.md.
6. When expanding the bridge, expose thin proxies to `task.create`, `task.list`, `task.detail`, `project.list`, `skill.list` first.

## Codex / Skills CLI (optional)

```bash
npx skills add https://open.manus.ai/docs
npx skills add https://open.manus.ai/docs --skill manus-api --agent codex --global --yes
npx skills update manus-api
```

Inside Manus webapp: `/manus-api` invokes the same official guidance.

## Related operator assets

- `mcp-stack-deploy` · `live-online-agent-swarm/mcp-stack/`
- Ops skills: api-integration-master · api-key-management · deployment-automation
