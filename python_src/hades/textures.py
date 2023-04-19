"""Handles loading and storage of textures needed by the game."""
from __future__ import annotations

# Builtin
from enum import Enum
from pathlib import Path

# Pip
import arcade

# Custom
from hades.constants import SPRITE_SIZE
from hades.exceptions import BiggerThanError

__all__ = (
    "TextureType",
    "grid_pos_to_pixel",
    "load_moving_texture",
    "load_non_moving_texture",
)


# Create the texture path
texture_path = Path(__file__).resolve().parent / "resources" / "textures"


def load_moving_texture(texture: str) -> tuple[arcade.Texture, arcade.Texture]:
    """Load a moving texture into Arcade.

    Parameters
    ----------
    texture: str
        The moving texture to load

    Returns
    -------
    tuple[arcade.Texture, arcade.Texture]
        The loaded moving texture.
    """
    return tuple(arcade.load_texture_pair(texture_path.joinpath(texture)))


def load_non_moving_texture(texture: str) -> arcade.Texture:
    """Load a non-moving texture into Arcade.

    Parameters
    ----------
    texture: str
        The non-moving texture to load


    Returns
    -------
    arcade.Texture
        The loaded non-moving texture.
    """
    return arcade.load_texture(texture_path.joinpath(texture))


class TextureType(Enum):
    """Stores the different types of textures that exist."""

    ARMOUR_BOOST_POTION = load_non_moving_texture("armour_boost_potion.png")
    ARMOUR_POTION = load_non_moving_texture("armour_potion.png")
    ENEMY_IDLE = load_moving_texture("enemy_idle.png")
    FIRE_RATE_BOOST_POTION = load_non_moving_texture("fire_rate_boost_potion.png")
    FLOOR = load_non_moving_texture("floor.png")
    HEALTH_BOOST_POTION = load_non_moving_texture("health_boost_potion.png")
    HEALTH_POTION = load_non_moving_texture("health_potion.png")
    PLAYER_IDLE = load_moving_texture("player_idle.png")
    SHOP = load_non_moving_texture("shop.png")
    SPEED_BOOST_POTION = load_non_moving_texture("speed_boost_potion.png")
    WALL = load_non_moving_texture("wall.png")


def grid_pos_to_pixel(x: int, y: int) -> tuple[float, float]:
    """Calculate the x and y position based on the game map or vector field position.

    Parameters
    ----------
    x: int
        The x position in the game map or vector field.
    y: int
        The x position in the game map or vector field.

    Raises
    ------
    BiggerThanError
        The input must be bigger than or equal to 0.

    Returns
    -------
    tuple[float, float]
        The x and y position of a sprite on the screen.
    """
    # Check if the inputs are negative
    if x < 0 or y < 0:
        raise BiggerThanError(0)

    # Calculate the position on screen
    return (
        x * SPRITE_SIZE + SPRITE_SIZE / 2,
        y * SPRITE_SIZE + SPRITE_SIZE / 2,
    )
