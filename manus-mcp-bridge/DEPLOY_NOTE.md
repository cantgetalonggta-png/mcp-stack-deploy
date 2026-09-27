# manus-mcp-bridge deploy notes

## Warning you saw

```
Due to `builds` existing in your configuration file, the Build and Development
Settings defined in your Project Settings will not apply.
```

**Cause:** Legacy `vercel.json` used `builds` + `routes` (old builder API).

**Fix:** `vercel.json` now uses `rewrites` + `functions` only (no `builds`).

## URLs

| Kind | URL |
|------|-----|
| Deployment you pasted | https://manus-mcp-bridge-mq9c133dh-echo-ec69.vercel.app |
| Latest READY (sha b87b4b…) | https://manus-mcp-bridge-bd1qf2exs-echo-ec69.vercel.app |
| Production alias (if assigned) | set in Vercel → Domains |

## SSO / 302 to vercel.com/login

Deployment Protection is ON. Unauthenticated curl gets 302 → Vercel login.

**To make API public (optional):**
Vercel → Project **manus-mcp-bridge** → Settings → Deployment Protection → disable or allow public for production.

## Wrong-repo ERROR

A deploy of `ma-os-12-console` commit `6616f4ca` hit **manus-mcp-bridge** and failed.
Keep git links separate:

| Vercel project | Git repo | Root Directory |
|----------------|----------|----------------|
| `manus-mcp-bridge` | `cantgetalonggta-png/mcp-stack-deploy` | `manus-mcp-bridge` |
| `ma-os-12-console` | `cantgetalonggta-png/ma-os-12-console` | `.` (repo root) |

## Secrets (vault only — not chat)

In Vercel env for this project only:
- `BRIDGE_TOKEN` (encrypted)
- `MANUS_API_KEY` (encrypted) if you use Manus API
- never commit them
