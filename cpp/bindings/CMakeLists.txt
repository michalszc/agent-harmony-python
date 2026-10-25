nanobind_add_module(_core NB_STATIC module.cpp)
target_link_libraries(_core PRIVATE agent_harmony_headers)
target_compile_definitions(_core PRIVATE
  AGENT_HARMONY_VERSION="${PROJECT_VERSION}")
set_target_properties(_core PROPERTIES CXX_EXTENSIONS OFF)
install(TARGETS _core
  LIBRARY DESTINATION agent_harmony
  RUNTIME DESTINATION agent_harmony)
