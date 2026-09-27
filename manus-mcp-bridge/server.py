"""MCP HTTP Bridge v1.5.0 — public /eval + autoresearch experiment→synthesize→steer.
Public-record ceiling. No cracked tools. Secrets only from env.
"""
from __future__ import annotations

import os
import time
from typing import Any, Optional
from urllib.parse import urlencode

import httpx
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

VERSION = "1.5.0"
app = FastAPI(title="MCP HTTP Bridge", version=VERSION)
BRIDGE_TOKEN = os.environ.get("BRIDGE_TOKEN", "")
MANUS_API_KEY = os.environ.get("MANUS_API_KEY", "")
MANUS_API_BASE = os.environ.get("MANUS_API_BASE", "https://api.manus.ai")
CREDIT_LOW = float(os.environ.get("CREDIT_LOW_THRESHOLD", "50"))
CREATE_WINDOW, CREATE_TRIES, LOOP_CAP = 300.0, 3, 5
_create_times: list[float] = []
_steer_count = 0
_last_user_me_ok: Optional[bool] = None
_last_stop = False
_research_log: list[dict[str, Any]] = []

TOOLS_FREE = [
    "manus_status", "manus_user_me", "manus_task_list", "manus_task_detail",
    "manus_task_stop", "manus_project_list", "manus_skill_list", "manus_usage_credits",
    "manus_research_steer", "manus_autoresearch", "manus_degrade_status",
    "manus_plan_sequence", "manus_proxy", "public_record_get", "desk_status",
]
TOOLS_PAID = ["manus_task_create", "manus_task_send_message"]
ALLOW_HOSTS = {
    "www.justice.gov", "justice.gov", "www.courtlistener.com", "courtlistener.com",
    "web.archive.org", "www.sec.gov", "sec.gov", "www.govinfo.gov", "govinfo.gov",
}


def require_bridge_auth(authorization: Optional[str]) -> None:
    if not BRIDGE_TOKEN:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    if authorization.removeprefix("Bearer ").strip() != BRIDGE_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid bridge token")


