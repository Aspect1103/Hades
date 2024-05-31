"""Manages various building/compiling operations on the game."""

from __future__ import annotations

# Builtin
import argparse
import platform
import subprocess
import zipfile
from pathlib import Path
from typing import Final

# Pip
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

# Initialise some constants for the executable command
RESOURCES_DIR: Final = "src/hades/resources"
ZIP_OUTPUT_NAME: Final = "hades.zip"


class BuildNamespace(argparse.Namespace):
    """Allows typing of an argparse Namespace for the CLI."""

    executable: bool
    cpp: bool


class CMakeBuild(build_ext):  # type: ignore[misc]
    """A custom build_ext command which allows CMake projects to be built."""

    def build_extension(self: CMakeBuild, ext: Extension) -> None:
        """Build a CMake extension.

        Args:
            ext: The extension to build.
        """
        # Determine where the extension should be transferred to after it has been
        # compiled
        current_dir = Path(__file__).parent
        build_dir = current_dir.joinpath(self.get_ext_fullpath(ext.name)).parent
        build_dir.mkdir(parents=True, exist_ok=True)

        # Compile and build the CMake extension
        print(str(current_dir.joinpath(ext.sources[0])))
        subprocess.run(
            [
                "cmake",
                str(current_dir.joinpath(ext.sources[0])),
                f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE={build_dir}",
                "-DDO_TESTS=OFF",
                "--fresh",
                "--preset",
                "Release",
            ],
            check=True,
        )
        subprocess.run(
            [
                "cmake",
                "--build",
                str(current_dir.joinpath(ext.sources[0])) + "/build-release",
            ],
            check=True,
        )


def executable() -> None:
    """Compiles the game into an executable format for portable use."""
    # Initialise some paths
    current_dir = Path(__file__).parent
    source_dir = current_dir.joinpath("src").joinpath("hades").joinpath("window.py")
    output_dir = current_dir.joinpath("build")
    dist_dir = output_dir.joinpath("window.dist")

    # Display some info about the system and the environment
    print(
        f"System information: {platform.system()} {platform.version()}. Python version:"
        f" {platform.python_implementation()} {platform.python_version()}",
    )

    # Execute the build command
    subprocess.run(
        " ".join(
            [
                "./.venv/Scripts/python.exe -m",
                f'nuitka "{source_dir}"',
                "--standalone",
                "--assume-yes-for-downloads",
                f"--include-data-dir={RESOURCES_DIR}={RESOURCES_DIR}",
                f'--output-dir="{output_dir}"',
                "--remove-output",
            ],
        ),
        check=True,
    )

    # Zip the game and display the result
    with zipfile.ZipFile(ZIP_OUTPUT_NAME, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for build_file in dist_dir.rglob("*"):
            zip_file.write(build_file, str(build_file).replace(str(dist_dir), ""))


def cpp() -> None:
    """Compiles the C++ extensions and installs them into the virtual environment."""
    result_path = Path(__file__).parent.joinpath(
        setup(
            name="hades_extensions",
            ext_modules=[Extension("hades_extensions", ["src/hades_extensions"])],
            script_args=["bdist_wheel"],
            cmdclass={"build_ext": CMakeBuild},
        ).dist_files[0][2],
    )
    subprocess.run(["pip", "install", "--force-reinstall", result_path], check=True)


if __name__ == "__main__":
    # Build the argument parser and start parsing arguments
    parser = argparse.ArgumentParser(
        description="Simplifies building/compiling related to Hades",
    )
    build_group = parser.add_mutually_exclusive_group()
    build_group.add_argument(
        "-e",
        "--executable",
        action="store_true",
        help="Compiles the game into an executable format",
    )
    build_group.add_argument(
        "-c",
        "--cpp",
        action="store_true",
        help="Compiles the C++ extensions and installs them",
    )
    args = parser.parse_args(namespace=BuildNamespace())

    # Determine which argument was selected
    if args.executable:
        executable()
    elif args.cpp:
        cpp()
