# Custom
from hades_extensions.game_objects import ComponentBase, SystemBase, Vec2d

class AttackSystem(SystemBase):
    def do_attack(
        self: AttackSystem,
        game_object_id: int,
        targets: list[int],
    ) -> tuple[Vec2d, float, float] | None: ...
    def previous_attack(self: AttackSystem, game_object_id: int) -> None: ...
    def next_attack(self: AttackSystem, game_object_id: int) -> None: ...

class DamageSystem(SystemBase):
    def deal_damage(self: DamageSystem, game_object_id: int, damage: int) -> None: ...

class EffectSystem(SystemBase):
    def apply_effects(
        self: EffectSystem,
        game_object_id: int,
        target_game_object_id: int,
    ) -> None: ...

class InventorySystem(SystemBase):
    def add_item_to_inventory(
        self: InventorySystem,
        game_object_id: int,
        item: int,
    ) -> None: ...
    def remove_item_from_inventory(
        self: InventorySystem,
        game_object_id: int,
        index: int,
    ) -> int: ...

class UpgradeSystem(SystemBase):
    def upgrade_component(
        self: UpgradeSystem,
        game_object_id: int,
        target_component: type[ComponentBase],
    ) -> None: ...
