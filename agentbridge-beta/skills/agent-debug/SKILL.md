---
name: agent-debug
description: >
  Advanced agent role for AgentBridge upgrade path.
metadata:
  version: "0.5.0"
  product: AgentBridge
---

# agent-debug

Debug multi-agent failures, type errors, deploy flakes, probe yellow/red.
## Protocol
1. Reproduce with live /health /eval
2. Isolate layer: client | server | bridge | connector auth
3. Fix minimal; re-verify chip
4. Log in reports/debug-*.json


## Cross-links
- agent-upgrader · agent-developer · agent-beautification · code-evolution · deployment-automation
- api-key-management · autoresearch · sensitive-data-defensive-scan
