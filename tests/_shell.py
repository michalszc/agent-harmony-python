"""Resolve shell tools before handing them to native process creation."""

import shutil


def bash_executable() -> str:
    """Use PATH explicitly so Windows cannot prefer the system WSL launcher."""
    executable = shutil.which("bash")
    if executable is None:
        raise RuntimeError(
            "Bash is required for shell tests; install Git Bash on Windows"
        )
    return executable
