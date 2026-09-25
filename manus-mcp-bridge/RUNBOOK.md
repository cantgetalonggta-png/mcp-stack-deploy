# Four curls (v1.3.1+)

```bash
curl -sS https://manus-mcp-bridge-olive.vercel.app/health
curl -sS https://manus-mcp-bridge-olive.vercel.app/eval
# finish without token must be 401
curl -sS -o /dev/null -w "%{http_code}\n" https://manus-mcp-bridge-olive.vercel.app/finish
```

Rule: fail any probe → no lead. remaining_creates_scope=instance-best-effort.
