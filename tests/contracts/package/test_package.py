"""Smoke tests shared by editable, wheel, and sdist installations."""

from importlib import machinery, metadata, resources

import agent_harmony
from agent_harmony import _core


def test_package_import() -> None:
    assert agent_harmony.__name__ == "agent_harmony"


def test_package_version() -> None:
    assert agent_harmony.__version__ == metadata.version("agent-harmony")
    assert agent_harmony.__version__ == _core.__version__


def test_native_extension_loaded() -> None:
    assert _core.__file__ is not None
    assert any(
        _core.__file__.endswith(suffix) for suffix in machinery.EXTENSION_SUFFIXES
    )


def test_package_is_typed() -> None:
    package = resources.files("agent_harmony")
    assert package.joinpath("py.typed").is_file()
    assert package.joinpath("_core.pyi").is_file()