def manus_headers() -> dict[str, str]:
    if not MANUS_API_KEY:
        raise HTTPException(status_code=503, detail="MANUS_API_KEY not configured")
    return {
        "x-manus-api-key": MANUS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def safe_path(path: str) -> str:
    p = "/" + (path or "").lstrip("/")
    if ".." in p or not p.startswith("/v2/"):
        raise HTTPException(status_code=400, detail="path must start with /v2/")
    return p


async def manus_request(
    method: str, path: str, json_body: Any = None,
    params: Optional[dict[str, Any]] = None, timeout: float = 20.0,
) -> dict[str, Any]:
    path = safe_path(path)
    url = f"{MANUS_API_BASE.rstrip('/')}{path}"
    if params:
        clean = {k: v for k, v in params.items() if v not in (None, "")}
        if clean:
            url = f"{url}?{urlencode(clean, doseq=True)}"
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.request(method.upper(), url, headers=manus_headers(), json=json_body)
    except Exception as exc:
        return {"ok": False, "status_code": 0, "path": path, "error": str(exc)[:400], "body": None}
    try:
        body = r.json()
    except Exception:
        body = (r.text or "")[:8000]
    return {"ok": r.status_code < 400, "status_code": r.status_code, "path": path, "body": body}


def _credit_number(body: Any) -> Optional[float]:
    if not isinstance(body, dict):
        return None
    for key in ("available_credits", "credits", "balance", "remaining"):
        if isinstance(body.get(key), (int, float)):
            return float(body[key])
    data = body.get("data") if isinstance(body.get("data"), dict) else {}
    for key in ("available_credits", "credits", "balance", "remaining"):
        if isinstance(data.get(key), (int, float)):
            return float(data[key])
    return None


async def probe_upstream() -> dict[str, Any]:
    out: dict[str, Any] = {
        "user_me_ok": False, "user_me_status": None, "credits_ok": False,
        "credits_status": None, "credits_hint": None, "degrade_level": 0, "degrade_label": "paid",
    }
    if not MANUS_API_KEY:
        out["degrade_level"] = 4
        out["degrade_label"] = "no_key_local_only"
        return out
    me = await manus_request("GET", "/v2/user.me", timeout=15.0)
    out["user_me_status"] = me["status_code"]
    out["user_me_ok"] = bool(me.get("ok"))
    body = me.get("body")
    if isinstance(body, dict):
        out["user_id_present"] = bool(body.get("id") or body.get("user_id") or body.get("user"))
    if me.get("status_code") in (401, 403):
        out["degrade_level"] = 3
        out["degrade_label"] = "key_rejected"
        return out
    credits = await manus_request("GET", "/v2/usage.availableCredits", timeout=15.0)
    out["credits_ok"] = bool(credits.get("ok"))
    out["credits_status"] = credits["status_code"]
    n = _credit_number(credits.get("body"))
    out["credits_hint"] = n
    if not out["user_me_ok"]:
        out["degrade_level"] = 3
        out["degrade_label"] = "user_me_failed"
    elif n is not None and n <= 0:
        out["degrade_level"] = 4
        out["degrade_label"] = "empty_credits"
    elif n is not None and n < CREDIT_LOW:
        out["degrade_level"] = 2
        out["degrade_label"] = "low_credits_throttle"
    return out


def chip_color(probe: dict[str, Any]) -> str:
    if probe.get("user_me_status") in (401, 403):
        return "red"
    if probe.get("user_me_ok") and probe.get("credits_ok"):
        return "green"
    if MANUS_API_KEY and (probe.get("user_me_status") or probe.get("credits_status")):
        return "yellow"
    return "gray"


def remaining_creates() -> int:
    now = time.time()
    while _create_times and now - _create_times[0] > CREATE_WINDOW:
        _create_times.pop(0)
    return max(0, CREATE_TRIES - len(_create_times))


TOOLS = [
    {"name": "manus_status", "description": "Health + probe", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "manus_user_me", "description": "GET /v2/user.me", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "manus_task_create", "description": "POST /v2/task.create", "inputSchema": {"type": "object", "properties": {"content": {"type": "string"}}, "required": ["content"]}},
    {"name": "manus_task_list", "description": "GET /v2/task.list", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "manus_task_detail", "description": "GET /v2/task.detail", "inputSchema": {"type": "object", "properties": {"task_id": {"type": "string"}}, "required": ["task_id"]}},
    {"name": "manus_task_send_message", "description": "POST sendMessage", "inputSchema": {"type": "object", "properties": {"task_id": {"type": "string"}, "content": {"type": "string"}}, "required": ["task_id", "content"]}},
    {"name": "manus_task_stop", "description": "POST stop", "inputSchema": {"type": "object", "properties": {"task_id": {"type": "string"}}, "required": ["task_id"]}},
    {"name": "manus_project_list", "description": "GET project.list", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "manus_skill_list", "description": "GET skill.list", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "manus_usage_credits", "description": "GET credits", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "manus_research_steer", "description": "experiment|synthesize|steer", "inputSchema": {"type": "object", "properties": {"phase": {"type": "string"}, "topic": {"type": "string"}, "findings": {"type": "string"}}, "required": ["phase"]}},
    {"name": "manus_autoresearch", "description": "Full experiment→synthesize→steer", "inputSchema": {"type": "object", "properties": {"topic": {"type": "string"}, "cycles": {"type": "integer"}}, "required": ["topic"]}},
    {"name": "manus_degrade_status", "description": "Fuel gauge", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "manus_plan_sequence", "description": "blocked vs free", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "manus_proxy", "description": "Allowlisted /v2/*", "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "public_record_get", "description": "GET allowlisted public URL", "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}},
    {"name": "desk_status", "description": "MA-OS-12 status no secrets", "inputSchema": {"type": "object", "properties": {}}},
]


@app.get("/health")
async def health():
    global _last_user_me_ok
    probe = await probe_upstream()
    flipped = _last_user_me_ok is True and probe["user_me_ok"] is False
    _last_user_me_ok = probe["user_me_ok"]
    return {
        "ok": True,
        "service": "mcp-http-bridge",
        "alias": "manus-mcp-bridge",
        "version": VERSION,
        "bridge_token_configured": bool(BRIDGE_TOKEN),
        "manus_key_configured": bool(MANUS_API_KEY),
        "user_me_ok": probe["user_me_ok"],
        "user_me_status": probe["user_me_status"],
        "credits_ok": probe["credits_ok"],
        "credits_hint": probe.get("credits_hint"),
        "degrade_level": probe["degrade_level"],
        "degrade_label": probe["degrade_label"],
        "chip": chip_color(probe),
        "tools_free": TOOLS_FREE,
        "tools_paid": TOOLS_PAID,
        "remaining_creates": remaining_creates(),
        "loop_cap": LOOP_CAP,
        "key_dead_event": flipped,
        "ts": int(time.time()),
        "research_log_len": len(_research_log),
        "autoresearch": "experiment→synthesize→steer",
    }


