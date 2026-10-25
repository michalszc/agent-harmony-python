"""Cleaning must preserve the development environment and original sources."""

from importlib import util
from pathlib import Path

SPEC = util.spec_from_file_location(
    "clean", Path(__file__).parents[3] / "scripts" / "clean.py"
)
assert SPEC is not None and SPEC.loader is not None
CLEAN = util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLEAN)


def test_clean_preserves_sources_and_environment(tmp_path: Path) -> None:
    preserved = [
        ".venv/marker",
        ".git/marker",
        "documentation/index.md",
        "notebooks/basic_usage.ipynb",
        "external/agent-harmony/include/header.hpp",
        "src/agent_harmony/__init__.py",
        "release-metadata.json",
    ]
    generated = [
        "build/library.so",
        "dist/package.whl",
        "docs/index.html",
        ".pytest_cache/marker",
        "src/agent_harmony/__pycache__/module.pyc",
    ]
    for name in preserved + generated:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture")
    CLEAN.clean(tmp_path)
    assert all((tmp_path / name).is_file() for name in preserved)
    assert all(not (tmp_path / name).exists() for name in generated)
    CLEAN.clean(tmp_path)  # Repeated cleaning is harmless.
