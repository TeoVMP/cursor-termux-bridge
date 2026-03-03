from pathlib import Path

import pytest

from bridge_server.policy import PolicyEngine, PolicyError, SessionPolicyState


def test_path_allowed() -> None:
    root = Path(".").resolve()
    policy = PolicyEngine([root], blocked_commands=[], confirm_command_patterns=[])
    policy.assert_path_allowed(root / "a.txt")


def test_path_blocked() -> None:
    root = Path(".").resolve()
    policy = PolicyEngine([root / "allowed"], blocked_commands=[], confirm_command_patterns=[])
    with pytest.raises(PolicyError):
        policy.assert_path_allowed(root / "other" / "a.txt")


def test_plan_first_blocks_mutations() -> None:
    policy = PolicyEngine([], blocked_commands=[], confirm_command_patterns=[])
    with pytest.raises(PolicyError):
        policy.assert_mutation_allowed("write_file", SessionPolicyState(plan_approved=False, plan_first=True))
