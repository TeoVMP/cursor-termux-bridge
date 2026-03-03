from __future__ import annotations

from pathlib import Path

from bridge_server.agent import AgentRuntime
from bridge_server.models import ApproveParams, ChatRunParams, JsonRpcError, JsonRpcRequest, JsonRpcResponse


async def dispatch_rpc(runtime: AgentRuntime, request: JsonRpcRequest) -> JsonRpcResponse:
    try:
        if request.method == "bridge.status":
            return JsonRpcResponse(id=request.id, result={"ok": True, "service": "gpt-codexbridge-server"})

        if request.method == "chat.run":
            params = ChatRunParams.model_validate(request.params)
            result = await runtime.run_chat(
                message=params.message,
                project_root=Path(params.project_root),
                session_id=params.session_id,
                max_steps=params.max_steps,
                plan_first=params.plan_first,
                require_approval=params.require_approval,
            )
            return JsonRpcResponse(id=request.id, result=result)

        if request.method == "chat.approve":
            params = ApproveParams.model_validate(request.params)
            runtime.set_approval(params.session_id, params.approve, params.reason)
            return JsonRpcResponse(id=request.id, result={"ok": True})

        return JsonRpcResponse(
            id=request.id,
            error=JsonRpcError(code=-32601, message=f"method not found: {request.method}"),
        )
    except Exception as exc:  # noqa: BLE001
        return JsonRpcResponse(
            id=request.id,
            error=JsonRpcError(code=-32000, message="internal error", data=str(exc)),
        )
