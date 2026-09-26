# Autoresearch × Manus MCP Bridge (Beta expanded)

Live: https://manus-mcp-bridge-olive.vercel.app/mcp
Health: https://manus-mcp-bridge-olive.vercel.app/health
Eval: https://manus-mcp-bridge-olive.vercel.app/eval

## Rhythm (enforced in agents/research/autoresearch_loop.py)

1. **Bootstrap** → research-state.yaml + hypotheses H1–H3
2. **Inner experiment** → protocol.md BEFORE results (git-style lock)
3. **Outer synthesize** → findings.md narrative
4. **Steer** → DEEPEN | BROADEN | PIVOT | CONCLUDE

## Manus tools

- Free: status, user.me, task list/detail/stop, project list, skill list, credits, research_steer, degrade, plan_sequence, proxy
- Paid: task_create, task_send_message (capped)

## Caps

loop_cap=5 · create window 300s · create tries 3 · remaining_creates_scope instance-best-effort

## Auth

`Authorization: Bearer $BRIDGE_TOKEN` · upstream `x-manus-api-key`
