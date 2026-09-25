# Autoresearch × Manus MCP Bridge

Wire the two-loop engine to the live bridge.

## Loops

| Loop | Tool | Purpose |
|------|------|---------|
| INNER experiment | `manus_research_steer` phase=`experiment` or `manus_task_create` | Run a constrained Manus task against a hypothesis |
| OUTER synthesize | phase=`synthesize` | Pattern extraction from findings |
| STEER | phase=`steer` | Next hypothesis or stop |

## Live endpoints

- Health: `https://manus-mcp-bridge-olive.vercel.app/health`
- MCP: `https://manus-mcp-bridge-olive.vercel.app/mcp`
- Client auth: `Authorization: Bearer $BRIDGE_TOKEN`
- Upstream: `https://api.manus.ai` via `x-manus-api-key`

## Rhythm

1. Bootstrap question in `research-state.yaml`
2. Experiment: create task, record `task_id`
3. Poll `manus_task_detail` until terminal (do not busy-loop; backoff)
4. Write `experiments/{slug}/analysis.md`
5. Every 3–5 experiments: synthesize → update `findings.md` → steer

Do not put keys in git. Prefer public-web / public-record tasks.
