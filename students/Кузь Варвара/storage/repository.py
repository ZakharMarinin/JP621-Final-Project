import json
import os
from models.pet import SPECIES_MAP
from models.inventory import Inventory


class StorageError(Exception):
    pass


class Repository:
    def __init__(self, path="data/pets.json"):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            self._save({"pets": [], "resources": {"medkits": 3}})

    def _load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise StorageError("Файл базы повреждён. Исправьте или удалите data/pets.json")
        except OSError as e:
            raise StorageError(f"Ошибка чтения базы: {e}")

    def _save(self, data):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise StorageError(f"Ошибка записи базы: {e}")

    def load_pets(self):
        data = self._load()
        result = []
        for item in data.get("pets", []):
            cls = SPECIES_MAP.get(item["species"])
            if not cls:
                continue
            stats = item.get("stats", {})
            pet = cls(
                name=item["name"],
                created_at=item.get("created_at"),
                last_updated=item.get("last_updated"),
                hunger=stats.get("hunger", 30),
                energy=stats.get("energy", 80),
                health=stats.get("health", 100),
                mood=stats.get("mood", 80),
                state=item.get("state", "awake"),
                history=item.get("history", []),
            )
            result.append(pet)
        return result

    def save_pets(self, pets, inventory):
        data = {
            "pets": [p.to_dict() for p in pets],
            "resources": inventory.to_dict(),
        }
        self._save(data)

    def load_inventory(self):
        data = self._load()
        return Inventory.from_dict(data.get("resources", {}))