from __future__ import annotations

import os
import subprocess
from pathlib import Path

import typer

from bridge_cli.client import BridgeClient
from bridge_cli.render import print_kv, print_result

app = typer.Typer(help="Termux bridge client for GPT-CodexBridge")


def _server_default() -> str:
    return os.getenv("BRIDGE_SERVER_URL", "http://127.0.0.1:8765")


def _token_default() -> str:
    return os.getenv("BRIDGE_API_TOKEN", "")


def _client(server: str, token: str) -> BridgeClient:
    return BridgeClient(server_url=server, token=token)


@app.command("status")
def status(
    server: str = typer.Option(default_factory=_server_default, help="Bridge server URL"),
    token: str = typer.Option(default_factory=_token_default, help="Bridge API token"),
) -> None:
    result = _client(server, token).call("bridge.status", {})
    print_kv(result)


@app.command("chat")
def chat(
    message: str = typer.Option(..., help="Task request"),
    project: str = typer.Option(..., help="Absolute project root path in host server"),
    server: str = typer.Option(default_factory=_server_default, help="Bridge server URL"),
    token: str = typer.Option(default_factory=_token_default, help="Bridge API token"),
    session_id: str | None = typer.Option(None, help="Reuse previous session id"),
    max_steps: int = typer.Option(16, help="Maximum tool loop steps"),
    plan_first: bool = typer.Option(True, help="Block mutating actions until approval"),
) -> None:
    result = _client(server, token).call(
        "chat.run",
        {
            "message": message,
            "project_root": project,
            "session_id": session_id,
            "max_steps": max_steps,
            "plan_first": plan_first,
            "require_approval": True,
        },
    )
    print_kv({"session_id": result.get("session_id"), "waiting_approval": result.get("waiting_approval")})
    print_result("assistant", result.get("message", ""))


@app.command("approve")
def approve(
    session_id: str = typer.Option(..., help="Session to approve/reject"),
    server: str = typer.Option(default_factory=_server_default, help="Bridge server URL"),
    token: str = typer.Option(default_factory=_token_default, help="Bridge API token"),
    deny: bool = typer.Option(False, help="Reject instead of approve"),
    reason: str = typer.Option("", help="Optional reason"),
) -> None:
    result = _client(server, token).call(
        "chat.approve",
        {"session_id": session_id, "approve": not deny, "reason": reason or None},
    )
    print_kv(result)


@app.command("run-task")
def run_task(
    message: str = typer.Option(..., help="Task request"),
    project: str = typer.Option(..., help="Absolute project root path in host server"),
    server: str = typer.Option(default_factory=_server_default, help="Bridge server URL"),
    token: str = typer.Option(default_factory=_token_default, help="Bridge API token"),
    auto_approve: bool = typer.Option(False, help="Auto approve when needed"),
) -> None:
    result = _client(server, token).call(
        "chat.run",
        {
            "message": message,
            "project_root": project,
            "max_steps": 24,
            "plan_first": True,
            "require_approval": True,
        },
    )
    print_kv({"session_id": result.get("session_id"), "waiting_approval": result.get("waiting_approval")})
    print_result("assistant", result.get("message", ""))

    if result.get("waiting_approval") and auto_approve:
        sid = result["session_id"]
        _client(server, token).call(
            "chat.approve",
            {"session_id": sid, "approve": True, "reason": "auto_approve"},
        )
        resumed = _client(server, token).call(
            "chat.run",
            {
                "message": "continue the task after approval",
                "project_root": project,
                "session_id": sid,
                "max_steps": 24,
                "plan_first": True,
                "require_approval": True,
            },
        )
        print_result("assistant", resumed.get("message", ""))


@app.command("git-flow")
def git_flow(
    project: str = typer.Option(..., help="Local repo path in termux"),
    branch: str = typer.Option(..., help="Branch name to create/use"),
    commit_message: str = typer.Option(..., help="Commit message"),
    push: bool = typer.Option(False, help="Push branch to origin"),
) -> None:
    repo = Path(project).resolve()
    subprocess.run(["git", "checkout", "-B", branch], cwd=repo, check=True)
    subprocess.run(["git", "status", "--short"], cwd=repo, check=False)
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", commit_message], cwd=repo, check=True)
    if push:
        subprocess.run(["git", "push", "-u", "origin", branch], cwd=repo, check=True)
    print_result("git-flow", "Workflow completed")


if __name__ == "__main__":
    app()
