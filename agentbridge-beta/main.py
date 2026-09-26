#!/usr/bin/env python3
"""AgentBridge Beta — supervisor entrypoint."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from swarm_config import PRODUCT, VERSION, SKILLS_WIRED, SUCCESS_CRITERIA, LIVE_EVAL, LIVE_BRIDGE
from agents.ops.supervisor import run_supervisor
from agents.marketing.team import run_marketing_proposals
from agents.product_sales.team import run_sales_proposals
from agents.debate.runners import run_heated_debate, run_product_debate
from agents.research.autoresearch_loop import bootstrap_research
from tools.health_probe import probe_live
from utils.pep8_gate import scan_tree


def cmd_status(_: argparse.Namespace) -> int:
    health = probe_live()
    out = {
        "product": PRODUCT,
        "version": VERSION,
        "skills_wired": len(SKILLS_WIRED),
        "success_criteria": SUCCESS_CRITERIA,
        "live": health,
    }
    print(json.dumps(out, indent=2))
    return 0 if health.get("eval_pass") else 1


def cmd_build(args: argparse.Namespace) -> int:
    print(f"== {PRODUCT} {VERSION} BUILD ==")
    reports = run_supervisor(full=not args.quick)
    (ROOT / "reports" / "build-summary.json").write_text(json.dumps(reports, indent=2))
    print(json.dumps({"ok": True, "wrote": "reports/build-summary.json", "keys": list(reports.keys())}, indent=2))
    return 0


def cmd_debates(_: argparse.Namespace) -> int:
    h = run_heated_debate()
    p = run_product_debate()
    print(json.dumps({"heated": h, "product": p}, indent=2))
    return 0


def cmd_teams(_: argparse.Namespace) -> int:
    m = run_marketing_proposals()
    s = run_sales_proposals()
    r = bootstrap_research()
    print(json.dumps({"marketing": m, "sales": s, "research": r}, indent=2))
    return 0


def cmd_lint(_: argparse.Namespace) -> int:
    issues = scan_tree(ROOT)
    print(json.dumps({"issues": issues, "count": len(issues)}, indent=2))
    return 0 if not issues else 1


def main() -> int:
    p = argparse.ArgumentParser(description=f"{PRODUCT} CLI")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(func=cmd_status)
    b = sub.add_parser("build")
    b.add_argument("--quick", action="store_true")
    b.set_defaults(func=cmd_build)
    sub.add_parser("debates").set_defaults(func=cmd_debates)
    sub.add_parser("teams").set_defaults(func=cmd_teams)
    sub.add_parser("lint").set_defaults(func=cmd_lint)
    args = p.parse_args()
    return int(args.func(args) or 0)


if __name__ == "__main__":
    raise SystemExit(main())
