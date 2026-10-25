#include <nanobind/nanobind.h>
#include <space/Point.hpp>

// Compile against a real upstream header without exposing a feature API.
static_assert(sizeof(agh::Point) > 0);

NB_MODULE(_core, module) {
    module.doc() = "Native build infrastructure for Agent-Harmony Python bindings.";
    module.attr("__version__") = AGENT_HARMONY_VERSION;
}
