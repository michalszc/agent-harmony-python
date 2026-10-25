"""Exercise the executable resolution used by shell-based contract tests."""

import subprocess
from pathlib import Path

import pytest

from tests._shell import bash_executable


def test_bash_is_launched_by_absolute_path() -> None:
    executable = bash_executable()
    assert Path(executable).is_absolute()
    result = subprocess.run(
        [executable, "-c", "printf '%s' \"$BASH_VERSION\""],
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout


def test_missing_bash_has_actionable_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("tests._shell.shutil.which", lambda command: None)
    with pytest.raises(RuntimeError, match="Git Bash"):
        bash_executable()
