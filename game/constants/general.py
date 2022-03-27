from __future__ import annotations

# Pip
import arcade

# Custom
from constants.generation import TileType

# Debug constants
DEBUG_LINES = False
DEBUG_GAME = True
DEBUG_VIEW_DISTANCE = arcade.color.RED
DEBUG_ATTACK_DISTANCE = arcade.color.BLUE

# Sprite sizes
SPRITE_SCALE = 2.5
SPRITE_SIZE = 16 * SPRITE_SCALE

# Physics constants
DAMPING = 0

# Inventory constants
INVENTORY_WIDTH = 5
INVENTORY_HEIGHT = 3

# Item constants
CONSUMABLES = [TileType.HEALTH_POTION]
HEALTH_POTION_INCREASE = 10
