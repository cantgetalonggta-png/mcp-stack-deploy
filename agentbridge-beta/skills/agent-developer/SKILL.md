---
name: agent-developer
description: >
  Advanced agent role for AgentBridge upgrade path.
metadata:
  version: "0.5.0"
  product: AgentBridge
---

# agent-developer

Application developer mode: build features, routes, APIs, UI.
## Protocol
1. TypeScript + React + Tailwind (no inline CSS monoliths)
2. Isolated components; Hyperframes stores when available
3. Server proxy for third-party health (CORS)
4. Tests + screenshots before ship
5. Secrets HITL; no baked keys


## Cross-links
- agent-upgrader · agent-developer · agent-beautification · code-evolution · deployment-automation
- api-key-management · autoresearch · sensitive-data-defensive-scan
