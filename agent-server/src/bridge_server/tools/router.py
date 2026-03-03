from __future__ import annotations

from pathlib import Path
from typing import Any

from bridge_server.config import Settings
from bridge_server.policy import PolicyEngine, SessionPolicyState
from bridge_server.tools import (
    apply_json_patch,
    git_diff,
    git_status,
    glob_paths,
    read_file,
    rg_search,
    run_shell,
    write_file,
)


class ToolRouter:
    def __init__(self, settings: Settings, policy: PolicyEngine) -> None:
        self.settings = settings
        self.policy = policy

    @staticmethod
    def definitions() -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read file content within project root",
                    "parameters": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}},
                        "required": ["path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Write file content within project root",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "content": {"type": "string"},
                        },
                        "required": ["path", "content"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "apply_patch",
                    "description": "Apply JSON patch operations on file text",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "patch_ops": {"type": "array", "items": {"type": "object"}},
                        },
                        "required": ["path", "patch_ops"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "glob",
                    "description": "Find paths by glob pattern",
                    "parameters": {
                        "type": "object",
                        "properties": {"pattern": {"type": "string"}},
                        "required": ["pattern"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "rg_search",
                    "description": "Search text using ripgrep",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {"type": "string"},
                            "glob": {"type": "string"},
                            "max_results": {"type": "integer"},
                        },
                        "required": ["pattern"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "run_shell",
                    "description": "Run shell command in project root",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string"},
                            "approval_granted": {"type": "boolean"},
                        },
                        "required": ["command"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "git_status",
                    "description": "Get git status",
                    "parameters": {"type": "object", "properties": {}},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "git_diff",
                    "description": "Get git diff",
                    "parameters": {"type": "object", "properties": {}},
                },
            },
        ]

    def execute(
        self,
        *,
        project_root: Path,
        session_state: SessionPolicyState,
        name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        self.policy.assert_mutation_allowed(name, session_state)
        project_root = project_root.resolve()
        self.policy.assert_path_allowed(project_root)

        if name == "read_file":
            return read_file(self.policy, project_root, arguments["path"])
        if name == "write_file":
            return write_file(self.policy, project_root, arguments["path"], arguments["content"])
        if name == "apply_patch":
            return apply_json_patch(self.policy, project_root, arguments["path"], arguments["patch_ops"])
        if name == "glob":
            return glob_paths(self.policy, project_root, arguments["pattern"])
        if name == "rg_search":
            return rg_search(
                self.policy,
                project_root,
                arguments["pattern"],
                arguments.get("glob"),
                int(arguments.get("max_results", 100)),
            )
        if name == "run_shell":
            return run_shell(
                self.policy,
                project_root,
                arguments["command"],
                self.settings.shell_timeout_seconds,
                self.settings.max_output_chars,
                bool(arguments.get("approval_granted", False)),
            )
        if name == "git_status":
            return git_status(self.policy, project_root)
        if name == "git_diff":
            return git_diff(self.policy, project_root)
        raise ValueError(f"unknown tool: {name}")
