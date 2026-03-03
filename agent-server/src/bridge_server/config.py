from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _split_paths(raw: str) -> list[Path]:
    if not raw.strip():
        return []
    return [Path(p.strip()).resolve() for p in raw.split(";") if p.strip()]


def _split_words(raw: str) -> list[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]


@dataclass(slots=True)
class Settings:
    host: str
    port: int
    lmstudio_base_url: str
    lmstudio_api_key: str
    model_name: str
    api_token: str
    allowed_roots: list[Path]
    blocked_commands: list[str]
    confirm_command_patterns: list[str]
    shell_timeout_seconds: int
    max_output_chars: int
    audit_log_path: Path
    plan_first_default: bool

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            host=os.getenv("BRIDGE_HOST", "0.0.0.0"),
            port=int(os.getenv("BRIDGE_PORT", "8765")),
            lmstudio_base_url=os.getenv("BRIDGE_LMSTUDIO_BASE_URL", "http://127.0.0.1:1234/v1"),
            lmstudio_api_key=os.getenv("BRIDGE_LMSTUDIO_API_KEY", "lm-studio"),
            model_name=os.getenv("BRIDGE_MODEL_NAME", "local-model"),
            api_token=os.getenv("BRIDGE_API_TOKEN", ""),
            allowed_roots=_split_paths(os.getenv("BRIDGE_ALLOWED_ROOTS", "")),
            blocked_commands=_split_words(
                os.getenv("BRIDGE_BLOCKED_COMMANDS", "del,rm,format,shutdown,reboot,powershell -enc")
            ),
            confirm_command_patterns=_split_words(
                os.getenv("BRIDGE_CONFIRM_COMMAND_PATTERNS", "pip install,npm install,git push,git reset")
            ),
            shell_timeout_seconds=int(os.getenv("BRIDGE_SHELL_TIMEOUT_SECONDS", "30")),
            max_output_chars=int(os.getenv("BRIDGE_MAX_OUTPUT_CHARS", "12000")),
            audit_log_path=Path(os.getenv("BRIDGE_AUDIT_LOG_PATH", "logs/audit.jsonl")).resolve(),
            plan_first_default=os.getenv("BRIDGE_PLAN_FIRST_DEFAULT", "true").lower() == "true",
        )
