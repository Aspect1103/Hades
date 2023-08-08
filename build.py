"""Manages various building/compiling operations on the game."""
from __future__ import annotations

# Builtin
import argparse
import platform
import subprocess
import zipfile
from pathlib import Path
from typing import TypeVar

# Pip
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

# Define a generic type for the keyword arguments
KW = TypeVar("KW")


class BuildNamespace(argparse.Namespace):
    """Allows typing of an argparse Namespace for the CLI."""

    executable: bool
    cpp: bool


class CMakeBuild(build_ext):
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

        # Determine the profile to build the CMake extension with
        profile = "Release"

        # Make sure the build directory exists
        build_temp = Path(self.build_temp).joinpath(ext.name)
        build_temp.mkdir(parents=True, exist_ok=True)

        # Compile and build the CMake extension
        print("before init")
        subprocess.run(
            " ".join(
                [
                    "cmake",
                    str(current_dir.joinpath(ext.sources[0])),
                    "-DDO_TESTS=false",
                    "-DDO_PYTHON=true",
                    f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{profile.upper()}={build_dir}",
                ],
            ),
            cwd=build_temp,
            check=True,
        )
        print("before build")
        subprocess.run(
            " ".join(["cmake", "--build", ".", f"--config {profile}"]),
            cwd=build_temp,
            check=True,
        )
        print("end")


def executable() -> None:
    """Compiles the game into an executable format for portable use."""
    # Initialise some constants
    game_dir = "src/hades"
    source_dir = Path().absolute() / game_dir / "window.py"
    resources_dir = f"{game_dir}/resources"
    output_dir = Path().absolute() / "build"
    dist_dir = output_dir.joinpath("window.dist")
    zip_output_name = f"{game_dir}.zip"

    # Display some info about the system and the environment
    print(
        f"System information: {platform.system()} {platform.version()}. Python"
        f" version: {platform.python_implementation()} {platform.python_version()}",
    )
    print(f"Current directory: {Path().absolute()}")

    # Create the command to build the game
    commands = [
        ".\\.venv\\Scripts\\python.exe -m",
        f'nuitka "{source_dir}"',
        "--standalone",
        "--assume-yes-for-downloads",
        f"--include-data-dir={resources_dir}={resources_dir}",
        f'--output-dir="{output_dir}"',
        "--plugin-enable=numpy",
    ]
    command_string = " ".join(commands)
    print(f"Executing command string: {command_string}")

    # Execute the build command
    subprocess.run(command_string, check=True)

    # Zip the game and verify that the file exists
    with zipfile.ZipFile(zip_output_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for build_file in dist_dir.rglob("*"):
            zip_file.write(build_file, str(build_file).replace(str(dist_dir), ""))
    print(f"Finishing zipping {zip_output_name}. Now verifying archive")
    try:
        print(f"Output of {zip_output_name} was successful")
    except AssertionError:
        print(f"Output of {zip_output_name} was unsuccessful")


def cpp() -> None:
    """Compiles the C++ extensions and installs them into the virtual environment."""
    dist = setup(
        name="hades_extensions",
        ext_modules=[Extension("hades_extensions", ["hades_extensions"])],
        script_args=["bdist_wheel"],
        cmdclass={"build_ext": CMakeBuild},
    )
    subprocess.run(
        f'pip install --force-reinstall "{Path.cwd().joinpath(dist.dist_files[0][2])}"',
        check=True,
    )


def build(**_: KW) -> None:
    """Allow Poetry to automatically build the C++ extension upon installation."""
    cpp()


if __name__ == "__main__":
    cpp()
