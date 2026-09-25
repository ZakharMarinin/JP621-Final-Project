import sys
from pathlib import Path

from models.character import Player
from engine.world_loader import WorldLoader
from engine.combat import start_combat
from engine.save_manager import SaveManager


class Game:
    def __init__(self):
        loader = WorldLoader("data/world.json")
        world = loader.load()

        self.rooms = world["rooms"]
        self.items = world["items"]
        self.start_room = world["start_room"]
        self.win_condition = world["win_condition"]

        self.player = Player("Hero")
        self.player.current_room = self.start_room

        self.defeated_enemies = set()
        self.taken_items = set()
        self.flags = {}

        self.save_manager = SaveManager()

    def current_room(self):
        return self.rooms[self.player.current_room]

    def start(self):
        print("Welcome to the dungeon!")
        print("Type 'help' to see the commands.")

        self.current_room().describe()

        while self.player.is_alive:
            command = input("\n> ").strip().lower()

            if command == "look":
                self.current_room().describe()

            elif command == "inventory":
                self.show_inventory()

            elif command.startswith("go "):
                direction = command[3:].strip()
                self.go(direction)

            elif command.startswith("take "):
                item_name = command[5:].strip()
                self.take_item(item_name)

            elif command.startswith("use "):
                item_name = command[4:].strip()
                self.use_item(item_name)

            elif command == "talk":
                self.talk()

            elif command.startswith("talk "):
                npc_name = command[5:].strip()
                self.talk(npc_name)

            elif command.startswith("attack "):
                enemy_name = command[7:].strip()
                self.attack_enemy(enemy_name)

            elif command == "save":
                self.save_manager.save(
                    "data/save1.json",
                    self.player,
                    self
                )

            elif command == "load":
                self.load_game("data/save1.json")

            elif command == "help":
                self.help()

            elif command == "quit":
                print("Goodbye!")
                break

            else:
                print("Unknown command. Type 'help'.")

            if self.check_win():
                print()
                print("You reached the throne room!")
                print("You won the game!")
                break

        if not self.player.is_alive:
            print("Game over.")

    def go(self, direction):
        room = self.current_room()

        if direction not in room.exits:
            print("You cannot go that way.")
            return

        exit_data = room.exits[direction]

        if isinstance(exit_data, str):
            destination = exit_data

        else:
            required_flag = exit_data["requires"]

            if not self.flags.get(required_flag, False):
                print("The door is locked.")
                return

            destination = exit_data["room"]

        self.player.current_room = destination

        print(f"You go {direction}.")
        self.current_room().describe()

    def show_inventory(self):
        if not self.player.inventory:
            print("Your inventory is empty.")
            return

        print("Inventory:")

        for item in self.player.inventory:
            print(f"- {item.name}")

        if self.player.equipped_weapon:
            print(
                f"Equipped weapon: "
                f"{self.player.equipped_weapon.name}"
            )

    def take_item(self, item_name):
        room = self.current_room()

        for item in room.items:
            if item.name.lower() == item_name:
                self.player.inventory.append(item)
                room.items.remove(item)
                self.taken_items.add(item.item_id)

                print(f"You took the {item.name}.")
                return

        print("That item is not here.")

    def use_item(self, item_name):
        for item in self.player.inventory:
            if item.name.lower() == item_name:
                should_remove = item.use(self.player, self)

                if should_remove:
                    self.player.inventory.remove(item)

                return

        print("You do not have that item.")

    def talk(self, npc_name=None):
        room = self.current_room()

        if not room.npcs:
            print("There is nobody here to talk to.")
            return

        if npc_name is None:
            for npc in room.npcs:
                print(f"{npc.name}: {npc.dialogue}")
            return

        for npc in room.npcs:
            if npc_name in npc.name.lower():
                print(f"{npc.name}: {npc.dialogue}")
                return

        print("That person is not here.")

    def attack_enemy(self, enemy_name):
        room = self.current_room()

        for enemy in room.enemies:
            if enemy.name.lower() == enemy_name:

                if not enemy.is_alive:
                    print("That enemy has already been defeated.")
                    return

                result = start_combat(self.player, enemy)

                if result == "win":
                    self.defeated_enemies.add(enemy.enemy_id)
                    room.enemies.remove(enemy)

                return

        print("That enemy is not here.")

    def check_win(self):
        if self.win_condition["type"] == "reach_room":
            return (
                self.player.current_room
                == self.win_condition["room"]
            )

        return False

    def load_game(self, filename):
        try:
            data = self.save_manager.load(filename)

            player_data = data["player"]
            world_state = data["world_state"]

            self.player.current_room = player_data["current_room"]
            self.player.hp = player_data["hp"]

            self.defeated_enemies = set(
                world_state["defeated_enemies"]
            )

            self.taken_items = set(
                world_state["taken_items"]
            )

            self.flags = world_state["flags"]

            self.player.inventory = []

            for item_id in player_data["inventory"]:
                if item_id in self.items:
                    self.player.inventory.append(
                        self.items[item_id]
                    )

            # Remove items already taken before saving
            for room in self.rooms.values():
                room.items = [
                    item
                    for item in room.items
                    if item.item_id not in self.taken_items
                ]

            # Remove enemies already defeated before saving
            for room in self.rooms.values():
                room.enemies = [
                    enemy
                    for enemy in room.enemies
                    if enemy.enemy_id not in self.defeated_enemies
                ]

            print("Game loaded.")

        except ValueError as error:
            print(error)

    def help(self):
        print()
        print("Commands:")
        print("look")
        print("go <direction>")
        print("take <item>")
        print("use <item>")
        print("inventory")
        print("talk")
        print("talk <person>")
        print("attack <enemy>")
        print("save")
        print("load")
        print("help")
        print("quit")


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--load":

            if len(sys.argv) < 3:
                print("Please provide a save file.")
                print(
                    "Example: "
                    "python main.py --load data/save1.json"
                )

            else:
                game = Game()
                game.load_game(sys.argv[2])
                game.start()

        elif len(sys.argv) > 1 and sys.argv[1] == "--new-game":
            game = Game()
            game.start()

        else:
            game = Game()
            game.start()

    except ValueError as error:
        print(f"Error: {error}")