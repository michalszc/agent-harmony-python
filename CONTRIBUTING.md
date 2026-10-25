# Contributing to Agent-Harmony Python

Version 0.0.0 establishes packaging and development infrastructure. No simulation
API is implemented. Before adding bindings or helper behavior, inspect the
upstream headers and existing repository tooling for an implementation to reuse.

## Source installation and binary compatibility

Release wheels are configured for standard CPython 3.12, 3.13, and 3.14 on Linux
x86_64 (glibc 2.28+), macOS Intel and Apple Silicon (macOS 11+), and Windows
x86_64 and ARM64. Prebuilt wheels require no C++ compiler or Python runtime
dependencies. To require a compatible wheel rather than fall back to compilation:

```bash
python -m pip install --only-binary=:all: agent-harmony
```

This command fails if a matching wheel is unavailable. Source builds require a
C++20 compiler, CMake 3.29+, Python development headers, and Git for checkouts:

```bash
git clone https://github.com/michalszc/agent-harmony-python.git
cd agent-harmony-python
git submodule update --init external/agent-harmony
python -m pip install .
```

Build isolation supplies the Python build tools and can supply CMake/Ninja when
needed. An sdist includes required upstream sources and needs no Git submodule
initialization. See [installation details](documentation/getting-started/installation.md).
For editable contributor builds and checks, follow the environment setup below.

## Environment setup

Use CPython 3.12–3.14, Git, a C++20 compiler, CMake 3.29+, GNU Make, and `jq`.
On Linux, install Python development headers. Windows source development uses
Visual Studio C++ tools and Git Bash; Make and jq must be on PATH. Supported
end users installing wheels need neither the compiler nor these developer tools.

Reuse the existing `.venv`. New contributors without one may create it with
`python -m venv .venv`. Make detects `.venv/bin/python` or
`.venv/Scripts/python.exe`; override with `make PYTHON=...` if needed.

```bash
make submodules
make install-dev INSTALL_HOOKS=0
```

`install-dev` installs the `dev` dependency groups, then builds an editable
extension without build isolation. It ensures pip supports dependency groups.
Use `make install-dev` to install the optional pre-commit hooks too. Their first
run may download hook environments. `make hooks-check` validates configuration
without installing hooks. Ask before installing or upgrading dependencies in
another contributor's existing environment.

After changing C++, upstream headers, or the version in `pyproject.toml`, rebuild:

```bash
make install INSTALL_ARGS=--no-build-isolation
```

An editable install does not automatically recompile C++ on import. Never create
an alternative environment to replace an existing contributor environment.

## Focused changes and commits

1. Work on a feature branch; this initialization uses `feature/init`.
2. Make one focused change, reusing existing methods where available.
3. Validate it with relevant Make commands and fix failures before continuing.
4. Review and commit using Conventional Commits, for example
   `build: add upstream header integration`.
5. Continue to the next area only after the validated commit.

```bash
make check
make test TEST_PATH=tests/contracts/package
make test PYTEST_ARGS="-k import"
make ci-check CHECK=test
```

`make check` runs Ruff lint/format checks, strict mypy, pytest, offline version
validation, strict MkDocs, examples, notebook validation, and hook configuration.
Use `make format` and `make lint-fix` for corrections. Tests cover package
imports, native loading, typed resources, archive rejection, validation failures,
and release identity/retry behavior. Publication tests replace external commands
with controlled fakes; they never upload anything.

## Project layout and native integration

| Directory | Purpose |
| --- | --- |
| `src/agent_harmony/` | Python interface, `_core.pyi`, and typed marker |
| `cpp/bindings/` | nanobind extension sources and future bindings |
| `external/agent-harmony/` | Upstream Git submodule pinned to an exact commit |
| `tests/contracts/` | Installed-package and repository infrastructure tests |
| `documentation/` | MkDocs sources, API templates, and release notes |
| `docs/` | Generated documentation, ignored by Git |
| `examples/`, `notebooks/` | Maintained Python and notebook examples |
| `assets/` | Project assets |
| `scripts/` | Build verification, validation, and release helpers |
| `.github/workflows/` | CI, CD, docs, notebooks, releases, and maintenance |

The initial module includes an upstream header to verify integration and exposes
only version metadata. Root CMake provides a header interface instead of invoking
upstream's experimental SFML visualization target. Do not initialize nested SFML
for this milestone. Future feature bindings must first inspect upstream types,
ownership rules, and supported methods.

To update upstream deliberately, check out the reviewed commit inside the
submodule, update `external/README.md`, preserve its notices, rebuild, and run
checks. Commit the changed gitlink with the integration change. Keep parent
repository sources separate from external dependency sources.

## Documentation and notebooks

