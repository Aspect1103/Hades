# Define some CMake options
cmake_minimum_required(VERSION 3.22.1)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_PROJECT_TOP_LEVEL_INCLUDES ${CMAKE_CURRENT_SOURCE_DIR}/cmake/conan_provider.cmake)

# Define custom options
set(ENABLE_COVERAGE ON CACHE BOOL "Enable coverage reporting for GCC/Clang")
set(DO_PYTHON ON CACHE BOOL "Enable Python bindings")
set(DO_TESTS ON CACHE BOOL "Enable testing")

# Define the module names and initialise the project
set(PY_MODULE hades_extensions)
set(CPP_LIB hades_extensions_lib)
set(TEST_MODULE hades_extensions_tests)
project(${PY_MODULE} LANGUAGES CXX)

# Include the required modules
include(CTest)

# Find the required packages
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)
find_package(GTest CONFIG REQUIRED)
find_package(chipmunk2d CONFIG REQUIRED)

# Set the warning level for the project
if (MSVC)
    add_compile_options(/W4 /WX)
else ()
    add_compile_options(-Wall -Wextra -Werror -pedantic)
endif ()

# Enable coverage if supported by the compiler and enabled by the user
if (ENABLE_COVERAGE)
    if (NOT MSVC)
        message(STATUS "Coverage enabled (compiler is GCC/Clang)")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -O0 --coverage")
        set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --coverage")
    else ()
        message(STATUS "Coverage disabled (compiler is not GCC/Clang)")
    endif ()
else ()
    message(STATUS "Coverage disabled (ENABLE_COVERAGE is not set)")
endif ()

# Add the subdirectories for the different parts of the project
add_subdirectory(src)
if (DO_TESTS)
    message(STATUS "Tests enabled (DO_TESTS is set)")
    add_subdirectory(tests)
else ()
    message(STATUS "Tests disabled (DO_TESTS is not set)")
endif ()
