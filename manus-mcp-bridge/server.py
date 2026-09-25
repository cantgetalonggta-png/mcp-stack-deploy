"""Manus MCP Bridge v1.2 \u2014 HTTP MCP + health that actually probes user.me."""
from __future__ import annotations

import os
import time
from typing import Any, Optional
from urllib.parse import urlencode

import httpx
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

VERSION = "1.2.0"
app = FastAPI(title="Manus MCP Bridge", version=VERSION)

BRIDGE_TOKEN = os.environ.get("BRIDGE_TOKEN", "")
MANUS_API_KEY = os.environ.get("MANUS_API_KEY", "")
MANUS_API_BASE = os.environ.get("MANUS_API_BASE", "https://api.manus.ai")
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))
ALLOWLIST_PREFIXES = ("/v2/",)
CREDIT_LOW = float(os.environ.get("CREDIT_LOW_THRESHOLD", "50"))


def require_bridge_auth(authorization: Optional[str]) -> None:
    if not BRIDGE_TOKEN:
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = authorization.removeprefix("Bearer ").strip()
    if token != BRIDGE_TOKEN:
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
    if ".." in p or not p.startswith(ALLOWLIST_PREFIXES):
        raise HTTPException(status_code=400, detail="path must start with /v2/")
    return p


async def manus_request(
    method: str,
    path: str,
    json_body: Any = None,
    params: Optional[dict[str, Any]] = None,
    timeout: float = 20.0,
) -> dict[str, Any]:
    path = safe_path(path)
    url = f"{MANUS_API_BASE.rstrip('/')}{path}"
    if params:
        clean = {k: v for k, v in params.items() if v is not None and v != ""}
        if clean:
            url = f"{url}?{urlencode(clean, doseq=True)}"
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.request(
                method.upper(), url, headers=manus_headers(), json=json_body
            )
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
        if key in body and isinstance(body[key], (int, float)):
            return float(body[key])
    data = body.get("data") if isinstance(body.get("data"), dict) else {}
    for key in ("available_credits", "credits", "balance", "remaining"):
        if key in data and isinstance(data[key], (int, float)):
            return float(data[key])
    return None


