from __future__ import annotations

import uvicorn
from fastapi import FastAPI, Header, HTTPException

from bridge_server.agent import AgentRuntime
from bridge_server.audit import AuditLogger
from bridge_server.config import Settings
from bridge_server.llm import LmStudioAdapter
from bridge_server.models import JsonRpcRequest
from bridge_server.policy import PolicyEngine
from bridge_server.rpc import dispatch_rpc
from bridge_server.tools.router import ToolRouter

settings = Settings.from_env()
policy = PolicyEngine(
    allowed_roots=settings.allowed_roots,
    blocked_commands=settings.blocked_commands,
    confirm_command_patterns=settings.confirm_command_patterns,
)
audit = AuditLogger(settings.audit_log_path)
llm = LmStudioAdapter(
    base_url=settings.lmstudio_base_url,
    api_key=settings.lmstudio_api_key,
    model_name=settings.model_name,
)
tools = ToolRouter(settings=settings, policy=policy)
runtime = AgentRuntime(llm=llm, tools=tools, policy=policy, audit=audit)

app = FastAPI(title="GPT-CodexBridge Server", version="0.1.0")


@app.get("/health")
async def health() -> dict[str, bool]:
    return {"ok": True}


@app.post("/rpc")
async def rpc_endpoint(payload: JsonRpcRequest, x_bridge_token: str | None = Header(default=None)) -> dict:
    if settings.api_token and x_bridge_token != settings.api_token:
        raise HTTPException(status_code=401, detail="invalid bridge token")
    response = await dispatch_rpc(runtime, payload)
    return response.model_dump(exclude_none=True)


def run() -> None:
    uvicorn.run(
        "bridge_server.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )


if __name__ == "__main__":
    run()
