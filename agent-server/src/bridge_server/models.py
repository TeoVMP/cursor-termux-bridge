from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class JsonRpcRequest(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: str | int | None = None
    method: str
    params: dict[str, Any] = Field(default_factory=dict)


class JsonRpcError(BaseModel):
    code: int
    message: str
    data: Any | None = None


class JsonRpcResponse(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: str | int | None = None
    result: dict[str, Any] | None = None
    error: JsonRpcError | None = None


class ChatRunParams(BaseModel):
    message: str
    project_root: str
    session_id: str | None = None
    plan_first: bool | None = None
    require_approval: bool = True
    max_steps: int = 16


class ApproveParams(BaseModel):
    session_id: str
    approve: bool
    reason: str | None = None
