"""Remove known generated artifacts while preserving sources and environments."""

from __future__ import annotations

import shutil
from pathlib import Path


def remove(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def clean(root: Path) -> None:
    for name in (
        "build",
        "dist",
        "wheelhouse",
        "docs",
        "site",
        "htmlcov",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".coverage",
        "coverage.xml",
        "test_output.txt",
        "lint_output.txt",
        "format_output.txt",
        "mypy_output.txt",
        "version_output.txt",
        "notebooks_output.txt",
        "publish_output.txt",
    ):
        remove(root / name)
    for source in (root / "src", root / "tests", root / "scripts", root / "examples"):
        if source.is_dir():
            for cache in source.rglob("__pycache__"):
                remove(cache)
    for parent in (root, root / "src"):
        for metadata in parent.glob("*.egg-info"):
            remove(metadata)


if __name__ == "__main__":
    clean(Path(__file__).resolve().parents[1])
