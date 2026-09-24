from abc import ABC, abstractmethod


class Item(ABC):
    # базовый класс предмета

    def __init__(self, item_id: str, name: str, description: str = ""):
        self.item_id = item_id
        self.name = name
        self.description = description

    @abstractmethod
    def use(self, player, context) -> str:
        ...

    def is_consumable(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.item_id})"


class Potion(Item):
    def __init__(self, item_id: str, name: str, heal: int, description: str = ""):
        super().__init__(item_id, name, description)
        self.heal = heal

    def use(self, player, context) -> str:
        before = player.hp
        player.hp = player.hp + self.heal
        return f"{player.name} выпивает {self.name} и восстанавливает {player.hp - before} HP."

    def is_consumable(self) -> bool:
        return True


class Weapon(Item):
    def __init__(self, item_id: str, name: str, bonus_damage: int, description: str = ""):
        super().__init__(item_id, name, description)
        self.bonus_damage = bonus_damage

    def use(self, player, context) -> str:
        player.damage += self.bonus_damage
        return f"{player.name} экипирует {self.name} (+{self.bonus_damage} к урону)."

    def is_consumable(self) -> bool:
        return True


class Key(Item):
    def __init__(self, item_id: str, name: str, opens: str, description: str = ""):
        super().__init__(item_id, name, description)
        self.opens = opens

    def use(self, player, context) -> str:
        room = context.room
        opened = []
        for direction, key_id in list(room.locked_exits.items()):
            if key_id == self.opens:
                del room.locked_exits[direction]
                context.world_state.setdefault("opened_exits", []).append([room.room_id, direction])
                opened.append(direction)
        if not opened:
            return f"{self.name} не подходит ни к одной двери здесь."
        return f"{self.name} открывает выход: {', '.join(opened)}."


class Inventory:
    # инвентарь игрока

    def __init__(self):
        self._items: list[Item] = []

    def add(self, item: Item) -> None:
        self._items.append(item)

    def remove(self, item_id: str) -> Item | None:
        for i, it in enumerate(self._items):
            if it.item_id == item_id:
                return self._items.pop(i)
        return None

    def get(self, item_id: str) -> Item | None:
        for it in self._items:
            if it.item_id == item_id:
                return it
        return None

    def has(self, item_id: str) -> bool:
        return any(it.item_id == item_id for it in self._items)

    def all(self) -> list[Item]:
        return list(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Inventory({[it.item_id for it in self._items]})"