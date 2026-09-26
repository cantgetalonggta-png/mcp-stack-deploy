---
name: agent-inferencer
description: >
  Advanced agent role for AgentBridge upgrade path.
metadata:
  version: "0.5.0"
  product: AgentBridge
---

# agent-inferencer

Infer next build steps from live chips, debates, Drive distill, imprint scoreboard.
## Protocol
1. Inputs: /health, /eval, stranger_count, proposal JSON, Drive distill
2. Infer: highest leverage next action under legal ceiling
3. Prefer ship-visible deltas over speculative rewrites
4. Output: ranked action list with evidence


## Cross-links
- agent-upgrader · agent-developer · agent-beautification · code-evolution · deployment-automation
- api-key-management · autoresearch · sensitive-data-defensive-scan
