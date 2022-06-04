from __future__ import annotations

# Builtin
import logging
import time
from collections import deque
from typing import TYPE_CHECKING

# Pip
import numpy as np

if TYPE_CHECKING:
    from game.entities.base import Tile

# Get the logger
logger = logging.getLogger(__name__)


class Queue:
    """Provides an abstraction over the deque object making access much easier."""

    __slots__ = ("_queue",)

    def __init__(self) -> None:
        self._queue: deque[Tile] = deque["Tile"]()

    def __repr__(self) -> str:
        return f"<Queue (Size={self.size})>"

    @property
    def size(self) -> int:
        """
        Gets the size of the queue.

        Returns
        -------
        int
            The size of the queue
        """
        return len(self._queue)

    @property
    def empty(self) -> bool:
        """
        Checks if the queue is empty or not.

        Returns
        -------
        bool
            Whether the queue is empty or not.
        """
        return not bool(self._queue)

    def put(self, tile: Tile) -> None:
        """
        Adds a tile to the queue.

        Parameters
        ----------
        tile: Tile
            The tile to add to the queue
        """
        self._queue.append(tile)

    def get(self) -> Tile:
        """
        Removes a tile from the queue.

        Returns
        -------
        Tile
            The tile that was removed from the queue.
        """
        return self._queue.popleft()


