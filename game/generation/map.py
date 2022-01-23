from __future__ import annotations

# Builtin
from typing import Optional, Tuple

# Pip
import numpy as np
from constants import MAP_HEIGHT, MAP_WIDTH, SPLIT_COUNT

# Custom
from .bsp import Leaf


class Map:
    """
    Procedurally generates a game generation based on a given game level.

    Parameters
    ----------
    level: int
        The game level to generate a map for.

    Attributes
    ----------
    width: int
        The width of the game generation.
    height: int
        The height of the game generation.
    split_count: int = 5
        The amount of times the bsp should split.
    grid: Optional[np.ndarray]
        The 2D grid which represents the dungeon.
    bsp: Optional[Leaf]
        The root leaf for the binary space partition.
    player_spawn: Optional[Tuple[int, int]]
        The coordinates for the player spawn. This is in the format (x, y).
    """

    def __init__(self, level: int) -> None:
        self.level: int = level
        self.width: int = -1
        self.height: int = -1
        self.split_count: int = -1
        self.grid: Optional[np.ndarray] = None
        self.bsp: Optional[Leaf] = None
        self.player_spawn: Optional[Tuple[int, int]] = None
        self.make_map()

    def __repr__(self) -> str:
        return f"<Map (Width={self.width}) (Height={self.height})>"

    def make_map(self) -> None:
        """Function which manages the map generation for a specified level."""

        # Create constants used during the generation
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        self.split_count = SPLIT_COUNT

        np.set_printoptions(
            edgeitems=100,
            linewidth=10000000000000000,
            formatter=dict(float=lambda x: "%.3g" % x),
        )

        # Create the 2D grid used for representing the dungeon
        self.grid = np.full((self.height, self.width), 0, np.int8)

        # Create the first leaf used for generation
        self.bsp = Leaf(0, 0, self.width - 1, self.height - 1, self.grid)

        # Start the recursive splitting
        for count in range(self.split_count):
            self.bsp.split()

        # Create the rooms recursively
        self.bsp.create_room()

        # Create the hallways recursively
        self.bsp.create_hallway()

        # Get the coordinates for the player spawn
        self.player_spawn = self.bsp.create_player_spawn()