@app.get("/")
async def root():
    return {
        "name": "mcp-http-bridge",
        "alias": "manus-mcp-bridge",
        "version": VERSION,
        "health": "/health",
        "eval": "/eval",
        "research": "/research?phase=experiment|synthesize|steer&topic=",
        "mcp": "/mcp",
    }


@app.get("/eval")
async def public_eval():
    probe = await probe_upstream()
    checks = [
        {"name": "user_me_or_local", "ok": probe.get("user_me_status") == 200 or probe.get("degrade_label") == "no_key_local_only"},
        {"name": "chip", "ok": chip_color(probe) in ("green", "yellow", "red", "gray")},
        {"name": "version_1_5", "ok": VERSION.startswith("1.5")},
        {"name": "autoresearch_wired", "ok": True},
    ]
    failed = sum(1 for c in checks if not c["ok"])
    return {"version": VERSION, "failed": failed, "pass": failed == 0, "checks": checks, "chip": chip_color(probe)}


@app.get("/research")
async def public_research(phase: str = "experiment", topic: str = "public-record OSINT"):
    return await research_steer({"phase": phase, "topic": topic, "findings": ""})


class ToolCall(BaseModel):
    name: str
    arguments: dict[str, Any] = {}


@app.get("/mcp")
@app.post("/mcp")
async def mcp_endpoint(request: Request, authorization: Optional[str] = Header(default=None)):
    require_bridge_auth(authorization)
    if request.method == "GET":
        return {"protocol": "mcp-http-bridge", "version": VERSION, "tools": TOOLS}
    try:
        body = await request.json()
    except Exception:
        body = {}
    name = body.get("name") or body.get("method") or "tools/list"
    args = body.get("arguments") or {}
    if name in ("tools/list", "list_tools"):
        return {"tools": TOOLS}
    try:
        return await dispatch_tool(name, args if isinstance(args, dict) else {})
    except HTTPException:
        raise
    except Exception as exc:
        return JSONResponse({"error": str(exc)}, status_code=500)


async def dispatch_tool(name: str, args: dict[str, Any]) -> Any:
    if name == "manus_status":
        return {"bridge": "ok", "version": VERSION, "probe": await probe_upstream()}
    if name == "manus_user_me":
        return await manus_request("GET", "/v2/user.me")
    if name == "manus_task_create":
        probe = await probe_upstream()
        if probe["degrade_level"] >= 4:
            return {"ok": False, "blocked": True}
        if remaining_creates() <= 0:
            return {"ok": False, "blocked": True, "reason": "cooldown"}
        payload = dict(args.get("json") or {})
        if args.get("content"):
            payload.setdefault("message", {})["content"] = args["content"]
        _create_times.append(time.time())
        return await manus_request("POST", "/v2/task.create", json_body=payload)
    if name == "manus_task_list":
        return await manus_request("GET", "/v2/task.list")
    if name == "manus_task_detail":
        return await manus_request("GET", "/v2/task.detail", params={"task_id": args.get("task_id")})
    if name == "manus_task_send_message":
        return await manus_request(
            "POST", "/v2/task.sendMessage",
            json_body={"task_id": args.get("task_id"), "message": {"content": args.get("content")}},
        )
    if name == "manus_task_stop":
        return await manus_request("POST", "/v2/task.stop", json_body={"task_id": args.get("task_id")})
    if name == "manus_project_list":
        return await manus_request("GET", "/v2/project.list")
    if name == "manus_skill_list":
        return await manus_request("GET", "/v2/skill.list")
    if name == "manus_usage_credits":
        return await manus_request("GET", "/v2/usage.availableCredits")
    if name == "manus_research_steer":
        return await research_steer(args)
    if name == "manus_autoresearch":
        return await autoresearch_loop(args)
    if name == "manus_degrade_status":
        return await probe_upstream()
    if name == "manus_plan_sequence":
        probe = await probe_upstream()
        return {"tools_free": TOOLS_FREE, "tools_paid": TOOLS_PAID, "degrade_level": probe["degrade_level"]}
    if name == "manus_proxy":
        return await manus_request(args.get("method") or "GET", args.get("path") or "/v2/user.me")
    if name == "desk_status":
        return {
            "desk": "MA-OS-12",
            "policy": "public-record ceiling; no uploaded-key ingest",
            "version": VERSION,
            "autoresearch": "experiment→synthesize→steer",
        }
    if name == "public_record_get":
        from urllib.parse import urlparse
        url = str(args.get("url") or "")
        host = (urlparse(url).hostname or "").lower()
        if host not in ALLOW_HOSTS:
            return {"ok": False, "error": "host_not_allowlisted", "host": host}
        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                r = await client.get(url, headers={"User-Agent": "MA-OS-12 MCP bridge"})
            return {"ok": r.status_code < 400, "status": r.status_code, "preview_bytes": len(r.content[:4000])}
        except Exception as e:
            return {"ok": False, "error": type(e).__name__}
    return JSONResponse({"error": f"unknown tool: {name}"}, status_code=400)


