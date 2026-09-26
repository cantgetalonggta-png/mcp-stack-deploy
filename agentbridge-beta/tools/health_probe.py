"""Probe live AgentBridge endpoints."""
from __future__ import annotations

import json
from typing import Any
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from swarm_config import LIVE_BRIDGE, LIVE_EVAL, LIVE_LANDING, LIVE_IMPRINT


def _get(url: str, timeout: float = 12.0) -> dict[str, Any]:
    try:
        req = Request(url, headers={"User-Agent": "AgentBridge-Beta/0.2"})
        with urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8", errors="replace")
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                data = {"raw": body[:500]}
            return {"ok": True, "status": r.status, "data": data}
    except HTTPError as e:
        return {"ok": False, "status": e.code, "error": str(e)}
    except URLError as e:
        return {"ok": False, "status": 0, "error": str(e)}


def probe_live() -> dict[str, Any]:
    health = _get(f"{LIVE_BRIDGE}/health")
    evalp = _get(LIVE_EVAL)
    landing = _get(LIVE_LANDING)
    imprint = _get(LIVE_IMPRINT)
    eval_data = evalp.get("data") if isinstance(evalp.get("data"), dict) else {}
    return {
        "health": health,
        "eval": evalp,
        "landing_status": landing.get("status"),
        "imprint_status": imprint.get("status"),
        "eval_pass": bool(eval_data.get("pass")),
        "chip": eval_data.get("chip"),
        "bridge_version": (health.get("data") or {}).get("version") if isinstance(health.get("data"), dict) else None,
    }
