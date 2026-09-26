"""Lightweight PEP8-ish style gate (python-pep8-code-reviewer skill proxy)."""
from __future__ import annotations

from pathlib import Path


def scan_tree(root: Path) -> list[dict]:
    issues: list[dict] = []
    for path in root.rglob("*.py"):
        if ".venv" in path.parts or "site-packages" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if len(line) > 120:
                issues.append({
                    "file": str(path.relative_to(root)),
                    "line": i,
                    "rule": "E501",
                    "msg": "line > 120",
                })
            if line.rstrip() != line and line.strip():
                issues.append({
                    "file": str(path.relative_to(root)),
                    "line": i,
                    "rule": "W291",
                    "msg": "trailing whitespace",
                })
            if "\t" in line:
                issues.append({
                    "file": str(path.relative_to(root)),
                    "line": i,
                    "rule": "W191",
                    "msg": "tab indent",
                })
    return issues