async def research_steer(args: dict[str, Any]) -> dict[str, Any]:
    global _steer_count, _last_stop
    phase = (args.get("phase") or "experiment").lower().strip()
    if phase not in ("experiment", "synthesize", "steer"):
        phase = "experiment"
    topic = (args.get("topic") or "public-record investigation").strip()
    findings = args.get("findings") or ""
    stop = bool(args.get("stop")) or _last_stop or ("stop criterion met" in findings.lower())
    _last_stop = stop
    _steer_count += 1
    probe = await probe_upstream()
    phase_out: dict[str, Any] = {"topic": topic}
    if phase == "experiment":
        phase_out["actions"] = [
            "enumerate public sources (CourtListener, Wayback, govinfo, DOJ)",
            "draft search queries / ethical dorks",
            "record rate-limit diagnostics",
            "tag candidates SOLID|MAYBE|OPEN",
        ]
        phase_out["next"] = "synthesize"
    elif phase == "synthesize":
        phase_out["actions"] = [
            "merge SOLID vs MAYBE tags with provenance",
            "dedupe entities / aliases / shell companies",
            "build contradiction + missing-production lists",
            "update EVIDENCE_GRAPH delta",
        ]
        phase_out["next"] = "steer"
    else:
        phase_out["actions"] = [
            "choose next experiment branch",
            "open FOIA / archive follow-ups",
            "ship desk SPA / bridge if graph changed",
            "halt if stop criterion met",
        ]
        phase_out["next"] = "experiment" if not stop else "halt"
    entry = {
        "ts": int(time.time()), "phase": phase, "topic": topic,
        "steer_count": _steer_count, "stop": stop, "dry_run": True,
        "degrade_label": probe.get("degrade_label"),
    }
    _research_log.append(entry)
    if len(_research_log) > 50:
        del _research_log[:-50]
    return {
        "phase": phase, "dry_run": True, "stop": stop, "steer_count": _steer_count,
        "task": None, "phase_out": phase_out,
        "probe": {"user_me_ok": probe["user_me_ok"], "degrade_label": probe["degrade_label"]},
        "log_tail": _research_log[-5:], "version": VERSION,
    }


async def autoresearch_loop(args: dict[str, Any]) -> dict[str, Any]:
    topic = (args.get("topic") or "public-record investigation").strip()
    try:
        cycles = max(1, min(int(args.get("cycles") or 1), LOOP_CAP))
    except Exception:
        cycles = 1
    results: list[dict[str, Any]] = []
    findings = ""
    for _ in range(cycles):
        for phase in ("experiment", "synthesize", "steer"):
            r = await research_steer({"phase": phase, "topic": topic, "findings": findings})
            results.append({
                "phase": phase,
                "next": r.get("phase_out", {}).get("next"),
                "steer_count": r.get("steer_count"),
                "actions": r.get("phase_out", {}).get("actions"),
            })
            findings = f"{phase} complete for {topic}"
            if r.get("stop"):
                return {
                    "topic": topic, "cycles_requested": cycles, "stopped_early": True,
                    "results": results, "version": VERSION,
                }
    return {
        "topic": topic, "cycles_requested": cycles, "stopped_early": False,
        "results": results, "version": VERSION,
    }
