from __future__ import annotations

# Map tile generation
MAP_WIDTH = 40
MAP_HEIGHT = 20
SPLIT_COUNT = 3
ENEMY_COUNT = 5
HALLWAY_WIDTH = 5
EMPTY = 0
FLOOR = 1
WALL = 2
PLAYER = 3
ENEMY = 4
DEBUG_WALL = 9
DEBUG_LINES = False
DEBUG_GAME = True

# Map container/room generation
MIN_CONTAINER_SIZE = 7
MIN_ROOM_SIZE = 5

# Sprite sizes
SPRITE_SCALE = 2.5
SPRITE_WIDTH = 16 * SPRITE_SCALE
SPRITE_HEIGHT = 16 * SPRITE_SCALE

# Physics constants
DAMPING = 0

# Player constants
PLAYER_MOVEMENT_FORCE = 10000
ATTACK_COOLDOWN = 1
PLAYER_HEALTH = 100

# Enemy constants
ENEMY_VIEW_DISTANCE = 5
ENEMY_MOVEMENT_FORCE = 20
ENEMY_HEALTH = 10

# Attack constants
BULLET_VELOCITY = 300
BULLET_OFFSET = 30
