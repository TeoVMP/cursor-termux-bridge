from __future__ import annotations

import fnmatch
from dataclasses import dataclass
from pathlib import Path


class PolicyError(RuntimeError):
    pass


@dataclass(slots=True)
class SessionPolicyState:
    plan_approved: bool = False
    plan_first: bool = True


class PolicyEngine:
    def __init__(
        self,
        allowed_roots: list[Path],
        blocked_commands: list[str],
        confirm_command_patterns: list[str],
    ) -> None:
        self.allowed_roots = [p.resolve() for p in allowed_roots]
        self.blocked_commands = [x.lower() for x in blocked_commands]
        self.confirm_command_patterns = [x.lower() for x in confirm_command_patterns]

    def assert_path_allowed(self, path: Path) -> None:
        resolved = path.resolve()
        if not self.allowed_roots:
            return
        for root in self.allowed_roots:
            if resolved == root or root in resolved.parents:
                return
        raise PolicyError(f"path not allowed: {resolved}")

    def is_command_blocked(self, command: str) -> bool:
        lower = command.lower().strip()
        return any(lower.startswith(prefix) for prefix in self.blocked_commands)

    def command_requires_approval(self, command: str) -> bool:
        lower = command.lower().strip()
        return any(fnmatch.fnmatch(lower, f"*{pattern}*") for pattern in self.confirm_command_patterns)

    def assert_mutation_allowed(self, tool_name: str, state: SessionPolicyState) -> None:
        mutable = {"write_file", "apply_patch", "run_shell"}
        if tool_name in mutable and state.plan_first and not state.plan_approved:
            raise PolicyError("plan-first enabled; mutation blocked until approval")
