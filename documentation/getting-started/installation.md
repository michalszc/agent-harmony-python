# Installation

## Prebuilt wheels

After a release is available, use:

```bash
python -m pip install --only-binary=:all: agent-harmony
```

The distribution is named `agent-harmony`; import it as `agent_harmony`.
Wheels require no compiler. Builds are configured for CPython 3.12–3.14 on Linux
x86_64 with glibc 2.28+, macOS 11+ on Intel and Apple Silicon, and Windows x86_64
and ARM64. Free-threaded Python, PyPy, 32-bit systems, and Alpine/musl wheels are
outside this initial matrix. No release is published as part of initialization.

## Build from source

Source builds require a C++20 compiler and Python development headers. CMake
3.29+ and Ninja are used; build isolation can install these tools when required.

```bash
git clone https://github.com/michalszc/agent-harmony-python.git
cd agent-harmony-python
git submodule update --init external/agent-harmony
python -m pip install .
```

Only initialize the direct Agent-Harmony submodule. Its nested SFML dependency
is unused. Git builds use the recorded commit; they never fetch an upstream
branch implicitly. Source archives include required upstream C++ inputs and
notices, so installing an sdist needs no Git checkout or submodule command.
Python build requirements may still need to be downloaded by pip.

See the [contribution guide](https://github.com/michalszc/agent-harmony-python/blob/master/CONTRIBUTING.md)
for editable native builds and developer dependencies.
