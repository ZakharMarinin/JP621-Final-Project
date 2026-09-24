import json
from datetime import datetime
from pathlib import Path

from models.character import Player
from engine.world_loader import World


class SaveManager:
    # сохранение и загрузка

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def save(self, player: Player, world_state: dict) -> None:
        data = {
            "player": {
                "current_room": player.current_room,
                "hp": player.hp,
                "max_hp": player.max_hp,
                "damage": player.damage,
                "inventory": [it.item_id for it in player.inventory.all()],
            },
            "world_state": world_state,
            "saved_at": datetime.now().isoformat(timespec="seconds"),
        }

        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise OSError(f"Не удалось записать сохранение: {e}")

    def load(self, world: World) -> tuple[Player, dict]:
        if not self.path.exists():
            raise FileNotFoundError(f"Сохранение не найдено: {self.path}")

        try:
            with self.path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Файл сохранения повреждён: {e}")

        if "player" not in data or "world_state" not in data:
            raise ValueError("В сохранении нет разделов 'player' / 'world_state'.")

        pdata = data["player"]
        player = Player(pdata.get("name", "Игрок"),
                        max_hp=pdata.get("max_hp", 100),
                        damage=pdata.get("damage", 8))
        player.hp = pdata.get("hp", player.max_hp)
        player.current_room = pdata.get("current_room", world.start_room)

        for item_id in pdata.get("inventory", []):
            try:
                player.inventory.add(world.make_item_by_id(item_id))
            except KeyError:
                continue

        return player, data["world_state"]


def apply_world_state(world: World, state: dict) -> None:
    # удаление всего не нужногг
    defeated = set(state.get("defeated_enemies", []))
    taken = set(state.get("taken_items", []))
    opened = {tuple(pair) for pair in state.get("opened_exits", [])}

    for room in world.rooms.values():
        room.enemies = [e for e in room.enemies if e.name not in defeated]
        room.items = [it for it in room.items if it.item_id not in taken]
        for direction in list(room.locked_exits.keys()):
            if (room.room_id, direction) in opened:
                del room.locked_exits[direction]