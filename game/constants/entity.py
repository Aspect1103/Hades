from __future__ import annotations

# Builtin
from typing import TYPE_CHECKING, NamedTuple

# Custom
from constants.enums import AIMovementType, AttackAlgorithmType
from textures import moving_textures

if TYPE_CHECKING:
    import arcade


# Base entity type
class EntityType(NamedTuple):
    """
    Stores general data about an entity type.

    name: str
        The name of the entity.
    health: int
        The entity's health.
    armour: int
        The entity's armour.
    textures: dict[str, list[list[arcade.Texture]]]
        The textures which represent this entity.
    max_velocity: int
        The max speed that the entity can go.
    attack_cooldown: int
        The time duration between attacks.
    damage: int
        The damage the entity deals.
    armour_regen: bool
        Whether the entity regenerates armour or not.
    armour_regen_cooldown: int
        The time between armour regenerations.
    attack_algorithms: list[AttackAlgorithmType]
        The attack algorithms that this player has.
    """

    name: str
    health: int
    armour: int
    textures: dict[str, list[list[arcade.Texture]]]
    max_velocity: int
    attack_cooldown: int
    damage: int
    armour_regen: bool
    armour_regen_cooldown: int
    attack_algorithms: list[AttackAlgorithmType]


# Base player type
class PlayerType(NamedTuple):
    """
    Stores data about a specific player type.

    melee_range: int
        The amount of tiles the player can attack within using a melee attack.
    melee_degree: int
        The degree that the player's melee attack is limited to.
    """

    melee_range: int
    melee_degree: int


# Base enemy type
class EnemyType(NamedTuple):
    """
    Stores data about a specific enemy type.

    view_distance: int
        The amount of tiles the enemy can see too.
    attack_range: int
        The amount of tiles the enemy can attack within.
    movement_algorithm: AIMovementType
        The movement algorithm that this enemy has.
    """

    view_distance: int
    attack_range: int
    movement_algorithm: AIMovementType


# Base entity constructor
class BaseType(NamedTuple):
    """
    The base class for constructing an entity.

    entity_type: EntityType
        The general data about this entity.
    custom_data: PlayerType | EnemyType
        The specific data related to this entity
    """

    entity_type: EntityType
    custom_data: PlayerType | EnemyType


# Player characters
PLAYER = BaseType(
    EntityType(
        "player",
        100,
        20,
        moving_textures["player"],
        200,
        1,
        10,
        True,
        1,
        [
            AttackAlgorithmType.RANGED,
            AttackAlgorithmType.MELEE,
            AttackAlgorithmType.AREA_OF_EFFECT,
        ],
    ),
    PlayerType(3, 60),
)

# Enemy characters
ENEMY1 = BaseType(
    EntityType(
        "enemy1",
        10,
        10,
        moving_textures["enemy"],
        50,
        1,
        5,
        True,
        3,
        [AttackAlgorithmType.RANGED],
    ),
    EnemyType(5, 3, AIMovementType.FOLLOW),
)
ENEMY2 = BaseType(
    EntityType(
        "enemy2",
        10,
        10,
        moving_textures["enemy"],
        50,
        1,
        5,
        True,
        3,
        [AttackAlgorithmType.RANGED],
    ),
    EnemyType(5, 3, AIMovementType.FOLLOW),
)

# Status effect constants
HEALTH_BOOST_POTION_INCREASE = 50
HEALTH_BOOST_POTION_DURATION = 10

# Other entity constants
FACING_RIGHT = 0
FACING_LEFT = 1
MOVEMENT_FORCE = 1000000
ARMOUR_REGEN_WAIT = 5
ARMOUR_REGEN_AMOUNT = 1
BULLET_VELOCITY = 300
BULLET_OFFSET = 30
MELEE_RESOLUTION = 10
