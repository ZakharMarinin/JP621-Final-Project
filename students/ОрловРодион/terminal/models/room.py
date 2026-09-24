from models.item import Item
from models.character import Enemy, NPC


class Room:
    # описание выходы предметы враги нпсишки

    def __init__(self, room_id: str, description: str, exits: dict[str, str] | None = None):
        self.room_id = room_id
        self.description = description
        self.exits: dict[str, str] = exits or {}
        self.items: list[Item] = []
        self.enemies: list[Enemy] = []
        self.npcs: list[NPC] = []
        self.locked_exits: dict[str, str] = {}

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def remove_item(self, item_id: str) -> Item | None:
        for i, it in enumerate(self.items):
            if it.item_id == item_id:
                return self.items.pop(i)
        return None

    def add_enemy(self, enemy: Enemy) -> None:
        self.enemies.append(enemy)

    def remove_enemy(self, enemy_name: str) -> Enemy | None:
        for i, e in enumerate(self.enemies):
            if e.name == enemy_name:
                return self.enemies.pop(i)
        return None

    def add_npc(self, npc: NPC) -> None:
        self.npcs.append(npc)

    def get_npc(self, name: str) -> NPC | None:
        for n in self.npcs:
            if n.name.lower() == name.lower():
                return n
        return None

    def get_enemy(self, name: str) -> Enemy | None:
        for e in self.enemies:
            if e.name.lower() == name.lower():
                return e
        return None

    def __repr__(self) -> str:
        return f"Room({self.room_id}, exits={list(self.exits.keys())})"