from pathlib import Path

import pytest

from bridge_server.validators import ValidationError, validate_content_for_path


def test_python_validator_ok() -> None:
    validate_content_for_path(Path("ok.py"), "def x():\n    return 1\n")


def test_python_validator_error() -> None:
    with pytest.raises(ValidationError):
        validate_content_for_path(Path("bad.py"), "def x(:\n    pass\n")


def test_json_validator_error() -> None:
    with pytest.raises(ValidationError):
        validate_content_for_path(Path("bad.json"), "{oops}")
