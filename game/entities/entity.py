from __future__ import annotations

import math

# Builtin
from enum import IntEnum
from typing import TYPE_CHECKING

# Pip
import arcade

# Custom
from constants import BULLET_OFFSET, BULLET_VELOCITY, SPRITE_SCALE
from textures import pos_to_pixel

if TYPE_CHECKING:
    from physics import PhysicsEngine


class EntityID(IntEnum):
    """Stores the ID of each enemy to make checking more efficient."""

    ENTITY = 0
    PLAYER = 1
    ENEMY = 2


class Bullet(arcade.SpriteSolidColor):
    """
    Represents a bullet in the game.

    Parameters
    ----------
    x: float
        The starting x position of the bullet.
    y: float
        The starting y position of the bullet.
    width: int
        Width of the bullet.
    height: int
        Height of the bullet.
    color: tuple[int, int, int]
        The color of the bullet.
    owner: Entity
        The entity which shot the bullet.
    """

    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        color: tuple[int, int, int],
        owner: Entity,
    ) -> None:
        super().__init__(width=width, height=height, color=color)
        self.center_x: float = x
        self.center_y: float = y
        self.owner: Entity = owner

    def __repr__(self) -> str:
        return f"<Bullet (Position=({self.center_x}, {self.center_y}))>"


class Entity(arcade.Sprite):
    """
    Represents an entity in the game.

    Parameters
    ----------
    x: int
        The x position of the entity in the game map.
    y: int
        The y position of the entity in the game map.
    texture_dict: dict[str, list[list[arcade.Texture]]]
        The textures which represent this entity.
    health: int
        The health of this entity.

    Attributes
    ----------
    direction: float
        The angle the entity is facing.
    facing: int
        The direction the entity is facing. 0 is right and 1 is left.
    time_since_last_attack: float
        The time since the last attack.
    """

    # Class variables
    ID: EntityID = EntityID.ENTITY

    def __init__(
        self,
        x: int,
        y: int,
        texture_dict: dict[str, list[list[arcade.Texture]]],
        health: int,
    ) -> None:
        super().__init__(scale=SPRITE_SCALE)
        self.center_x, self.center_y = pos_to_pixel(x, y)
        self.texture_dict: dict[str, list[list[arcade.Texture]]] = texture_dict
        self.texture: arcade.Texture = self.texture_dict["idle"][0][0]
        self.health: int = health
        self.direction: float = 0
        self.facing: int = 0
        self.time_since_last_attack: float = 0

    def __repr__(self) -> str:
        return f"<Entity (Position=({self.center_x}, {self.center_y}))>"

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """
        Processes movement and game logic.

        Parameters
        ----------
        delta_time: float
            Time interval since the last time the function was called.
        """
        raise NotImplementedError

    def deal_damage(self, damage: int) -> None:
        """
        Deals damage to an entity.

        Parameters
        ----------
        damage: int
            The amount of health to take away from the entity.
        """
        self.health -= damage

    def ranged_attack(self, bullet_list: arcade.SpriteList) -> None:
        """
        Performs a ranged attack in the direction the character is facing.

        Parameters
        ----------
        bullet_list: arcade.SpriteList
            The sprite list to add the bullet to.
        """

        # Reset the time counter
        self.time_since_last_attack = 0

        # Create and add the new bullet to the physics engine
        new_bullet = Bullet(self.center_x, self.center_y, 25, 5, arcade.color.RED, self)
        new_bullet.angle = self.direction
        physics: PhysicsEngine = self.physics_engines[0]
        physics.add_bullet(new_bullet)
        bullet_list.append(new_bullet)

        # Move the bullet away from the entity a bit to stop its colliding with them
        angle_radians = self.direction * math.pi / 180
        new_x, new_y = (
            new_bullet.center_x + math.cos(angle_radians) * BULLET_OFFSET,
            new_bullet.center_y + math.sin(angle_radians) * BULLET_OFFSET,
        )
        physics.set_position(new_bullet, (new_x, new_y))

        # Calculate its velocity
        change_x, change_y = (
            math.cos(angle_radians) * BULLET_VELOCITY,
            math.sin(angle_radians) * BULLET_VELOCITY,
        )
        physics.set_velocity(new_bullet, (change_x, change_y))
