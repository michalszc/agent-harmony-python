"""Inspect distribution archives without installing or publishing anything."""

from __future__ import annotations

import argparse
import tarfile
import tomllib
import zipfile
from email.parser import BytesParser
from pathlib import Path

LICENSES = {"LICENSE", "LICENSE-UPSTREAM", "LICENSE-NANOBIND", "NOTICE"}


def check_metadata(data: bytes, name: str, version: str) -> None:
    metadata = BytesParser().parsebytes(data)
    if metadata["Name"] != name or metadata["Version"] != version:
        raise ValueError("Distribution identity does not match pyproject.toml")
    if metadata.get_all("Requires-Dist"):
        raise ValueError("The infrastructure package must have no runtime dependencies")
    if set(metadata.get_all("License-File", [])) != LICENSES:
        raise ValueError("Distribution license metadata is incomplete")


def check_wheel(path: Path, name: str, version: str) -> None:
    with zipfile.ZipFile(path) as wheel:
        files = set(wheel.namelist())
        metadata_files = [f for f in files if f.endswith(".dist-info/METADATA")]
        if len(metadata_files) != 1:
            raise ValueError("Expected exactly one wheel metadata file")
        check_metadata(wheel.read(metadata_files[0]), name, version)
        dist_info = metadata_files[0].removesuffix("METADATA")
        required = {
            "agent_harmony/__init__.py",
            "agent_harmony/_core.pyi",
            "agent_harmony/py.typed",
            *(dist_info + "licenses/" + license_file for license_file in LICENSES),
        }
        if not required <= files:
            raise ValueError(f"Missing wheel files: {required - files}")
        extensions = [
            f
            for f in files
            if f.startswith("agent_harmony/_core.") and f.endswith((".so", ".pyd"))
        ]
        if len(extensions) != 1:
            raise ValueError("Expected exactly one native extension")
        wheel_metadata = BytesParser().parsebytes(wheel.read(dist_info + "WHEEL"))
        if wheel_metadata["Root-Is-Purelib"] != "false":
            raise ValueError("Native wheel must not be marked as pure Python")
        if any(f.startswith(("external/", "cpp/", "tests/")) for f in files):
            raise ValueError("Wheel contains development-only sources")


def check_sdist(path: Path, name: str, version: str) -> None:
    with tarfile.open(path) as archive:
        members = archive.getmembers()
        if any(m.issym() or m.islnk() or m.isdev() for m in members):
            raise ValueError("Source archive contains links or special files")
        files = {"/".join(m.name.split("/")[1:]) for m in members if m.isfile()}
        required = {
            "pyproject.toml",
            "CMakeLists.txt",
            "PKG-INFO",
            "cpp/bindings/CMakeLists.txt",
            "cpp/bindings/module.cpp",
            "src/agent_harmony/__init__.py",
            "src/agent_harmony/_core.pyi",
            "src/agent_harmony/py.typed",
            "external/agent-harmony/include/space/Point.hpp",
            "external/agent-harmony/src/experimental/visualization/Visualization.cpp",
            "external/agent-harmony/CMakeLists.txt",
            "external/agent-harmony/LICENSE",
            *LICENSES,
        }
        if not required <= files:
            raise ValueError(f"Missing sdist files: {required - files}")
        forbidden = {".git", ".venv", "SFML", "__pycache__"}
        if any(forbidden.intersection(Path(f).parts) for f in files):
            raise ValueError("Source archive contains excluded development files")
        metadata = next(m for m in members if m.name.endswith("/PKG-INFO"))
        stream = archive.extractfile(metadata)
        if stream is None:
            raise ValueError("Source metadata is unreadable")
        check_metadata(stream.read(), name, version)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=Path("dist"))
    parser.add_argument("--require-wheels", type=int, default=1)
    args = parser.parse_args()
    with Path("pyproject.toml").open("rb") as stream:
        project = tomllib.load(stream)["project"]
    wheels = sorted(args.dist.glob("*.whl"))
    sdists = sorted(args.dist.glob("*.tar.gz"))
    if len(sdists) != 1 or len(wheels) != args.require_wheels:
        raise ValueError("Unexpected number of distribution artifacts")
    for path in wheels:
        check_wheel(path, project["name"], project["version"])
    check_sdist(sdists[0], project["name"], project["version"])
    print(f"Validated {len(wheels)} wheel(s) and one sdist")


if __name__ == "__main__":
    main()
