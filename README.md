# Agent-Harmony Python

[![CI](https://github.com/michalszc/agent-harmony-python/actions/workflows/ci.yml/badge.svg)](https://github.com/michalszc/agent-harmony-python/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12%20%E2%80%93%203.14-blue)](pyproject.toml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)

Python bindings for the [Agent-Harmony](https://github.com/Tosiekdev/Agent-Harmony)
C++20 agent-based modeling library, built with nanobind, CMake, and scikit-build-core.

**Version 0.0.0 is a repository foundation milestone.** It provides an importable
package, version metadata, and a working native extension. Simulation classes and
Agent-Harmony feature bindings are not implemented yet.

## Installation

Use standard CPython 3.12, 3.13, or 3.14. After a release is available, install a
prebuilt wheel without a C++ compiler:

```bash
python -m pip install --only-binary=:all: agent-harmony
```

Wheels are configured for Linux x86_64 (glibc 2.28+), macOS Intel and Apple Silicon
(macOS 11+), and Windows x86_64 and ARM64. This initialization does not publish a
release. If a matching wheel is unavailable, the command above fails rather than
attempting a source build. The package has no Python runtime dependencies.

To build from a Git checkout, install a C++20 compiler, CMake 3.29+, Python
headers, and Git, then run:

```bash
git clone https://github.com/michalszc/agent-harmony-python.git
cd agent-harmony-python
git submodule update --init external/agent-harmony
python -m pip install .
```

Build isolation supplies the Python build tools and can supply CMake/Ninja when
needed. An sdist includes the required upstream sources and needs no Git
submodule initialization. See [installation details](documentation/getting-started/installation.md).

## Verify the package

```python
import agent_harmony

print(agent_harmony.__version__)  # 0.0.0
```

Importing the package loads its compiled `agent_harmony._core` extension.
See [the Python example](examples/basic_usage.py) and
[basic usage notebook](notebooks/basic_usage.ipynb).

## Development

Reuse the existing `.venv`; see [CONTRIBUTING.md](CONTRIBUTING.md) for setup,
Make commands, testing, and release procedures.

```bash
make submodules
make install-dev INSTALL_HOOKS=0
make check
make build
make check-build
make check-install
```

`make help` lists the interface. Quality checks include lint, formatting, strict
typing, tests, documentation, notebook validation, and hook configuration.
CI runs the full suite against each wheel on every configured Python/platform
combination, in addition to the main quality checks.

## Repository layout

| Directory | Purpose |
| --- | --- |
| `src/agent_harmony/` | Python package, native type stub, and typed marker |
| `cpp/bindings/` | nanobind extension and future bindings |
| `external/agent-harmony/` | Upstream Git submodule pinned to an exact commit |
| `tests/` | Installed-package and infrastructure contracts |
| `documentation/` | MkDocs sources and release notes |
| `docs/` | Generated documentation, ignored by Git |
| `examples/`, `notebooks/` | Minimal Python and notebook examples |
| `scripts/` | Build verification, validation, and release helpers |
| `.github/workflows/` | CI, CD, docs, notebooks, releases, and maintenance |

## License

The Python bindings and repository code are licensed under [Apache 2.0](LICENSE).
Agent-Harmony retains its upstream [MIT license](LICENSE-UPSTREAM). The compiled
extension incorporates nanobind under its [BSD 3-Clause license](LICENSE-NANOBIND).
All notices are included in wheels and source distributions; see [NOTICE](NOTICE).
