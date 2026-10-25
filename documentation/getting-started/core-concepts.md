# Core concepts

The upstream C++ library supplies modeling, scheduling, and spatial types.
Version 0.0.0 does not expose these types to Python. Binding ownership, lifetimes,
and public API conventions will be documented when those features are added.

Current architecture separates the Python package in `src/agent_harmony`,
nanobind sources in `cpp/bindings`, and upstream code in a pinned Git submodule.
The initial extension includes a real upstream header without exposing its types.
