#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../manus-mcp-bridge"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install -r requirements.txt
else
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
# Codespaces injects secrets as env vars automatically
if [[ -z "${BRIDGE_TOKEN:-}" ]]; then
  export BRIDGE_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
  echo "Generated ephemeral BRIDGE_TOKEN (set Codespace secret for stable token)"
  echo "BRIDGE_TOKEN=$BRIDGE_TOKEN"
fi
exec python server.py
