import asyncio

from bridge_server.models import JsonRpcRequest
from bridge_server.rpc import dispatch_rpc


class DummyRuntime:
    async def run_chat(self, **kwargs):  # noqa: ANN003
        return {"session_id": "s1", "message": "ok", "waiting_approval": False}

    def set_approval(self, session_id: str, approve: bool, reason: str | None = None) -> None:
        _ = (session_id, approve, reason)


def test_rpc_status() -> None:
    req = JsonRpcRequest(method="bridge.status")
    res = asyncio.run(dispatch_rpc(DummyRuntime(), req))  # type: ignore[arg-type]
    assert res.result is not None
    assert res.result["ok"] is True
