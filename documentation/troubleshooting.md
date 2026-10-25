# Troubleshooting

## Package import fails

Install into the Python environment you are using, and select the same notebook
kernel. The package name on PyPI is `agent-harmony`; the import is `agent_harmony`.

## The native `_core` module is missing

A source checkout alone is not an installed native package. Run `make submodules`
and install the package. After cleaning or changing C++ sources, rebuild with:

```bash
make install INSTALL_ARGS=--no-build-isolation
```

For source builds, ensure a C++20 compiler and Python development headers are
available. Prebuilt wheels require no compiler.

## No matching binary distribution

Check your interpreter, CPU architecture, and platform against
[installation support](getting-started/installation.md). The binary-only install
command intentionally fails if no compatible wheel is available. Source builds
require developer tools.

## Missing upstream headers

Run `git submodule update --init external/agent-harmony` from the checkout.
An extracted sdist already contains its required upstream sources.

## Version validation reports an old native build

After changing `pyproject.toml`, rebuild the editable extension. The Python
version is re-exported from the compiled module, rather than duplicated in source.

## Documentation dependency conflict

Use the constrained docs dependency group. The retained mkdocstrings toolchain
uses `pymdown-extensions>=10,<12`; installing incompatible versions can break
strict documentation builds.
