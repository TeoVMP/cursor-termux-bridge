from __future__ import annotations

from pathlib import Path

import jsonpatch

from bridge_server.policy import PolicyEngine
from bridge_server.validators import validate_content_for_path


def _resolve_in_root(project_root: Path, rel_path: str) -> Path:
    return (project_root / rel_path).resolve()


def read_file(policy: PolicyEngine, project_root: Path, rel_path: str) -> dict[str, str]:
    target = _resolve_in_root(project_root, rel_path)
    policy.assert_path_allowed(target)
    content = target.read_text(encoding="utf-8")
    return {"path": str(target), "content": content}


def write_file(
    policy: PolicyEngine,
    project_root: Path,
    rel_path: str,
    content: str,
) -> dict[str, str]:
    target = _resolve_in_root(project_root, rel_path)
    policy.assert_path_allowed(target)
    validate_content_for_path(target, content)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return {"path": str(target), "status": "written"}


def apply_json_patch(
    policy: PolicyEngine,
    project_root: Path,
    rel_path: str,
    patch_ops: list[dict],
) -> dict[str, str]:
    target = _resolve_in_root(project_root, rel_path)
    policy.assert_path_allowed(target)
    original = target.read_text(encoding="utf-8") if target.exists() else ""
    patched = jsonpatch.apply_patch({"text": original}, patch_ops, in_place=False)["text"]
    validate_content_for_path(target, patched)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(patched, encoding="utf-8")
    return {"path": str(target), "status": "patched"}
