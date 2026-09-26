---
name: agent-code-execution
description: >
  Advanced agent role for AgentBridge upgrade path.
metadata:
  version: "0.5.0"
  product: AgentBridge
---

# agent-code-execution

Safe code execution patterns in sandbox: bash, python, node, ffmpeg.
## Protocol
1. Prefer sandbox under /workspace/artifacts
2. Timeouts; no secret print
3. Capture stdout; write artifacts
4. Never execute quarantined credential/bypass packages


## Cross-links
- agent-upgrader · agent-developer · agent-beautification · code-evolution · deployment-automation
- api-key-management · autoresearch · sensitive-data-defensive-scan