class VectorField:
    """
    Represents a vector flow field that allows for efficient pathfinding to a specific
    position for large amount of entities. The steps needed to accomplish this:
        1. First, we start at the destination tile and work our way outwards using a
        breadth first search. This is called a 'flood fill' and will construct the
        Dijkstra map needed for the flow field.

        2. Next, we iterate over each tile and find the neighbour with the lowest
        Dijkstra distance. Using this we can create a vector from the source tile to the
        neighbour tile making for more natural pathfinding since the enemy can go in 6
        directions instead of 4.

        # 3. Finally, we can optionally add a value to each tile which is the distance
        # from the current tile to the destination tile and is just the sum of the
        # number of vectors to get to the destination tile. This is called a Dijkstra
        # map and allows us to calculate the cost for a particular path.

    Further reading which may be useful:
        `Other uses of Dijkstra maps
        <http://www.roguebasin.com/index.php/The_Incredible_Power_of_Dijkstra_Maps>`_
        `Dijkstra maps visualized
        <http://www.roguebasin.com/index.php/Dijkstra_Maps_Visualized>`_
        `Understanding goal based pathfinding
        <https://gamedevelopment.tutsplus.com/tutorials/understanding-goal-based-vector\
        -field-pathfinding--gamedev-9007>`_

    Parameters
    ----------
    vector_grid: np.ndarray
        The generated game map which has the vector tiles already initialised.

    Attributes
    ----------
    vector_dict: dict[Tile, tuple[float, float]]
        A dictionary which will hold the vector direction an enemy needs to travel in
        from the current tile to get to the destination tile.
    """

    __slots__ = (
        "vector_grid",
        "vector_dict",
    )

    _no_diagonal_offsets: list[tuple[int, int]] = [
        (0, -1),
        (-1, 0),
        (1, 0),
        (0, 1),
    ]

    _diagonal_offsets: list[tuple[int, int]] = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
    ]

    def __init__(
        self,
        vector_grid: np.ndarray,
    ) -> None:
        self.vector_grid: np.ndarray = vector_grid
        self.vector_dict: dict[Tile, tuple[float, float]] = {}

    def __repr__(self) -> str:
        return (
            f"<VectorField (Width={self.vector_grid.shape[1]})"
            f" (Height={self.vector_grid.shape[0]})"
        )

    @property
    def width(self) -> int:
        """
        Gets the width of the vector grid.

        Returns
        -------
        int
            The width of the vector grid.
        """
        return self.vector_grid.shape[1]

    @property
    def height(self) -> int:
        """
        Gets the height of the vector grid.

        Returns
        -------
        int
            The height of the vector grid.
        """
        return self.vector_grid.shape[0]

    def _get_direct_neighbours(self, tile: Tile) -> list[Tile]:
        """
        Gets a tile's direct neighbours (top, bottom, left and right) based on their
        position in the grid.

        Parameters
        ----------
        tile: Tile
            The tile to get direct neighbours for.

        Returns
        -------
        list[Tile]
            A list of the tile's direct neighbours.
        """
        return self._get_neighbours(tile, self._no_diagonal_offsets)

    def _get_full_neighbours(self, tile: Tile) -> list[Tile]:
        """
        Gets a tile's full neighbours (top-left, top-middle, top-right, middle-left,
        middle-right, bottom-left, bottom-middle and bottom-right) based on their
        position in the grid.

        Parameters
        ----------
        tile: Tile
            The tile to get full neighbours for.

        Returns
        -------
        list[Tile]
            A list of the tile's full neighbours.
        """
        return self._get_neighbours(tile, self._diagonal_offsets)

    def _get_neighbours(self, tile: Tile, offsets: list[tuple[int, int]]) -> list[Tile]:
        """
        Gets a tile's neighbours based on a given list of offsets.

        Parameters
        ----------
        tile: Tile
            The tile to get neighbours for.
        offsets: list[tuple[int, int]]
            A list of offsets used for getting the tile's neighbours.

        Returns
        -------
        list[Tile]
            A list of the tile's neighbours.
        """
        # Get all the neighbour floor tiles relative to the current tile
        tile_neighbours: list[Tile] = []
        for dx, dy in offsets:
            # Check if the neighbour position is within the boundaries or not
            x, y = tile.tile_pos[0] + dx, tile.tile_pos[1] + dy
            if (x < 0 or x >= self.width) and (y < 0 or y >= self.height):
                continue

            # Check if the neighbour is a tile or not
            target_tile: Tile = self.get_tile_at_position(x, y)
            if not target_tile:
                continue

            # Check if the neighbour is a wall or not
            if target_tile.blocking:
                continue

            # Neighbour tile is a floor tile so it is valid
            tile_neighbours.append(target_tile)

        # Return all the neighbours
        return tile_neighbours

    def recalculate_map(self, destination_tile: tuple[int, int]) -> None:
        """
        Recalculates the vector field and produces a new path_dict.

        Parameters
        ----------
        destination_tile: tuple[int, int]
            The destination tile which every tile will point towards.
        """
        # Record the start time, so we can know how long the generation takes
        start_time = time.perf_counter()

        # To recalculate the map, we need a few things:
        #   1. A queue object, so we can explore the grid.
        #   2. A vector_dict dict to store the paths for the vector field. We need to
        #   make sure this is empty first.
        #   3. A distances dict to store the distances to each tile from the destination
        #   tile. We also need to make sure this is empty first.
        start = self.get_tile_at_position(destination_tile[0], destination_tile[1])
        queue = Queue()
        queue.put(start)
        self.vector_dict.clear()
        distances: dict[Tile, int] = {start: 0}

        # Explore the grid using a breadth first search to generate the Dijkstra
        # distances
        while not queue.empty:
            # Get the current tile to explore
            current = queue.get()

            # Sometimes current can be None, so check if it is None
            if not current:
                continue

            # Get the current tile's neighbours
            for neighbour in self._get_direct_neighbours(current):
                # Test if the neighbour has already been reached or not. If it hasn't,
                # add it to the queue and set its distance
                if neighbour not in distances:
                    queue.put(neighbour)
                    distances[neighbour] = 1 + distances[current]

        # Use the newly generated Dijkstra map to calculate the vectors at each tile
        for tile in distances:
            # Find the tile's neighbour with the lowest Dijkstra distance
            min_tile = None
            min_dist = np.inf
            for neighbour in self._get_full_neighbours(tile):
                distance = distances[neighbour]
                if distances[neighbour] < min_dist:
                    min_tile = neighbour
                    min_dist = distance

            # If we've found a valid neighbour, point the tile's vector in the direction
            # of the tile with the lowest Dijkstra distance
            if min_tile:
                self.vector_dict[tile] = -(tile.center_x - min_tile.center_x), -(
                    tile.center_y - min_tile.center_y
                )

        # Output the time taken to generate the vector field and update the enemies
        time_taken = (
            f"Vector field generated in {time.perf_counter() - start_time} seconds"
        )
        logger.debug(time_taken)
        print(time_taken)

    def get_tile_at_position(self, x: int, y: int) -> Tile:
        """
        Gets a tile at a specific position in the vector grid.

        Parameters
        ----------
        x: int
            The x position of the tile.
        y: int
            The y position of the tile.

        Returns
        -------
        Tile
            The tile at the given position
        """
        return self.vector_grid[y][x]

    def get_vector_direction(self, current_tile: Tile) -> tuple[float, float]:
        """
        Gets the vector direction an enemy needs to travel in for a given tile.

        Parameters
        ----------
        current_tile: Tile
            The current tile the enemy is on.

        Returns
        -------
        tuple[float, float]
            The direction the enemy needs to travel in.
        """
        return self.vector_dict[current_tile]
