"""Manages the Conan configuration for the application."""

# Pip
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain


class HadesExtensions(ConanFile):  # type: ignore[misc]
    """The Conan configuration for the application."""

    settings = "build_type"
    generators = "CMakeDeps"

    def requirements(self: ConanFile) -> None:
        """Add the required dependencies to the Conan configuration."""
        self.requires("pybind11/2.11.1")
        self.requires("gtest/1.14.0")
        self.requires("chipmunk2d/7.0.3")

    def generate(self: ConanFile) -> None:
        """Generate the CMake toolchain file for the application."""
        tc = CMakeToolchain(self)
        tc.user_presets_path = None
        tc.generate()