The existing documentation layout is retained. `make docs` builds
`documentation/` into `docs/`; `make docs-serve` starts a local preview.
Mkdocstrings is ready for future implemented APIs. Keep its compatible
`pymdown-extensions<12` dependency constraint.

`make notebooks-check` validates JSON/schema, saved execution counts, stored
errors, and version output without executing notebook cells. The basic notebook
contains only an import and version print. Update its saved version after a
version change. Installation cells must remain unexecuted.

## Distribution checks

```bash
make build
make check-build
make check-install
```

`make build` creates an sdist and builds a wheel from that sdist. Required
upstream headers/sources and all notices are explicitly included; environments,
Git internals, SFML, and generated artifacts are excluded. Missing upstream
sources fail the CMake configuration with initialization instructions.

`check-build` runs Twine metadata checks and inspects archive contents.
`check-install` installs the local wheel into a disposable environment outside
the checkout with binary-only/no-index settings, then rebuilds and installs a
wheel from the extracted sdist with dependency downloads disabled. It reuses
approved build tools and does not replace the development `.venv`.

`make clean` removes generated builds, distributions, docs, and caches while
preserving source files, notebooks, `.venv`, and the upstream submodule. Reinstall
the editable package after cleaning because its native build is removed.

## CI and releases

The existing workflow sequence remains **CI → CD → Release**. Docs, notebooks,
and stale maintenance retain their dedicated workflows.

CI keeps `test` in the main quality matrix. Wheel jobs also run the **entire test
suite** through `make test` for CPython 3.12, 3.13, and 3.14 on Linux x86_64,
macOS Intel, macOS Apple Silicon, Windows x86_64, and native Windows ARM64.
The Apple Silicon runner uses `macos-latest`; Intel uses `macos-26-intel`.
Cibuildwheel creates and tests each interpreter's wheel in its own environment.
Linux containers install jq, Make, and Git for the infrastructure tests. Windows
jobs ensure Make and jq are available and use Git Bash for shell helpers.
A separate source-distribution job verifies the sdist and clean installation.

Markdown, README, contribution, license, and notice-only changes do not trigger
CI. Code, build inputs, tests, dependency pins, and release automation do.
Documentation and notebook changes use their own workflows. Mixed code/docs
changes still run CI. Ordinary PRs cannot publish packages or deploy Pages.

For a publishing change:

1. Update the version in `pyproject.toml` and rebuild the editable extension.
   CMake passes that version to `_core`; Python re-exports it.
2. Add exactly one nonempty version section in
   `documentation/release-notes.md` and update the notebook's saved output.
3. Run the quality, archive, and installation checks.
4. After a reviewed merge to `master`, successful push CI triggers CD for that
   exact commit. CD downloads that CI run's 15 tested wheels and sdist, checks
   their identity and notices, installs a compatible wheel, checks PyPI version
   availability, records deployment identity, and publishes without rebuilding.
5. Successful CD triggers Release, which retrieves metadata from that CD run,
   checks out the deployed commit, and creates the matching tag/release.

`make validate-version` is offline by default. Use
`make validate-version VALIDATE_VERSION_ARGS=` for the read-only PyPI comparison.
Only HTTP 404 is treated as an unpublished project; network/service failures
fail the check. An already published version fails publication validation.
A publishing master push therefore needs an unpublished version. An
infrastructure-only change may retain a version locally, but CD will reject an
attempt to republish it.

All manual commands remain available: `make publish-test`, `make publish`,
`make ci-publish`, and `make release` perform external publication. Normal checks
never invoke them except within isolated mocked tests.

**Agent execution rule:** agents working on repository initialization must not
run publication/release-creation commands, push changes, or trigger publishing
workflows. They may inspect those commands and run mocked tests. Actual
publication requires a separate, explicit user instruction. The commands remain
available and automation remains enabled.

`make release-metadata` only records `sha`, `name`, and `version`; it does not
publish. `make release-select-commit` validates metadata and writes its SHA to
`GITHUB_OUTPUT`. `RELEASE_METADATA`, `RELEASE_PROJECT`, and
`RELEASE_REPOSITORY` select the deployment inputs for manual recovery.

### Maintainer settings and recovery

Configure externally, when ready:

- GitHub Pages with Actions and deployment from `master`.
- A project-scoped `PYPI_API_TOKEN` repository secret for `agent-harmony`.
- Actions token permissions for artifact reads and GitHub release writes.
- The `no-activity` label used by unchanged stale maintenance automation.

No credentials belong in the repository. The first workflow chain must be
verified on GitHub after the workflow files reach the default branch. Local
validation cannot establish the results on remote operating systems.

If GitHub release creation fails after PyPI publication, rerun the failed Release
job while its metadata artifact is available. Do not rerun CD merely to recover
a GitHub release. Matching published releases are preserved; conflicting tags,
draft releases, or mismatched deployment metadata fail for maintainer review.
