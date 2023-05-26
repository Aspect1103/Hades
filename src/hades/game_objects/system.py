"""Manages the entity component system and its processes."""
from __future__ import annotations

# Builtin
from typing import TYPE_CHECKING, cast

# Custom
from hades.game_objects.attacks import AttackBase, AttackManager
from hades.game_objects.base import (
    ATTACK_ALGORITHMS,
    GAME_OBJECT_ATTRIBUTES,
    MOVEMENT_ALGORITHMS,
    ComponentType,
)
from hades.game_objects.movements import MovementBase, MovementManager

if TYPE_CHECKING:
    from collections.abc import Generator

    from hades.game_objects.base import ComponentData, GameObjectComponent

__all__ = ("ECS", "NotRegisteredError")


class NotRegisteredError(Exception):
    """Raised when a game object or component type is not registered."""

    def __init__(
        self: NotRegisteredError,
        *,
        not_registered_type: str,
        value: int | str | ComponentType,
    ) -> None:
        """Initialise the object.

        Args:
            not_registered_type: The game object or component type that is not
                registered.
            value: The value that is not registered.
        """
        super().__init__(
            f"The {not_registered_type} `{value}` is not registered with the ECS.",
        )


class ECS:
    """Stores and manages game objects registered with the entity component system."""

    __slots__ = (
        "_next_game_object_id",
        "_components",
    )

    def __init__(self: ECS) -> None:
        """Initialise the object."""
        self._next_game_object_id = 0
        self._components: dict[int, dict[ComponentType, GameObjectComponent]] = {}

    def add_game_object(
        self: ECS,
        component_data: ComponentData,
        *components: type[GameObjectComponent],
    ) -> int:
        """Add a game object to the system with optional components.

        Args:
            component_data: The data for the components.
            *components: The optional list of components for the game object.

        Returns:
            The game object ID.

        Raises:
            NotRegisteredError: The component type `type` is not registered with the
                ECS.
        """
        # Create the game object and get the constructor for this game object type
        self._components[self._next_game_object_id] = {}

        # Add the optional components to the system
        attack_components, movement_components = [], []
        for component in components:
            game_object_component = component(
                self._next_game_object_id,
                self,
                component_data,
            )
            self._components[self._next_game_object_id][
                component.component_type
            ] = game_object_component

            # Determine if this component requires a manager or not
            if component.component_type in ATTACK_ALGORITHMS:
                attack_components.append(game_object_component)
            elif component.component_type in MOVEMENT_ALGORITHMS:
                movement_components.append(game_object_component)

        # Instantiate the required managers
        if attack_components:
            self._components[self._next_game_object_id][
                ComponentType.ATTACK_MANAGER
            ] = AttackManager(
                self._next_game_object_id,
                self,
                component_data,
                cast(list[AttackBase], attack_components),
            )
        if movement_components:
            self._components[self._next_game_object_id][
                ComponentType.MOVEMENT_MANAGER
            ] = MovementManager(
                self._next_game_object_id,
                self,
                component_data,
                cast(list[MovementBase], movement_components),
            )

        # Increment _next_game_object_id and return the current game object ID
        self._next_game_object_id += 1
        return self._next_game_object_id - 1

    def remove_game_object(self: ECS, game_object_id: int) -> None:
        """Remove a game object from the system.

        Args:
            game_object_id: The game object ID.

        Raises:
            NotRegisteredError: The game object ID `ID` is not registered with the ECS.
        """
        # Check if the game object is registered or not
        if game_object_id not in self._components:
            raise NotRegisteredError(
                not_registered_type="game object ID",
                value=game_object_id,
            )

        # Delete the game object from the system
        del self._components[game_object_id]

    def get_component_for_game_object(
        self: ECS,
        game_object_id: int,
        component_type: ComponentType,
    ) -> GameObjectComponent:
        """Get a component from a game object.

        Args:
            game_object_id: The game object ID.
            component_type: The component type to get.

        Returns:
            The game object's component.

        Raises:
            NotRegisteredError: The game object ID `ID` is not registered with the ECS.
            KeyError: The component type is not part of the game object.
        """
        # Check if the game object ID is registered or not
        if game_object_id not in self._components:
            raise NotRegisteredError(
                not_registered_type="game object ID",
                value=game_object_id,
            )

        # Return the game object's components
        return self._components[game_object_id][component_type]

    def get_game_object_attributes_for_game_object(
        self: ECS,
        game_object_id: int,
    ) -> Generator[GameObjectComponent, None, None]:
        """Get all the game object attributes registered to the game object.

        Args:
            game_object_id: The game object ID.

        Returns:
            The game object attributes registered to the game object.

        Raises:
            NotRegisteredError: The game object ID `ID` is not registered with the ECS.
        """
        # Check if the game object ID is registered or not
        if game_object_id not in self._components:
            raise NotRegisteredError(
                not_registered_type="game object ID",
                value=game_object_id,
            )

        # Get the game object attributes if they exist
        return (
            game_object_attribute
            for component_type in GAME_OBJECT_ATTRIBUTES
            if (
                game_object_attribute := self._components[game_object_id].get(
                    component_type,
                )
            )
            is not None
        )

    def __repr__(self: ECS) -> str:
        """Return a human-readable representation of this object.

        Returns:
            The human-readable representation of this object.
        """
        return f"<EntityComponentSystem (Game object count={len(self._components)})>"
