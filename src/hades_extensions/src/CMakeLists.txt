# Create the C++ library which will be used for the tests and the Python module and link
# it against Chipmunk
add_library(${CPP_LIB} STATIC
        ${CMAKE_SOURCE_DIR}/src/game_objects/registry.cpp
        ${CMAKE_SOURCE_DIR}/src/game_objects/steering.cpp
        ${CMAKE_SOURCE_DIR}/src/game_objects/systems/armour_regen.cpp
        ${CMAKE_SOURCE_DIR}/src/game_objects/systems/attacks.cpp
        ${CMAKE_SOURCE_DIR}/src/game_objects/systems/effects.cpp
        ${CMAKE_SOURCE_DIR}/src/game_objects/systems/inventory.cpp
        ${CMAKE_SOURCE_DIR}/src/game_objects/systems/movements.cpp
        ${CMAKE_SOURCE_DIR}/src/game_objects/systems/upgrade.cpp
        ${CMAKE_SOURCE_DIR}/src/generation/bsp.cpp
        ${CMAKE_SOURCE_DIR}/src/generation/map.cpp
        ${CMAKE_SOURCE_DIR}/src/generation/searching.cpp
)
target_include_directories(${CPP_LIB} PUBLIC ${CMAKE_SOURCE_DIR}/include)
target_include_directories(${CPP_LIB} PUBLIC ${chipmunk_SOURCE_DIR}/include)
target_link_libraries(${CPP_LIB} PUBLIC chipmunk2d::chipmunk2d)

# Create the Python module
if (DO_PYTHON)
    message(STATUS "Python bindings enabled (DO_PYTHON is set)")
    pybind11_add_module(${PY_MODULE} ${CMAKE_SOURCE_DIR}/src/binding.cpp)
    target_link_libraries(${PY_MODULE} PRIVATE ${CPP_LIB})
else ()
    message(STATUS "Python bindings disabled (DO_PYTHON is not set)")
endif ()
