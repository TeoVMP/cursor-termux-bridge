from __future__ import annotations

from typing import Any

import httpx


class BridgeClient:
    def __init__(self, server_url: str, token: str = "") -> None:
        self.server_url = server_url.rstrip("/")
        self.token = token
        self._id = 0

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    def call(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": method,
            "params": params,
        }
        with httpx.Client(timeout=180) as client:
            headers = {"x-bridge-token": self.token} if self.token else {}
            resp = client.post(f"{self.server_url}/rpc", json=payload, headers=headers)
            resp.raise_for_status()
            body = resp.json()
        if "error" in body:
            raise RuntimeError(f"RPC error {body['error'].get('code')}: {body['error'].get('message')}")
        return body["result"]
