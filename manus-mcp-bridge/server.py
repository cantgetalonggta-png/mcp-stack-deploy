"""Manus MCP Bridge v1.1 — HTTP MCP for remote clients.

Auth: Authorization: Bearer <BRIDGE_TOKEN>
Upstream: x-manus-api-key from MANUS_API_KEY. No secrets hardcoded.
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

app = FastAPI(title="Manus MCP Bridge", version="1.1.0")

BRIDGE_TOKEN = os.environ.get("BRIDGE_TOKEN", "")
MANUS_API_KEY = os.environ.get("MANUS_API_KEY", "")
MANUS_API_BASE = os.environ.get("MANUS_API_BASE", "https://api.manus.ai")
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))

ALLOWLIST_PREFIXES = ("/v2/",)


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
) -> dict[str, Any]:
    path = safe_path(path)
    url = f"{MANUS_API_BASE.rstrip('/')}{path}"
    if params:
        clean = {k: v for k, v in params.items() if v is not None and v != ""}
        if clean:
            url = f"{url}?{urlencode(clean, doseq=True)}"
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.request(
            method.upper(),
            url,
            headers=manus_headers(),
            json=json_body,
        )
    body: Any
    try:
        body = r.json()
    except Exception:
        body = r.text[:8000]
    return {
        "ok": r.status_code < 400,
        "status_code": r.status_code,
        "path": path,
        "body": body,
    }


TOOLS = [
    {
        "name": "manus_status",
        "description": "Bridge health + GET /v2/user.me",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "manus_user_me",
        "description": "GET /v2/user.me",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "manus_task_create",
        "description": "POST /v2/task.create — start a Manus agent task",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {"type": "string"},
                "project_id": {"type": "string"},
                "enable_skills": {"type": "array", "items": {"type": "string"}},
                "json": {"type": "object"},
            },
            "required": ["content"],
        },
    },
    {
        "name": "manus_task_list",
        "description": "GET /v2/task.list",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_id": {"type": "string"},
                "limit": {"type": "integer"},
            },
        },
    },
    {
        "name": "manus_task_detail",
        "description": "GET /v2/task.detail",
        "inputSchema": {
            "type": "object",
            "properties": {"task_id": {"type": "string"}},
            "required": ["task_id"],
        },
    },
    {
        "name": "manus_task_send_message",
        "description": "POST /v2/task.sendMessage — multi-turn",
        "inputSchema": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "content": {"type": "string"},
            },
            "required": ["task_id", "content"],
        },
    },
    {
        "name": "manus_task_stop",
        "description": "POST /v2/task.stop",
        "inputSchema": {
            "type": "object",
            "properties": {"task_id": {"type": "string"}},
            "required": ["task_id"],
        },
    },
    {
        "name": "manus_project_list",
        "description": "GET /v2/project.list",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "manus_skill_list",
        "description": "GET /v2/skill.list",
        "inputSchema": {
            "type": "object",
            "properties": {"project_id": {"type": "string"}},
        },
    },
    {
        "name": "manus_usage_credits",
        "description": "GET /v2/usage.availableCredits",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "manus_research_steer",
        "description": "Autoresearch helper: wrap a hypothesis as a Manus task prompt",
        "inputSchema": {
            "type": "object",
            "properties": {
                "phase": {
                    "type": "string",
                    "enum": ["experiment", "synthesize", "steer"],
                },
                "hypothesis": {"type": "string"},
                "findings": {"type": "string"},
                "content": {"type": "string"},
            },
            "required": ["phase"],
        },
    },
    {
        "name": "manus_proxy",
        "description": "Allowlisted /v2/* proxy",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "method": {"type": "string", "default": "GET"},
                "json": {"type": "object"},
                "params": {"type": "object"},
            },
            "required": ["path"],
        },
    },
]


@app.get("/health")
async def health():
    return {
        "ok": True,
        "service": "manus-mcp-bridge",
        "version": "1.1.0",
        "bridge_token_configured": bool(BRIDGE_TOKEN),
        "manus_key_configured": bool(MANUS_API_KEY),
        "tools": [t["name"] for t in TOOLS],
        "ts": int(time.time()),
    }


@app.get("/")
async def root():
    return {
        "name": "manus-mcp-bridge",
        "version": "1.1.0",
        "mcp": "/mcp",
        "health": "/health",
        "docs": "/docs",
        "tools": [t["name"] for t in TOOLS],
    }


class ToolCall(BaseModel):
    name: str
    arguments: dict[str, Any] = {}


@app.get("/mcp")
@app.post("/mcp")
async def mcp_endpoint(
    request: Request,
    authorization: Optional[str] = Header(default=None),
):
    require_bridge_auth(authorization)
    if request.method == "GET":
        return {
            "protocol": "mcp-http-bridge",
            "version": "1.1",
            "tools": TOOLS,
        }
    try:
        body = await request.json()
    except Exception:
        body = {}
    method = body.get("method") or body.get("name") or "tools/list"
    if method in ("tools/list", "list_tools"):
        return {"tools": TOOLS}

    name = body.get("name") or (body.get("params") or {}).get("name")
    args = body.get("arguments") or (body.get("params") or {}).get("arguments") or {}
    if method in ("tools/call", "call_tool") and not name:
        name = (body.get("params") or {}).get("name")

    dispatch = name or method
    try:
        return await dispatch_tool(dispatch, args if isinstance(args, dict) else {})
    except HTTPException:
        raise
    except Exception as exc:
        return JSONResponse({"error": str(exc), "tool": dispatch}, status_code=500)


async def dispatch_tool(name: str, args: dict[str, Any]) -> Any:
    if name == "manus_status":
        return await manus_status()
    if name == "manus_user_me":
        return await manus_request("GET", "/v2/user.me")
    if name == "manus_task_create":
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
        return await manus_request(
            "GET",
            "/v2/task.list",
            params={
                "project_id": args.get("project_id"),
                "limit": args.get("limit"),
            },
        )
    if name == "manus_task_detail":
        return await manus_request(
            "GET",
            "/v2/task.detail",
            params={"task_id": args.get("task_id")},
        )
    if name == "manus_task_send_message":
        return await manus_request(
            "POST",
            "/v2/task.sendMessage",
            json_body={
                "task_id": args.get("task_id"),
                "message": {"content": args.get("content")},
            },
        )
    if name == "manus_task_stop":
        return await manus_request(
            "POST",
            "/v2/task.stop",
            json_body={"task_id": args.get("task_id")},
        )
    if name == "manus_project_list":
        return await manus_request("GET", "/v2/project.list")
    if name == "manus_skill_list":
        return await manus_request(
            "GET",
            "/v2/skill.list",
            params={"project_id": args.get("project_id")},
        )
    if name == "manus_usage_credits":
        return await manus_request("GET", "/v2/usage.availableCredits")
    if name == "manus_research_steer":
        return await research_steer(args)
    if name == "manus_proxy":
        return await manus_request(
            args.get("method") or "GET",
            args.get("path") or "/v2/user.me",
            json_body=args.get("json"),
            params=args.get("params"),
        )
    return JSONResponse({"error": f"unknown tool: {name}"}, status_code=400)


async def manus_status():
    status: dict[str, Any] = {
        "bridge": "ok",
        "version": "1.1.0",
        "manus_key_configured": bool(MANUS_API_KEY),
        "manus_api_base": MANUS_API_BASE,
        "tools": [t["name"] for t in TOOLS],
    }
    if not MANUS_API_KEY:
        status["manus"] = "skipped (no MANUS_API_KEY)"
        return status
    me = await manus_request("GET", "/v2/user.me")
    status["manus_http"] = me["status_code"]
    status["user"] = me["body"]
    return status


async def research_steer(args: dict[str, Any]) -> dict[str, Any]:
    phase = (args.get("phase") or "experiment").lower()
    hypothesis = args.get("hypothesis") or ""
    findings = args.get("findings") or ""
    extra = args.get("content") or ""
    prompts = {
        "experiment": (
            "INNER LOOP experiment. Test this hypothesis with a short public-web "
            f"investigation and return measurable findings.\nHypothesis: {hypothesis}\n{extra}"
        ),
        "synthesize": (
            "OUTER LOOP synthesize. Given findings, extract patterns, contradictions, "
            f"and confidence.\nFindings:\n{findings}\nHypothesis: {hypothesis}\n{extra}"
        ),
        "steer": (
            "STEER. Propose the next hypothesis or stop criterion from the synthesis.\n"
            f"Findings:\n{findings}\nPrior hypothesis: {hypothesis}\n{extra}"
        ),
    }
    content = prompts.get(phase, prompts["experiment"])
    created = await manus_request(
        "POST",
        "/v2/task.create",
        json_body={"message": {"content": content}},
    )
    return {"phase": phase, "prompted": content[:400], "task": created}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host=HOST, port=PORT, reload=False)
