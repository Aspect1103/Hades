"""Holds fixtures and test data used by all tests."""
from __future__ import annotations

# Pip
import numpy as np
import pytest

# Custom
from hades.constants.generation import TileType
from hades.generation.bsp import Leaf
from hades.generation.map import Map
from hades.generation.primitives import Point, Rect

__all__ = ()


@pytest.fixture
def valid_point_one() -> Point:
    """Initialise the first valid point for use in testing.

    Returns
    -------
    Point
        The first valid point used for testing.
    """
    return Point(3, 5)


@pytest.fixture
def valid_point_two() -> Point:
    """Initialise the second valid point for use in testing.

    Returns
    -------
    Point
        The second valid point used for testing.
    """
    return Point(5, 7)


@pytest.fixture
def boundary_point() -> Point:
    """Initialise a boundary point for use in testing.

    Returns
    -------
    Point
        The boundary point used for testing.
    """
    return Point(0, 0)


@pytest.fixture
def invalid_point() -> Point:
    """Initialise an invalid point for use in testing.

    Returns
    -------
    Point
        The invalid point used for testing.
    """
    return Point("test", "test")  # type: ignore


@pytest.fixture
def grid() -> np.ndarray:
    """Initialise a 2D numpy grid for use in testing.

    Returns
    -------
    np.ndarray
        The 2D numpy grid used for testing.
    """
    return np.full((50, 50), TileType.EMPTY, np.int8)


@pytest.fixture
def rect(valid_point_one: Point, valid_point_two: Point, grid: np.ndarray) -> Rect:
    """Initialise a rect for use in testing.

    Parameters
    ----------
    valid_point_one: Point
        The first valid point used for testing.
    valid_point_two: Point
        The second valid point used for testing.
    grid: np.ndarray
        The 2D grid used for testing.

    Returns
    -------
    Rect
        The rect used for testing.
    """
    return Rect(grid, valid_point_one, valid_point_two)


@pytest.fixture
def leaf(boundary_point: Point, grid: np.ndarray) -> Leaf:
    """Initialise a leaf for use in testing.

    Parameters
    ----------
    boundary_point: Point
        A boundary point used for testing.
    grid: np.ndarray
        The 2D grid used for testing.

    Returns
    -------
        The leaf used for testing.
    """
    return Leaf(boundary_point, Point(grid.shape[1], grid.shape[0]), grid)


@pytest.fixture
def map_obj() -> Map:
    """Initialise a map for use in testing.

    Returns
    -------
    Map
        The map used for testing.
    """
    return Map(0)
