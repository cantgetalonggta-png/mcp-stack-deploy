# Encyclopedia: agent-security-defensive

Defensive app security for AgentBridge (lawful, defensive only).
## Protocol
1. OWASP-aligned: no secrets in client, CSP-friendly, HTTPS only
2. Bridge: BRIDGE_TOKEN ≠ MANUS_API_KEY; allowlist tools
3. Auth: Supabase session; never paste operator keys into agents
4. Sensitive-data-defensive-scan before push
5. Rate limits; no open proxy to arbitrary upstreams
6. Document findings; no offensive exploit how-to

