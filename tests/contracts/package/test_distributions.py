"""Reject incomplete or mislabeled artifacts before release."""

from __future__ import annotations

import zipfile
from importlib import util
from pathlib import Path

import pytest

SPEC = util.spec_from_file_location(
    "check_dist", Path(__file__).parents[3] / "scripts" / "check_dist.py"
)
assert SPEC is not None and SPEC.loader is not None
CHECK = util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


def test_rejects_wrong_version() -> None:
    with pytest.raises(ValueError, match="identity"):
        CHECK.check_metadata(
            b"Name: agent-harmony\nVersion: 9.0.0\n", "agent-harmony", "0.0.0"
        )


def test_rejects_runtime_dependency() -> None:
    with pytest.raises(ValueError, match="runtime dependencies"):
        CHECK.check_metadata(
            b"Name: agent-harmony\nVersion: 0.0.0\nRequires-Dist: pandas\n",
            "agent-harmony",
            "0.0.0",
        )


def test_rejects_missing_notices() -> None:
    with pytest.raises(ValueError, match="license metadata"):
        CHECK.check_metadata(
            b"Name: agent-harmony\nVersion: 0.0.0\n", "agent-harmony", "0.0.0"
        )


def test_rejects_wheel_without_metadata(tmp_path: Path) -> None:
    wheel = tmp_path / "broken.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr("agent_harmony/__init__.py", "")
    with pytest.raises(ValueError, match="metadata"):
        CHECK.check_wheel(wheel, "agent-harmony", "0.0.0")
