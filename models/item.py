from abc import ABC, abstractmethod


class Item(ABC):
    def __init__(self, item_id, name):
        self.item_id = item_id
        self.name = name

    @abstractmethod
    def use(self, player, game):
        pass


class Potion(Item):
    def __init__(self, item_id, name, heal):
        super().__init__(item_id, name)
        self.heal = heal

    def use(self, player, game):
        player.hp += self.heal
        print(f"You used {self.name}.")
        print(f"You healed {self.heal} HP.")
        return True


class Weapon(Item):
    def __init__(self, item_id, name, damage):
        super().__init__(item_id, name)
        self.damage = damage

    def use(self, player, game):
        player.equipped_weapon = self
        print(f"You equipped {self.name}.")
        print(f"Your damage is now {self.damage}.")
        return False


class Key(Item):
    def __init__(self, item_id, name, opens):
        super().__init__(item_id, name)
        self.opens = opens

    def use(self, player, game):
        game.flags[self.opens] = True
        print(f"You used the {self.name}.")
        print("The locked door is now open.")
        return False