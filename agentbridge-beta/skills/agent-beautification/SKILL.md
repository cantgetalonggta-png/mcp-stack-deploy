---
name: agent-beautification
description: >
  Advanced agent role for AgentBridge upgrade path.
metadata:
  version: "0.5.0"
  product: AgentBridge
---

# agent-beautification

UI beautification: spacing, type, color, motion, a11y, anti-slop.
## Protocol
1. Commit aesthetic before CSS (design token pass)
2. Tailwind utility system; consistent radius/shadow
3. Contrast 4.5:1 body; focus rings; touch targets 44px
4. Avoid AI-slop: no purple-on-white default, no Inter-only, no excessive centered empty
5. Responsive: mobile overflow-x-hidden; break-all on dumps
6. Stack: shadcn/ui + Tailwind v4 + Radix/Base UI a11y


## Cross-links
- agent-upgrader · agent-developer · agent-beautification · code-evolution · deployment-automation
- api-key-management · autoresearch · sensitive-data-defensive-scan
