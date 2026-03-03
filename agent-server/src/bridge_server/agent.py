from __future__ import annotations

import asyncio
import json
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bridge_server.audit import AuditLogger
from bridge_server.llm import LmStudioAdapter
from bridge_server.policy import PolicyEngine, SessionPolicyState
from bridge_server.telemetry import Telemetry
from bridge_server.tools.router import ToolRouter


SYSTEM_PROMPT = (
    "You are a software engineering agent running through strict tools. "
    "Prefer tools for file reads/writes, search, and shell. "
    "Explain final outcomes clearly and briefly."
)


@dataclass(slots=True)
class SessionContext:
    session_id: str
    project_root: Path
    state: SessionPolicyState
    waiting_approval: bool = False
    pending_reason: str | None = None
    history: list[dict[str, Any]] | None = None
    lock: asyncio.Lock | None = None


class AgentRuntime:
    def __init__(
        self,
        *,
        llm: LmStudioAdapter,
        tools: ToolRouter,
        policy: PolicyEngine,
        audit: AuditLogger,
    ) -> None:
        self.llm = llm
        self.tools = tools
        self.policy = policy
        self.audit = audit
        self.sessions: dict[str, SessionContext] = {}
        self.telemetry = Telemetry()

    def get_or_create_session(
        self,
        *,
        session_id: str | None,
        project_root: Path,
        plan_first_default: bool,
    ) -> SessionContext:
        if session_id and session_id in self.sessions:
            return self.sessions[session_id]
        sid = session_id or str(uuid.uuid4())
        ctx = SessionContext(
            session_id=sid,
            project_root=project_root.resolve(),
            state=SessionPolicyState(plan_approved=not plan_first_default, plan_first=plan_first_default),
            history=[],
            lock=asyncio.Lock(),
        )
        self.sessions[sid] = ctx
        return ctx

    def set_approval(self, session_id: str, approve: bool, reason: str | None = None) -> None:
        if session_id not in self.sessions:
            raise ValueError("unknown session")
        ctx = self.sessions[session_id]
        ctx.state.plan_approved = approve
        ctx.waiting_approval = False
        ctx.pending_reason = reason
        self.audit.write(
            session_id=session_id,
            event="approval",
            payload={"approved": approve, "reason": reason},
        )

    async def run_chat(
        self,
        *,
        message: str,
        project_root: Path,
        session_id: str | None,
        max_steps: int,
        plan_first: bool | None,
        require_approval: bool,
    ) -> dict[str, Any]:
        ctx = self.get_or_create_session(
            session_id=session_id,
            project_root=project_root,
            plan_first_default=bool(plan_first) if plan_first is not None else True,
        )
        if plan_first is not None:
            ctx.state.plan_first = plan_first
            if not plan_first:
                ctx.state.plan_approved = True

        assert ctx.lock is not None
        async with ctx.lock:
            self.policy.assert_path_allowed(ctx.project_root)
            base_messages: list[dict[str, Any]] = [
                {"role": "system", "content": SYSTEM_PROMPT},
                *list(ctx.history or []),
                {
                    "role": "user",
                    "content": (
                        f"Project root: {ctx.project_root}\n"
                        f"Require approval for risky commands: {require_approval}\n"
                        f"Task: {message}"
                    ),
                },
            ]
            messages = base_messages
            self.telemetry.inc("chat_requests")

            for _ in range(max_steps):
                response = await self.llm.chat_completion(messages, self.tools.definitions())
                self.telemetry.inc("llm_calls")
                choice = response["choices"][0]["message"]
                tool_calls = choice.get("tool_calls", [])
                content = choice.get("content")

                if not tool_calls:
                    if ctx.history is not None:
                        ctx.history.extend(
                            [
                                {"role": "user", "content": message},
                                {"role": "assistant", "content": content or ""},
                            ]
                        )
                        if len(ctx.history) > 24:
                            ctx.history = ctx.history[-24:]
                    self.audit.write(session_id=ctx.session_id, event="final", payload={"content": content})
                    return {
                        "session_id": ctx.session_id,
                        "message": content or "",
                        "waiting_approval": ctx.waiting_approval,
                        "telemetry": self.telemetry.snapshot(),
                    }

                messages.append(
                    {
                        "role": "assistant",
                        "content": content,
                        "tool_calls": tool_calls,
                    }
                )

                for call in tool_calls:
                    name = call["function"]["name"]
                    arguments = json.loads(call["function"]["arguments"] or "{}")
                    if name == "run_shell" and require_approval and "approval_granted" not in arguments:
                        arguments["approval_granted"] = False
                    try:
                        result = self.tools.execute(
                            project_root=ctx.project_root,
                            session_state=ctx.state,
                            name=name,
                            arguments=arguments,
                        )
                        self.telemetry.inc(f"tool_ok_{name}")
                        self.audit.write(
                            session_id=ctx.session_id,
                            event="tool_ok",
                            payload={"tool": name, "arguments": arguments},
                        )
                    except Exception as exc:  # noqa: BLE001
                        result = {"error": str(exc)}
                        self.telemetry.inc(f"tool_error_{name}")
                        self.audit.write(
                            session_id=ctx.session_id,
                            event="tool_error",
                            payload={"tool": name, "arguments": arguments, "error": str(exc)},
                        )

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": call["id"],
                            "name": name,
                            "content": json.dumps(result, ensure_ascii=True),
                        }
                    )

                    if "requires approval" in str(result.get("error", "")):
                        ctx.waiting_approval = True
                        ctx.pending_reason = f"Tool {name} requires approval"
                        return {
                            "session_id": ctx.session_id,
                            "message": "Approval required before continuing.",
                            "waiting_approval": True,
                            "reason": ctx.pending_reason,
                            "telemetry": self.telemetry.snapshot(),
                        }

            return {
                "session_id": ctx.session_id,
                "message": "Max steps reached without final answer.",
                "waiting_approval": ctx.waiting_approval,
                "telemetry": self.telemetry.snapshot(),
            }
