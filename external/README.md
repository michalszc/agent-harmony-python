# Upstream dependency

`agent-harmony/` is the Git submodule for
[Tosiekdev/Agent-Harmony](https://github.com/Tosiekdev/Agent-Harmony), pinned to
`8bd36a04bb5de5a020ffeb71390ce80a05e6b708` for Python package 0.0.0.

Initialize it with `make submodules`. Do not copy or edit upstream source files
in the parent repository. A deliberate dependency update changes the gitlink,
this record, and `LICENSE-UPSTREAM` if upstream changes its notice.

The initial CMake integration uses only the core headers. Upstream's CMake target
compiles experimental SFML visualization code; its nested SFML submodule is not
needed, initialized, or distributed. Source distributions include upstream
headers, sources, CMake input, and license so wheel builds need no Git checkout
or network fetch of C++ dependencies.