async def probe_upstream() -> dict[str, Any]:
    out: dict[str, Any] = {
        "user_me_ok": False,
        "user_me_status": None,
        "credits_ok": False,
        "credits_status": None,
        "credits_hint": None,
        "degrade_level": 0,
        "degrade_label": "paid",
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
        if body.get("error"):
            err = body.get("error")
            out["user_me_error"] = err.get("code") if isinstance(err, dict) else str(err)[:120]
    elif me.get("error"):
        out["user_me_error"] = str(me["error"])[:120]
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


TOOLS = [
    {"name": "manus_status", "description": "Bridge health + live GET /v2/user.me probe", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "manus_user_me", "description": "GET /v2/user.me", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "manus_task_create", "description": "POST /v2/task.create \u2014 spends credits", "inputSchema": {"type": "object", "properties": {"content": {"type": "string"}, "project_id": {"type": "string"}, "enable_skills": {"type": "array", "items": {"type": "string"}}, "json": {"type": "object"}}, "required": ["content"]}},
    {"name": "manus_task_list", "description": "GET /v2/task.list", "inputSchema": {"type": "object", "properties": {"project_id": {"type": "string"}, "limit": {"type": "integer"}}}},
    {"name": "manus_task_detail", "description": "GET /v2/task.detail", "inputSchema": {"type": "object", "properties": {"task_id": {"type": "string"}}, "required": ["task_id"]}},
    {"name": "manus_task_send_message", "description": "POST /v2/task.sendMessage", "inputSchema": {"type": "object", "properties": {"task_id": {"type": "string"}, "content": {"type": "string"}}, "required": ["task_id", "content"]}},
    {"name": "manus_task_stop", "description": "POST /v2/task.stop", "inputSchema": {"type": "object", "properties": {"task_id": {"type": "string"}}, "required": ["task_id"]}},
    {"name": "manus_project_list", "description": "GET /v2/project.list", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "manus_skill_list", "description": "GET /v2/skill.list", "inputSchema": {"type": "object", "properties": {"project_id": {"type": "string"}}}},
    {"name": "manus_usage_credits", "description": "GET /v2/usage.availableCredits", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "manus_research_steer", "description": "Autoresearch experiment|synthesize|steer. Default dry_run=true.", "inputSchema": {"type": "object", "properties": {"phase": {"type": "string", "enum": ["experiment", "synthesize", "steer"]}, "hypothesis": {"type": "string"}, "findings": {"type": "string"}, "content": {"type": "string"}, "create_task": {"type": "boolean"}, "dry_run": {"type": "boolean"}}, "required": ["phase"]}},
    {"name": "manus_degrade_status", "description": "Fuel gauge + degrade level + local finish checklist", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "manus_proxy", "description": "Allowlisted /v2/* proxy", "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}, "method": {"type": "string", "default": "GET"}, "json": {"type": "object"}, "params": {"type": "object"}}, "required": ["path"]}},
]


@app.get("/health")
async def health():
    probe = await probe_upstream()
    return {
        "ok": True,
        "service": "manus-mcp-bridge",
        "version": VERSION,
        "bridge_token_configured": bool(BRIDGE_TOKEN),
        "manus_key_configured": bool(MANUS_API_KEY),
        "user_me_ok": probe["user_me_ok"],
        "user_me_status": probe["user_me_status"],
        "credits_ok": probe["credits_ok"],
        "degrade_level": probe["degrade_level"],
        "degrade_label": probe["degrade_label"],
        "tools": [t["name"] for t in TOOLS],
        "ts": int(time.time()),
        "user_me_error": probe.get("user_me_error"),
        "user_id_present": probe.get("user_id_present"),
    }


@app.get("/")
async def root():
    return {"name": "manus-mcp-bridge", "version": VERSION, "mcp": "/mcp", "health": "/health", "docs": "/docs", "tools": [t["name"] for t in TOOLS]}


class ToolCall(BaseModel):
    name: str
    arguments: dict[str, Any] = {}


@app.get("/mcp")
@app.post("/mcp")
async def mcp_endpoint(request: Request, authorization: Optional[str] = Header(default=None)):
    require_bridge_auth(authorization)
    if request.method == "GET":
        return {"protocol": "mcp-http-bridge", "version": "1.2", "tools": TOOLS}
    try:
        body = await request.json()
    except Exception:
        body = {}
    method = body.get("method") or body.get("name") or "tools/list"
    if method in ("tools/list", "list_tools"):
        return {"tools": TOOLS}
    name = body.get("name") or (body.get("params") or {}).get("name")
    args = body.get("arguments") or (body.get("params") or {}).get("arguments") or {}
    dispatch = name or method
    try:
        return await dispatch_tool(dispatch, args if isinstance(args, dict) else {})
    except HTTPException:
        raise
    except Exception as exc:
        return JSONResponse({"error": str(exc), "tool": dispatch}, status_code=500)


def local_finish_checklist() -> list[str]:
    return [
        "Do not call task.create until credits or key recover.",
        "Dump work to git: code, notes, open issues.",
        "Switch IDE model to local OSS for typing.",
        "Keep this bridge up \u2014 GitHub/Vercel tools do not need Manus credits.",
        "Finish remaining Manus work later with task.sendMessage on an existing task.",
    ]


async def dispatch_tool(name: str, args: dict[str, Any]) -> Any:
    if name == "manus_status":
        return await manus_status()
    if name == "manus_user_me":
        return await manus_request("GET", "/v2/user.me")
    if name == "manus_task_create":
        probe = await probe_upstream()
        if probe["degrade_level"] >= 4:
            return {"ok": False, "blocked": True, "reason": "degrade_level>=4", "checklist": local_finish_checklist(), "probe": probe}
        payload = dict(args.get("json") or {})
        content = args.get("content")
        if content:
            payload.setdefault("message", {})["content"] = content
        if args.get("project_id"):
            payload["project_id"] = args["project_id"]
        if args.get("enable_skills"):
            payload["enable_skills"] = args["enable_skills"]
        return await manus_request("POST", "/v2/task.create", json_body=payload)
    if name == "manus_task_list":
        return await manus_request("GET", "/v2/task.list", params={"project_id": args.get("project_id"), "limit": args.get("limit")})
    if name == "manus_task_detail":
        return await manus_request("GET", "/v2/task.detail", params={"task_id": args.get("task_id")})
    if name == "manus_task_send_message":
        return await manus_request("POST", "/v2/task.sendMessage", json_body={"task_id": args.get("task_id"), "message": {"content": args.get("content")}})
    if name == "manus_task_stop":
        return await manus_request("POST", "/v2/task.stop", json_body={"task_id": args.get("task_id")})
    if name == "manus_project_list":
        return await manus_request("GET", "/v2/project.list")
    if name == "manus_skill_list":
        return await manus_request("GET", "/v2/skill.list", params={"project_id": args.get("project_id")})
    if name == "manus_usage_credits":
        return await manus_request("GET", "/v2/usage.availableCredits")
    if name == "manus_research_steer":
        return await research_steer(args)
    if name == "manus_degrade_status":
        probe = await probe_upstream()
        probe["checklist"] = local_finish_checklist() if probe["degrade_level"] >= 2 else None
        return probe
    if name == "manus_proxy":
        return await manus_request(args.get("method") or "GET", args.get("path") or "/v2/user.me", json_body=args.get("json"), params=args.get("params"))
    return JSONResponse({"error": f"unknown tool: {name}"}, status_code=400)


async def manus_status():
    probe = await probe_upstream()
    return {"bridge": "ok", "version": VERSION, "manus_key_configured": bool(MANUS_API_KEY), "manus_api_base": MANUS_API_BASE, "tools": [t["name"] for t in TOOLS], "probe": probe}


async def research_steer(args: dict[str, Any]) -> dict[str, Any]:
    phase = (args.get("phase") or "experiment").lower()
    hypothesis = args.get("hypothesis") or ""
    findings = args.get("findings") or ""
    extra = args.get("content") or ""
    create_task = bool(args.get("create_task"))
    dry_run = args.get("dry_run")
    if dry_run is None:
        dry_run = not create_task
    prompts = {
        "experiment": f"INNER LOOP experiment. Test this hypothesis with a short public-web investigation and return measurable findings.\nHypothesis: {hypothesis}\n{extra}",
        "synthesize": f"OUTER LOOP synthesize. Given findings, extract patterns, contradictions, and confidence.\nFindings:\n{findings}\nHypothesis: {hypothesis}\n{extra}",
        "steer": f"STEER. Propose the next hypothesis or stop criterion from the synthesis.\nFindings:\n{findings}\nPrior hypothesis: {hypothesis}\n{extra}",
    }
    content = prompts.get(phase, prompts["experiment"])
    result: dict[str, Any] = {"phase": phase, "dry_run": bool(dry_run), "prompted": content[:800], "next": {"experiment": "Run one measurable check.", "synthesize": "Write what is actually true.", "steer": "Change the next experiment or stop."}.get(phase)}
    probe = await probe_upstream()
    result["probe"] = {"user_me_ok": probe["user_me_ok"], "degrade_level": probe["degrade_level"], "degrade_label": probe["degrade_label"]}
    if dry_run or probe["degrade_level"] >= 4:
        result["task"] = None
        result["blocked"] = probe["degrade_level"] >= 4
        return result
    created = await manus_request("POST", "/v2/task.create", json_body={"message": {"content": content}})
    result["task"] = created
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host=HOST, port=PORT, reload=False)
