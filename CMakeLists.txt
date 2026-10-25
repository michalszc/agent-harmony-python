cmake_minimum_required(VERSION 3.29...4.4)
project(agent_harmony VERSION "${SKBUILD_PROJECT_VERSION}" LANGUAGES CXX)

find_package(Python 3.12 REQUIRED COMPONENTS Interpreter Development.Module)
find_package(nanobind CONFIG REQUIRED)

set(AGENT_HARMONY_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/external/agent-harmony")
if(NOT EXISTS "${AGENT_HARMONY_SOURCE_DIR}/include/space/Point.hpp")
  message(FATAL_ERROR
    "Agent-Harmony sources are missing. Run: git submodule update --init external/agent-harmony")
endif()

# Upstream's CMake target builds experimental SFML visualization code. The core
# APIs are headers; keep the initial extension independent of that GUI dependency.
add_library(agent_harmony_headers INTERFACE)
target_include_directories(agent_harmony_headers INTERFACE
  "${AGENT_HARMONY_SOURCE_DIR}/include")
target_compile_features(agent_harmony_headers INTERFACE cxx_std_20)

add_subdirectory(cpp/bindings)
