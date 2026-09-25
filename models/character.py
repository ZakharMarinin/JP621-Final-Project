from abc import ABC, abstractmethod


class Character(ABC):
    def __init__(self, name, hp, max_hp):
        self.name = name
        self._hp = hp
        self._max_hp = max_hp

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        if value < 0:
            self._hp = 0
        elif value > self._max_hp:
            self._hp = self._max_hp
        else:
            self._hp = value

    @property
    def max_hp(self):
        return self._max_hp

    @property
    @abstractmethod
    def is_alive(self):
        pass

    @abstractmethod
    def attack(self, target):
        pass


class Player(Character):
    def __init__(self, name="Hero", hp=100, max_hp=100):
        super().__init__(name, hp, max_hp)
        self.current_room = None
        self.inventory = []
        self.equipped_weapon = None

    @property
    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        if self.equipped_weapon:
            damage = self.equipped_weapon.damage
        else:
            damage = 3

        target.hp -= damage
        print(f"You attack {target.name} for {damage} damage.")


class Enemy(Character):
    def __init__(self, enemy_id, name, hp, damage):
        super().__init__(name, hp, hp)
        self.enemy_id = enemy_id
        self.damage = damage

    @property
    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        target.hp -= self.damage
        print(f"{self.name} attacks you for {self.damage} damage.")


class NPC(Character):
    def __init__(self, npc_id, name, dialogue):
        super().__init__(name, 1, 1)
        self.npc_id = npc_id
        self.dialogue = dialogue

    @property
    def is_alive(self):
        return True

    def attack(self, target):
        print(f"{self.name} does not want to fight.")