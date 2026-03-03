from __future__ import annotations

import subprocess
from pathlib import Path

from bridge_server.policy import PolicyEngine, PolicyError


def run_shell(
    policy: PolicyEngine,
    project_root: Path,
    command: str,
    timeout_seconds: int,
    max_output_chars: int,
    approval_granted: bool,
) -> dict[str, str | int]:
    policy.assert_path_allowed(project_root)
    if policy.is_command_blocked(command):
        raise PolicyError("command blocked by policy")
    if policy.command_requires_approval(command) and not approval_granted:
        raise PolicyError("command requires approval")

    proc = subprocess.run(
        command,
        shell=True,
        cwd=str(project_root),
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
    )
    stdout = (proc.stdout or "")[:max_output_chars]
    stderr = (proc.stderr or "")[:max_output_chars]
    return {
        "exit_code": proc.returncode,
        "stdout": stdout,
        "stderr": stderr,
    }
