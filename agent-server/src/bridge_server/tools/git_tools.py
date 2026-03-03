from __future__ import annotations

import subprocess
from pathlib import Path

from bridge_server.policy import PolicyEngine


def _run_git(project_root: Path, args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(project_root),
        capture_output=True,
        text=True,
        check=False,
        timeout=20,
    )
    out = (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")
    return out.strip()


def git_status(policy: PolicyEngine, project_root: Path) -> dict[str, str]:
    policy.assert_path_allowed(project_root)
    return {"output": _run_git(project_root, ["status", "--short", "--branch"])}


def git_diff(policy: PolicyEngine, project_root: Path) -> dict[str, str]:
    policy.assert_path_allowed(project_root)
    return {"output": _run_git(project_root, ["diff"])}
