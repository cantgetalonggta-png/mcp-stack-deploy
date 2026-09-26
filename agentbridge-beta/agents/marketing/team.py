"""Marketing team proposals — AUTO_MARKETING."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OUT = Path(__file__).resolve().parents[2] / "reports" / "marketing-proposals.json"


def run_marketing_proposals() -> dict[str, Any]:
    proposals = [
        {
            "agent": "HookLead",
            "title": "Honest hose, not vapor",
            "action": "Lead with live /eval green chip + remaining_creates honesty",
            "channel": "landing + imprint wall + X/GitHub",
            "metric": "CTR to imprint wall",
            "priority": 1,
        },
        {
            "agent": "ChannelScout",
            "title": "Builder channels only",
            "action": "Target key owners only (HN, IH, Cursor, MCP dirs)",
            "channel": "community posts with eval link",
            "metric": "qualified imprint issues",
            "priority": 1,
        },
        {
            "agent": "ImprintHunter",
            "title": "One stranger sentence",
            "action": "Ship wall + one-pager + gist; ask ONE honest sentence",
            "channel": "imprint wall",
            "metric": "non-ops imprint count >= 1",
            "priority": 0,
        },
        {
            "agent": "CarlinCritic",
            "title": "Language audit",
            "action": "Kill AI-platform fluff. Say hose + lock + live user.me",
            "channel": "copy rewrite",
            "metric": "jargon ratio down",
            "priority": 2,
        },
        {
            "agent": "HookLead",
            "title": "Beta badge",
            "action": "Publish Beta 0.2 dashboard with skills + debates",
            "channel": "beta dashboard",
            "metric": "dashboard uniques",
            "priority": 1,
        },
        {
            "agent": "ChannelScout",
            "title": "Compare table push",
            "action": "Surface compare.html vs DIY / agency / multi-source",
            "channel": "compare page",
            "metric": "compare -> lead form",
            "priority": 2,
        },
    ]
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "team": "marketing",
        "proposals": proposals,
        "recommendation": (
            "Prioritize ImprintHunter + live eval proof over brand fluff. "
            "One honest outside mark beats ten fake testimonials."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    return payload
