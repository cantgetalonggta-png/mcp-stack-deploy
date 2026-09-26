"""Product sales team — slot closing with honesty guard."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OUT = Path(__file__).resolve().parents[2] / "reports" / "sales-proposals.json"


def run_sales_proposals() -> dict[str, Any]:
    proposals = [
        {
            "agent": "OfferArchitect",
            "sku": "Starter",
            "price": 1499,
            "include": ["1-2 tools", "client pack", "health plane", "5-day path"],
            "exclude": ["raw Manus key access", "unlimited creates", "fake KV"],
        },
        {
            "agent": "OfferArchitect",
            "sku": "Standard",
            "price": 2499,
            "include": ["5-10 tools", "runbook", "eval gate", "auth allowlist"],
            "exclude": ["selling operator credits"],
        },
        {
            "agent": "OfferArchitect",
            "sku": "Hosted",
            "price": 99,
            "period": "mo",
            "include": ["uptime", "token rotation help", "eval"],
            "note": "Do NOT sell KV until shared store is real",
        },
        {
            "agent": "ObjectionKiller",
            "objection": "Why not Zapier/n8n?",
            "rebuttal": (
                "General automation vs HTTP MCP for agent clients "
                "with Bearer lock + allowlist + live user.me chip."
            ),
        },
        {
            "agent": "ObjectionKiller",
            "objection": "Can I use your Manus key?",
            "rebuttal": "No. BYO keys. We sell the hose pattern.",
        },
        {
            "agent": "SlotCloser",
            "action": "Lead form opens GitHub [lead] issue — 24h reply SLA",
            "cta": "Get a slot on landing #buy",
        },
        {
            "agent": "HonestyGuard",
            "flags": [
                "remaining_creates_scope is instance-best-effort until shared KV",
                "Hosted $99 does not include pretend durable store",
                "No fabricated case studies on brochure or site",
                "Ops imprint seeds must not count as stranger imprints",
            ],
        },
    ]
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "team": "product_sales",
        "proposals": proposals,
        "recommendation": (
            "Close on proof (eval green) not hype. "
            "Price is fixed-path delivery of gateway pattern."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    return payload
