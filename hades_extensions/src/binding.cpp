// Std includes
#include <optional>

// External includes
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// Custom includes
#include "include/map.hpp"

// ----- PYTHON MODULE CREATION ------------------------------
PYBIND11_MODULE(hades_extensions, m
) {
// Add the module docstring
m.
doc() = "Generates the dungeon and places game objects in it.";

// Add the create_map function to the module
m.def("create_map",
&create_map,
pybind11::arg("level"),
pybind11::arg("seed") =
pybind11::none(),
("Generate the game map for a given game level.\n\n"
"Parameters\n"
"----------\n"
"level: int\n"
"    The game level to generate a map for.\n"
"seed: int\n"
"    The seed to initialise the random generator.\n\n"
"Returns\n"
"-------\n"
"A tuple containing the generated map and the level constants.\n\n"));

// Add the TileType enum to the module
pybind11::enum_<TileType>(m,
"TileType")
.value("DebugWall", TileType::DebugWall)
.value("Empty", TileType::Empty)
.value("Floor", TileType::Floor)
.value("Wall", TileType::Wall)
.value("Obstacle", TileType::Obstacle)
.value("Player", TileType::Player)
.value("Potion", TileType::Potion);
}


// TODO: pybind11.def_submodule (https://github.com/pybind/pybind11/discussions/4027) for submodules (alternative is
//  https://hopstorawpointers.blogspot.com/2018/06/pybind11-and-python-sub-modules.html?m=1 )