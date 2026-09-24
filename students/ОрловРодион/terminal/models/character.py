from abc import ABC, abstractmethod
import random


class Character(ABC):
    # базовый класс персонажа

    def __init__(self, name: str, max_hp: int, damage: int):
        self.name = name
        self._max_hp = max_hp
        self._hp = max_hp
        self.damage = damage

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        if value < 0:
            value = 0
        elif value > self._max_hp:
            value = self._max_hp
        self._hp = value

    @property
    def max_hp(self) -> int:
        return self._max_hp

    @abstractmethod
    def attack(self, target: "Character") -> str:
        ...

    @abstractmethod
    def is_alive(self) -> bool:
        ...

    def take_damage(self, amount: int) -> int:
        amount = max(0, amount)
        self.hp = self._hp - amount
        return amount

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, hp={self.hp}/{self.max_hp})"


class Player(Character):
    def __init__(self, name: str = "Игрок", max_hp: int = 100, damage: int = 8):
        super().__init__(name, max_hp, damage)
        from models.item import Inventory
        self.inventory = Inventory()
        self.current_room: str | None = None

    def attack(self, target: Character) -> str:
        dealt = target.take_damage(self.damage)
        return f"{self.name} бьёт {target.name} на {dealt} урона."

    def is_alive(self) -> bool:
        return self.hp > 0


class Enemy(Character):
    def __init__(self, name: str, max_hp: int, damage: int, loot: str | None = None):
        super().__init__(name, max_hp, damage)
        self.loot = loot

    def attack(self, target: Character) -> str:
        dealt = target.take_damage(self.damage)
        return f"{self.name} атакует {target.name} на {dealt} урона."

    def is_alive(self) -> bool:
        return self.hp > 0


class Goblin(Enemy):
    def attack(self, target: Character) -> str:
        # 25% шанс крита
        if random.random() < 0.25:
            dealt = target.take_damage(self.damage * 2)
            return f"{self.name} сильно кусает {target.name} на {dealt} урона (крит!)."
        return super().attack(target)


class Skeleton(Enemy):
    def attack(self, target: Character) -> str:
        dealt = target.take_damage(self.damage)
        return f"{self.name} рубит костяным мечом {target.name} на {dealt} урона."


class NPC(Character):
    def __init__(self, name: str, dialogue: str, reward: str | None = None):
        super().__init__(name, max_hp=10, damage=0)
        self.dialogue = dialogue
        self.reward = reward

    def attack(self, target: Character) -> str:
        return f"{self.name} не хочет драться."

    def is_alive(self) -> bool:
        return True

    def talk(self) -> str:
        return self.dialogue