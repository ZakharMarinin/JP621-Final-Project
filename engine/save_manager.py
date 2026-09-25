import json
from datetime import datetime


class SaveManager:
    def save(self, filename, player, game):
        data = {
            "player": {
                "current_room": player.current_room,
                "hp": player.hp,
                "max_hp": player.max_hp,
                "inventory": [
                    item.item_id for item in player.inventory
                ]
            },

            "world_state": {
                "defeated_enemies": list(game.defeated_enemies),
                "taken_items": list(game.taken_items),
                "flags": game.flags
            },

            "saved_at": datetime.now().isoformat()
        }

        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            print(f"Game saved to {filename}.")

        except OSError:
            print("Could not save the game.")

    def load(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)

        except FileNotFoundError:
            raise ValueError("Save file was not found.")

        except json.JSONDecodeError:
            raise ValueError("Save file contains invalid JSON.")