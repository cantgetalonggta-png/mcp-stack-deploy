#!/usr/bin/env python3
"""Public eval gate. Fail deploy if these fail. No secrets."""
import json, urllib.error, urllib.request, sys
BASE = "https://manus-mcp-bridge-olive.vercel.app"
LAND = "https://agentbridge-launch.vercel.app"
results = []

def add(name, ok, detail):
    results.append({"name": name, "ok": bool(ok), "detail": str(detail)[:240]})
    print(("PASS" if ok else "FAIL"), name, detail)

def get(url):
    req = urllib.request.Request(url, headers={"Cache-Control": "no-store"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.status, r.read().decode("utf-8", "replace"), dict(r.headers)

# 1 health
st, body, _ = get(BASE + "/health")
h = json.loads(body)
add("health_200", st == 200, st)
add("version_present", bool(h.get("version")), h.get("version"))
add("user_me_200", h.get("user_me_status") == 200, h.get("user_me_status"))
add("credits_ok", h.get("credits_ok") is True, h.get("credits_ok"))
add("chip_set", h.get("chip") in ("green", "yellow", "red", "gray"), h.get("chip"))
add("tools_free", isinstance(h.get("tools_free"), list) and h["tools_free"], len(h.get("tools_free") or []))
add("tools_paid", isinstance(h.get("tools_paid"), list), h.get("tools_paid"))
# 2 runbook
st, _, _ = get(BASE + "/runbook")
add("runbook_200", st == 200, st)
# 3 finish no auth -> 401
try:
    get(BASE + "/finish")
    add("finish_401", False, "got 200")
except urllib.error.HTTPError as e:
    add("finish_401", e.code == 401, e.code)
# 4 mcp no auth -> 401
try:
    get(BASE + "/mcp")
    add("mcp_401", False, "got 200")
except urllib.error.HTTPError as e:
    add("mcp_401", e.code == 401, e.code)
# 5 landing
st, html, _ = get(LAND + "/")
add("landing_200", st == 200, st)
add("landing_chip_js", "chipText" in html and "ownkeys" in html, "chip+ownkeys")
failed = [r for r in results if not r["ok"]]
open("/tmp/eval-results.json", "w").write(json.dumps({"failed": len(failed), "results": results}, indent=2))
print("FAILED", len(failed), "of", len(results))
sys.exit(1 if failed else 0)
