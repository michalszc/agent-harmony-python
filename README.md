# Agent-Harmony Python

<p align="center">
  <a href="https://pypi.org/project/agent-harmony/"><img src="https://img.shields.io/pypi/v/agent-harmony" alt="PyPI version"></a>
  <a href="https://pypi.org/project/agent-harmony/"><img src="https://img.shields.io/pypi/dm/agent-harmony" alt="PyPI monthly downloads"></a>
  <a href="https://github.com/michalszc/agent-harmony-python/blob/master/pyproject.toml"><img src="https://img.shields.io/badge/python-3.12%2B-important" alt="Python 3.12 or newer"></a>
  <a href="https://github.com/michalszc/agent-harmony-python/actions/workflows/ci.yml"><img src="https://github.com/michalszc/agent-harmony-python/actions/workflows/ci.yml/badge.svg?branch=master" alt="CI on master"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg" alt="License: Apache 2.0"></a>
  <a href="https://michalszc.github.io/agent-harmony-python/"><img src="https://img.shields.io/badge/docs-online-blue.svg" alt="Docs"></a>
</p>

Python bindings for [Agent-Harmony](https://github.com/Tosiekdev/Agent-Harmony),
an agent-based modeling library.

**Version 0.0.0 is the initial package foundation.** You can import the package
and inspect its version. Simulation classes and Agent-Harmony feature bindings
are not implemented yet.

## Installation

Once a release is available on PyPI:

```bash
pip install agent-harmony
```

Python 3.12 or newer is required.

## Quick start

```python
import agent_harmony

print(agent_harmony.__version__)  # 0.0.0
```

## Documentation

- [Online documentation](https://michalszc.github.io/agent-harmony-python/)
- [Getting started](https://michalszc.github.io/agent-harmony-python/getting-started/)
- [API reference](https://michalszc.github.io/agent-harmony-python/reference/)
- [Release notes](https://michalszc.github.io/agent-harmony-python/release-notes/)

## Examples

- [Basic Python example](examples/basic_usage.py)
- [Basic usage notebook](examples/basic_usage.ipynb)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for source installation, development setup,
repository layout, testing, and release procedures.

## License

Licensed under [Apache 2.0](LICENSE). Upstream Agent-Harmony retains its
[MIT license](LICENSE-UPSTREAM). Additional bundled notices are included in
[LICENSE-NANOBIND](LICENSE-NANOBIND) and [NOTICE](NOTICE).
