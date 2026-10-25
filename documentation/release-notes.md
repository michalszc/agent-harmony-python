# Release notes

## 0.0.0 — 2026-10-25

- Established `agent-harmony` packaging and the typed `agent_harmony` import.
- Added a metadata-only nanobind extension, CMake/scikit-build-core build, and a
  pinned Agent-Harmony Git submodule with Apache, MIT, and nanobind notices.
- Added wheel/sdist archive checks, clean wheel installation, and source-archive
  rebuilding without C++ dependency downloads.
- Retained the existing CI/CD, documentation, notebook, release, and stale
  workflows; extended wheel jobs to test the full suite on Python 3.12–3.14
  across Linux x86_64, both macOS architectures, and Windows x86_64/ARM64.
- Added package examples, developer guidance, and a consistent Make interface.
- No simulation functionality is implemented in this milestone.
