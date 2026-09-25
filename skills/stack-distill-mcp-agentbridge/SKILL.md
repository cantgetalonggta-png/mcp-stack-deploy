---
name: stack-distill-mcp-agentbridge
description: Master distillation of the operator MCP plus AgentBridge stack — connectors, live URLs, skills map, autoresearch loops, deploy state, and monorepo layout. Use for /status, stack recovery, onboarding, or full system orientation after context loss.
---

# Stack Distill — MCP + AgentBridge

Snapshot of the working system as of 2026-09-25. Prefer live health checks over this file when conflicting.

## Live services

| Service | URL / note |
|---------|------------|
| Manus MCP bridge | https://manus-mcp-bridge-olive.vercel.app |
| Bridge health | `/health` → version 1.1.0, 12 tools |
| Bridge MCP | `/mcp` Bearer `BRIDGE_TOKEN` |
| AgentBridge landing | https://agentbridge-launch.vercel.app |
| GitHub monorepo | https://github.com/cantgetalonggta-png/mcp-stack-deploy |
| Manus docs index | https://open.manus.ai/docs/llms.txt |
| Manus API base | https://api.manus.ai |

## Bridge tools (v1.1)

`manus_status`, `manus_user_me`, `manus_task_create`, `manus_task_list`, `manus_task_detail`, `manus_task_send_message`, `manus_task_stop`, `manus_project_list`, `manus_skill_list`, `manus_usage_credits`, `manus_research_steer`, `manus_proxy`

## Auth facts

- Client → bridge: `Authorization: Bearer $BRIDGE_TOKEN`
- Bridge → Manus: `x-manus-api-key: $MANUS_API_KEY`
- Never commit either secret. Vercel encrypted env only.
- Keys pasted in chat should be rotated.

## Connected platforms (operator)

GitHub · Vercel · Voice · Google Drive · HyperFrames · Automations · SUPABASE_SERVICE (MCP tools may not surface)

## Autoresearch mapping

| Loop | Bridge tool |
|------|-------------|
| INNER experiment | `manus_research_steer` phase=`experiment` or `manus_task_create` |
| OUTER synthesize | phase=`synthesize` |
| STEER | phase=`steer` |

## Product SKU #1

**AgentBridge Launch** — custom MCP shop. Pricing $1,499 / $2,499 / $99/mo. Leads = GitHub issues `[lead]`.

## Monorepo layout (key paths)

```
mcp-stack-deploy/
  manus-mcp-bridge/server.py
  agentbridge-site/index.html
  product/
  skills/manus-api/
  .github/ISSUE_TEMPLATE/lead.yml
```

## Distilled skills in this stack

| Skill | Role |
|-------|------|
| `manus-api` | Manus v2 API usage |
| `mcp-http-bridge` | Gateway build pattern |
| `agentbridge-launch` | Commercial SKU + leads |
| `stack-distill-mcp-agentbridge` | This inventory |
| `autoresearch` | Experiment loops |
| `deployment-automation` | Ship/rollback |
| `api-key-management` | Secrets |

## Recovery checklist

1. curl bridge `/health` — expect `version` + tools
2. curl landing — expect AgentBridge HTML
3. Confirm Vercel env `MANUS_API_KEY` + `BRIDGE_TOKEN` set (encrypted)
4. Open leads: issues with `lead` label
5. Do not rebuild from zero if health is green — evolve with `code-evolution`

## Money path (locked)

Build/sell MCP gateways first. Lease explainer and research packs later. No Codespace dependency.
