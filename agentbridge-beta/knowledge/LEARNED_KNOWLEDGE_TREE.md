# LEARNED_KNOWLEDGE_TREE — Application Design · Beautification · Dev · Security

Updated: 2026-09-26T03:45:33.952991+00:00
Version: 0.5.0

## 1. Product core (AgentBridge)
- Hose + lock + live user.me (HTTP MCP glue)
- BYO keys; BRIDGE_TOKEN ≠ MANUS_API_KEY
- remaining_creates_scope: instance-best-effort until shared KV
- Imprint taxonomy: ops | stranger | lead (ops never counts as stranger)
- Eval green before promote

## 2. Application developer mode (skills map)
| Need | Skills |
|---|---|
| Architecture / refactor | code-evolution, multi-agent-project-structure, application-development-scope |
| Orchestration | llm-orchestration, multi-agent-patterns, multi-agent-tooling, swarm-agent-framework |
| APIs / keys | api-integration-master, api-key-management, manus-api, manus-api-mcp-bridge, mcp-http-bridge |
| Deploy / CI | deployment-automation, deployment-boundary, metrics-self-healing, directive-yolo-deploy-activation |
| Quality | python-pep8-code-reviewer, final-quality-check, agent-debug, agent-analyzer |
| Code exec | agent-code-execution (sandbox bash/python/node/ffmpeg) |
| Debug multi-agent | directive-grok-4.6-debug-multi-agent, agent-debug, metrics-self-healing |
| Knowledge / RAG | knowledge-base-builder, skill-creator, skill-seekers, skill-distiller |
| Research | autoresearch, research-automation, live-web-mastery, search-techniques-master |
| Security defensive | sensitive-data-defensive-scan, agent-security-defensive, api-key-management, legal-osint-compliance-layer |
| UI / beautify | agent-beautification, agent-layout-design, directive-app-ninja, coherent-communication |
| Advanced agents | agent-upgrader, agent-ontologist, agent-inferencer, agent-analyzer, agent-developer |

## 3. Design & beautification (2026 stack)
- **Default stack:** Tailwind CSS v4 + shadcn/ui (Base UI/Radix a11y) + Lucide icons
- **Alternatives:** HeroUI (React Aria + Tailwind), DaisyUI for fast prototype
- **A11y:** WCAG contrast 4.5:1 body, focus management, keyboard, labels, skip links
- **Anti-slop:** avoid indigo-purple gradients + Inter-only + empty centered hero
- **Commit aesthetic first:** tokens → components → pages
- **Tokens:** bg / surface / raised / fg / muted / accent / ok / warn / bad
- **Motion:** respect prefers-reduced-motion; Sonner toasts; Vaul drawers
- **Responsive:** mobile overflow-x-hidden; pre break-all; 44px touch targets
- **QA:** screenshot desktop + mobile; Vercel-style guideline lint mindset

## 4. Layout systems
- Metric cards grid (auto-fit minmax 200px)
- Probe dump + hunt board side-by-side on desktop
- Nav chips; status chip with live color
- Density: dashboards denser than marketing; launch page airier

## 5. Developer-focused app development
- TypeScript strict; isolated components; no monolithic CSS
- Server functions for third-party (CORS proxy pattern)
- Health/eval chips always no-store
- Preview → production only when eval pass
- Secrets: env only; HITL for paste

## 6. Defensive security (pen-test *mindset*, lawful)
- OWASP Top 10 awareness for our own apps only
- Never open-proxy Manus; allowlist tools
- Scan for leaked keys (sensitive-data-defensive-scan)
- HTTPS, auth boundaries, rate limits
- Quarantine credential-harvest / bypass skill claims (already in drive-distill/QUARANTINE)
- No offensive exploit how-to; defensive findings + fixes only

## 7. Permanent audio rule
- **ALWAYS upload every .mp3 to Google Drive AgentBridge-Audio same turn**
- Folder: https://drive.google.com/drive/folders/1ZxqtwHMdoTT-eAe8jO2XR5nCvvpyDTeb

## 8. Audio uploaded this turn
- helios-zagan-heated-debate.mp3
- helios-zagan-product-discussion.mp3
