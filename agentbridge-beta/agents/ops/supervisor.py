"""Supervisor orchestrator — multi-agent-patterns supervisor style."""
from __future__ import annotations

from typing import Any

from agents.marketing.team import run_marketing_proposals
from agents.product_sales.team import run_sales_proposals
from agents.debate.runners import run_heated_debate, run_product_debate
from agents.research.autoresearch_loop import bootstrap_research, inner_experiment, outer_synthesize
from tools.health_probe import probe_live
from utils.pep8_gate import scan_tree
from pathlib import Path
from swarm_config import VERSION, SKILLS_WIRED


def run_supervisor(full: bool = True) -> dict[str, Any]:
    report: dict[str, Any] = {
        "version": VERSION,
        "skills": SKILLS_WIRED,
        "live": probe_live(),
        "lint": {"count": len(scan_tree(Path(__file__).resolve().parents[2]))},
    }
    report["marketing"] = run_marketing_proposals()
    report["sales"] = run_sales_proposals()
    report["research"] = bootstrap_research()
    if full:
        report["research_inner"] = inner_experiment("H1-imprint-path")
        report["research_outer"] = outer_synthesize()
        report["debate_heated"] = run_heated_debate()
        report["debate_product"] = run_product_debate()
    return report
