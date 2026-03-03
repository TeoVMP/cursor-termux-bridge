from __future__ import annotations

import subprocess
from pathlib import Path

from bridge_server.policy import PolicyEngine


def glob_paths(policy: PolicyEngine, project_root: Path, pattern: str) -> dict[str, list[str]]:
    policy.assert_path_allowed(project_root)
    matches = [str(path) for path in project_root.glob(pattern)]
    return {"matches": sorted(matches)}


def rg_search(
    policy: PolicyEngine,
    project_root: Path,
    pattern: str,
    glob: str | None = None,
    max_results: int = 100,
) -> dict[str, list[str]]:
    policy.assert_path_allowed(project_root)
    command = ["rg", "-n", "--max-count", str(max_results), pattern, str(project_root)]
    if glob:
        command.extend(["--glob", glob])
    proc = subprocess.run(command, capture_output=True, text=True, timeout=20, check=False)
    lines = proc.stdout.splitlines()
    return {"matches": lines[:max_results], "stderr": proc.stderr[:4000]}
