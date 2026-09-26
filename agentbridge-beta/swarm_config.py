"""AgentBridge Beta — central swarm configuration."""
from __future__ import annotations

VERSION = "0.2.0-beta"
PRODUCT = "AgentBridge Beta"
LIVE_BRIDGE = "https://manus-mcp-bridge-olive.vercel.app"
LIVE_LANDING = "https://agentbridge-launch.vercel.app"
LIVE_IMPRINT = "https://agentbridge-launch.vercel.app/imprint"
LIVE_EVAL = "https://manus-mcp-bridge-olive.vercel.app/eval"
REPO = "cantgetalonggta-png/mcp-stack-deploy"

SKILLS_WIRED = [
    "code-evolution",
    "comedian-persona-debate",
    "deployment-automation",
    "knowledge-base-builder",
    "multi-agent-tooling",
    "public-dataset-discovery",
    "python-pep8-code-reviewer",
    "self-dev-resources",
    "rex-export-x5-master",
    "autoresearch",
    "api-integration-master",
    "api-key-management",
    "llm-orchestration",
    "metrics-self-healing",
    "multi-agent-patterns",
    "multi-agent-project-structure",
    "mcp-http-bridge",
    "manus-api",
    "agentbridge-launch",
    "stack-distill-mcp-agentbridge",
]

TEAMS = {
    "marketing": ["HookLead", "ChannelScout", "ImprintHunter", "CarlinCritic"],
    "product_sales": ["OfferArchitect", "ObjectionKiller", "SlotCloser", "HonestyGuard"],
    "debate": ["Rex", "Kenji", "Raj", "Nova", "Blitz"],
    "research": ["InnerLoop", "OuterLoop", "Steer", "TruthVerifier"],
    "ops": ["Deployer", "HealthWatch", "SecretGuard", "Rollback"],
}

SUCCESS_CRITERIA = {
    "outside_imprint": "At least one non-ops public imprint (GitHub issue label=imprint or wall entry)",
    "eval_green": "GET /eval pass:true chip green",
    "beta_dashboard": "Public beta dashboard deployed",
    "debates_archived": "Heated + product debate transcripts + MP3 proposals",
}
