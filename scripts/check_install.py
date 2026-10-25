"""Test built distributions in disposable environments outside the checkout."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tarfile
import venv
from pathlib import Path
from tempfile import TemporaryDirectory

SMOKE = """
from importlib import machinery, metadata, resources
import agent_harmony
from agent_harmony import _core
assert agent_harmony.__version__ == metadata.version('agent-harmony')
assert _core.__version__ == agent_harmony.__version__
assert any(_core.__file__.endswith(s) for s in machinery.EXTENSION_SUFFIXES)
assert resources.files('agent_harmony').joinpath('py.typed').is_file()
assert resources.files('agent_harmony').joinpath('_core.pyi').is_file()
assert 'site-packages' in _core.__file__
print('Installed native package:', agent_harmony.__version__)
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=Path("dist"))
    args = parser.parse_args()
    wheels = list(args.dist.resolve().glob("*.whl"))
    sdists = list(args.dist.resolve().glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise ValueError(
            "Build exactly one local wheel and sdist before installation checks"
        )
    environment = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    with TemporaryDirectory(prefix="agent-harmony-install-") as temporary:
        root = Path(temporary)
        target = root / "environment"
        venv.create(target, with_pip=True)
        python = target / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        subprocess.run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--no-index",
                "--no-deps",
                "--only-binary=:all:",
                str(wheels[0]),
            ],
            cwd=root,
            env=environment,
            check=True,
        )
        subprocess.run(
            [str(python), "-I", "-c", SMOKE], cwd=root, env=environment, check=True
        )
        source = root / "source"
        with tarfile.open(sdists[0]) as archive:
            archive.extractall(source, filter="data")
        project = next(source.iterdir())
        # Reuse approved build tools; the source build has no Git metadata and
        # cannot download upstream sources or Python build dependencies.
        environment["PIP_NO_INDEX"] = "1"
        environment["CMAKE_ARGS"] = "-DFETCHCONTENT_FULLY_DISCONNECTED=ON"
        subprocess.run(
            [
                sys.executable,
                "-m",
                "build",
                "--wheel",
                "--no-isolation",
                "--outdir",
                str(root / "rebuilt"),
                str(project),
            ],
            cwd=root,
            env=environment,
            check=True,
        )
        rebuilt = next((root / "rebuilt").glob("*.whl"))
        subprocess.run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--no-index",
                "--no-deps",
                "--force-reinstall",
                str(rebuilt),
            ],
            cwd=root,
            env=environment,
            check=True,
        )
        subprocess.run(
            [str(python), "-I", "-c", SMOKE], cwd=root, env=environment, check=True
        )


if __name__ == "__main__":
    main()
