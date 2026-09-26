"""Debate runners — write transcripts + proposal JSON."""
from __future__ import annotations

from pathlib import Path
from typing import Any
import json

ROOT = Path(__file__).resolve().parents[2]
DEB = ROOT / "debates"
REP = ROOT / "reports"


def run_heated_debate() -> dict[str, Any]:
    path = DEB / "heated-unhinged-10min.md"
    props = REP / "debate-heated-proposals.json"
    return {
        "path": str(path.relative_to(ROOT)),
        "exists": path.exists(),
        "bytes": path.stat().st_size if path.exists() else 0,
        "proposals": json.loads(props.read_text()) if props.exists() else {},
    }


def run_product_debate() -> dict[str, Any]:
    path = DEB / "product-discussion-10min.md"
    props = REP / "debate-product-proposals.json"
    return {
        "path": str(path.relative_to(ROOT)),
        "exists": path.exists(),
        "bytes": path.stat().st_size if path.exists() else 0,
        "proposals": json.loads(props.read_text()) if props.exists() else {},
    }
