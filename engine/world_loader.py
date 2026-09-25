import json

from models.room import Room
from models.character import Enemy, NPC
from models.item import Potion, Weapon, Key


class WorldLoader:
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

        except FileNotFoundError:
            raise ValueError("World file was not found.")

        except json.JSONDecodeError:
            raise ValueError("World file has invalid JSON.")

        items = {}

        for item_id, item_data in data["items"].items():

            if item_data["type"] == "potion":
                item = Potion(
                    item_id,
                    item_data["name"],
                    item_data["heal"]
                )

            elif item_data["type"] == "weapon":
                item = Weapon(
                    item_id,
                    item_data["name"],
                    item_data["damage"]
                )

            elif item_data["type"] == "key":
                item = Key(
                    item_id,
                    item_data["name"],
                    item_data["opens"]
                )

            else:
                continue

            items[item_id] = item

        enemies = {}

        for enemy_id, enemy_data in data["enemies"].items():
            enemies[enemy_id] = Enemy(
                enemy_id,
                enemy_data["name"],
                enemy_data["hp"],
                enemy_data["damage"]
            )

        npcs = {}

        for npc_id, npc_data in data["npcs"].items():
            npcs[npc_id] = NPC(
                npc_id,
                npc_data["name"],
                npc_data["dialogue"]
            )

        rooms = {}

        for room_id, room_data in data["rooms"].items():

            room_items = [
                items[item_id]
                for item_id in room_data.get("items", [])
            ]

            room_enemies = [
                Enemy(
                    enemy_id,
                    enemies[enemy_id].name,
                    enemies[enemy_id].hp,
                    enemies[enemy_id].damage
                )
                for enemy_id in room_data.get("enemies", [])
            ]

            room_npcs = [
                npcs[npc_id]
                for npc_id in room_data.get("npcs", [])
            ]

            rooms[room_id] = Room(
                room_id,
                room_data["description"],
                room_data["exits"],
                room_items,
                room_enemies,
                room_npcs
            )

        return {
            "rooms": rooms,
            "items": items,
            "start_room": data["start_room"],
            "win_condition": data["win_condition"]
        }