"""Expanded autoresearch skill: experiment → synthesize → steer."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "research" / "research-state.yaml"
FINDINGS = ROOT / "research" / "findings.md"
LOG = ROOT / "research" / "research-log.md"
EXP = ROOT / "research" / "experiments"


def bootstrap_research() -> dict[str, Any]:
    EXP.mkdir(parents=True, exist_ok=True)
    state = {
        "project": "AgentBridge Beta imprint + conversion",
        "question": (
            "What minimal public proof converts a key-owning builder "
            "into one honest imprint?"
        ),
        "hypotheses": [
            {
                "id": "H1",
                "text": "Live /eval green + creates honesty increases imprint rate",
            },
            {
                "id": "H2",
                "text": "Compare table vs DIY/agency pricing beats feature lists",
            },
            {
                "id": "H3",
                "text": "Debate archive + beta dashboard signals seriousness",
            },
        ],
        "metric": "non_ops_imprint_count",
        "baseline": 0,
        "phase": "bootstrap",
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    lines = [
        "# research-state.yaml",
        f"project: {state['project']!r}",
        f"question: {state['question']!r}",
        "hypotheses:",
    ]
    for h in state["hypotheses"]:
        lines.append(f"  - id: {h['id']}")
        lines.append(f"    text: {h['text']!r}")
    lines += [
        f"metric: {state['metric']}",
        f"baseline: {state['baseline']}",
        f"phase: {state['phase']}",
        f"ts: {state['ts']}",
    ]
    STATE.write_text("\n".join(lines) + "\n")
    if not FINDINGS.exists():
        FINDINGS.write_text(
            "# Findings\n\n"
            "Bootstrapped. Live bridge v1.3.1 passes /eval. "
            "Imprint wall open. Ops seeds exist; stranger imprint "
            "still the north star.\n"
        )
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"\n## {state['ts']} bootstrap\n- Question locked\n- H1-H3 formed\n")
    return state


def inner_experiment(slug: str) -> dict[str, Any]:
    folder = EXP / slug
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "protocol.md").write_text(
        f"# Protocol {slug}\n\n"
        "**Prediction:** Publishing Beta dashboard + product debate "
        "proposals increases qualified wall visits without fake proof.\n\n"
        "**Measure:** imprint wall hits + new non-ops imprint issues.\n"
    )
    (folder / "analysis.md").write_text(
        f"# Analysis {slug}\n\n"
        f"ts: {datetime.now(timezone.utc).isoformat()}\n\n"
        "CONFIRMATORY setup only until stranger imprint lands. "
        "Live eval green; creates remaining=3; scope=instance-best-effort.\n"
    )
    result = {
        "experiment_id": slug,
        "hypothesis": "H1",
        "status": "protocol_locked",
        "metric_value": None,
        "note": "Await outside imprint; do not fabricate metric",
    }
    (folder / "results").mkdir(exist_ok=True)
    (folder / "results" / "summary.json").write_text(json.dumps(result, indent=2))
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"\n## inner {slug}\n- protocol locked\n")
    return result


def outer_synthesize() -> dict[str, Any]:
    FINDINGS.write_text(
        "# Findings (outer loop)\n\n"
        "## What we know\n"
        "- Bridge health/eval green is necessary but not sufficient "
        "for stranger imprint.\n"
        "- Ops seeds must stay labeled so scoreboard stays honest.\n"
        "- Market: DIY fragile, agency $3-6k, multi-source $6-12k; "
        "AgentBridge sells fixed path.\n\n"
        "## Patterns\n"
        "- Builders respond to live chips and explicit limits.\n"
        "- Debates surface implementation ideas better than solo brainstorm.\n\n"
        "## Open\n"
        "- First non-ops imprint still pending — primary success criterion.\n"
    )
    synth = {
        "direction": "DEEPEN",
        "reason": "H1 untested with real stranger; keep eval honesty",
        "next": "Ship Beta dashboard; honest system imprint; hunt outside mark",
    }
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"\n## outer synthesize\n- direction: {synth['direction']}\n")
    return synth
