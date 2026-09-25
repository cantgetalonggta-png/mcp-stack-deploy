---
name: autoresearch
description: experiment → synthesize → steer via manus_research_steer on AgentBridge. Default dry_run.
---

# Autoresearch on bridge

Tool: manus_research_steer
Phases: experiment | synthesize | steer
Default dry_run true so credits are not spent.
loop_cap 5 then force synthesize.
stop or findings containing stop criterion met freezes create_task.

Always probe /eval and /health first. If pass false, do not open leads.
