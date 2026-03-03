from __future__ import annotations

import ast
import json
from pathlib import Path


class ValidationError(ValueError):
    pass


def validate_content_for_path(path: Path, content: str) -> None:
    suffix = path.suffix.lower()
    if suffix == ".py":
        try:
            ast.parse(content)
        except SyntaxError as exc:
            raise ValidationError(f"python syntax error: {exc.msg}") from exc
    elif suffix == ".json":
        try:
            json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValidationError(f"json syntax error: {exc.msg}") from exc
