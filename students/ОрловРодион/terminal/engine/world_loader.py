import json
from pathlib import Path

from models.room import Room
from models.item import Item, Potion, Weapon, Key
from models.character import Player, Enemy, Goblin, Skeleton, NPC


class WorldLoader:
    # чтение мира

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.raw: dict = {}

    def load(self) -> "World":
        if not self.path.exists():
            raise FileNotFoundError(f"Не найден файл мира: {self.path}")

        try:
            with self.path.open("r", encoding="utf-8") as f:
                self.raw = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Файл мира повреждён (некорректный JSON): {e}")

        return self._build_world()

    def _build_world(self) -> "World":
        items = self._build_items(self.raw.get("items", {}))
        enemies_proto = self.raw.get("enemies", {})
        npcs_proto = self.raw.get("npcs", {})
        rooms = self._build_rooms(self.raw.get("rooms", {}), items, enemies_proto, npcs_proto)

        return World(
            rooms=rooms,
            start_room=self.raw.get("start_room"),
            win_condition=self.raw.get("win_condition", {}),
            raw=self.raw,
        )

    def _build_items(self, raw_items: dict) -> dict[str, Item]:
        items: dict[str, Item] = {}
        for item_id, data in raw_items.items():
            itype = data.get("type")
            if itype == "potion":
                items[item_id] = Potion(item_id, data["name"], heal=data["heal"],
                                        description=data.get("description", ""))
            elif itype == "weapon":
                items[item_id] = Weapon(item_id, data["name"], bonus_damage=data["bonus_damage"],
                                        description=data.get("description", ""))
            elif itype == "key":
                items[item_id] = Key(item_id, data["name"], opens=data["opens"],
                                     description=data.get("description", ""))
            else:
                raise ValueError(f"Неизвестный тип предмета '{itype}' у '{item_id}'")
        return items

    def _build_rooms(self, raw_rooms, items_proto, enemies_proto, npcs_proto) -> dict[str, Room]:
        rooms: dict[str, Room] = {}
        for room_id, data in raw_rooms.items():
            room = Room(room_id, data["description"], exits=data.get("exits", {}))
            room.locked_exits = dict(data.get("locked_exits", {}))

            for item_id in data.get("items", []):
                if item_id not in items_proto:
                    raise ValueError(f"Комната '{room_id}' ссылается на неизвестный предмет '{item_id}'")
                room.add_item(self._clone_item(items_proto[item_id]))

            for enemy_id in data.get("enemies", []):
                if enemy_id not in enemies_proto:
                    raise ValueError(f"Комната '{room_id}' ссылается на неизвестного врага '{enemy_id}'")
                room.add_enemy(self._make_enemy(enemy_id, enemies_proto[enemy_id]))

            for npc_id in data.get("npcs", []):
                if npc_id not in npcs_proto:
                    raise ValueError(f"Комната '{room_id}' ссылается на неизвестного NPC '{npc_id}'")
                room.add_npc(self._make_npc(npc_id, npcs_proto[npc_id]))

            rooms[room_id] = room
        return rooms

    @staticmethod
    def _clone_item(item: Item) -> Item:
        if isinstance(item, Potion):
            return Potion(item.item_id, item.name, item.heal, item.description)
        if isinstance(item, Weapon):
            return Weapon(item.item_id, item.name, item.bonus_damage, item.description)
        if isinstance(item, Key):
            return Key(item.item_id, item.name, item.opens, item.description)
        raise TypeError(f"Неизвестный класс предмета: {type(item).__name__}")

    @staticmethod
    def _make_enemy(enemy_id: str, data: dict) -> Enemy:
        cls = data.get("class", "Enemy")
        name = data["name"]
        hp = data["hp"]
        dmg = data["damage"]
        loot = data.get("loot")

        if cls == "Goblin":
            e = Goblin(name, hp, dmg, loot=loot)
        elif cls == "Skeleton":
            e = Skeleton(name, hp, dmg, loot=loot)
        else:
            e = Enemy(name, hp, dmg, loot=loot)

        e.enemy_id = enemy_id
        return e

    @staticmethod
    def _make_npc(npc_id: str, data: dict) -> NPC:
        n = NPC(data["name"], data["dialogue"], reward=data.get("reward"))
        n.npc_id = npc_id
        return n


class World:
    # контейнер мира

    def __init__(self, rooms: dict[str, Room], start_room: str,
                 win_condition: dict, raw: dict):
        self.rooms = rooms
        self.start_room = start_room
        self.win_condition = win_condition
        self.raw = raw

    def get_room(self, room_id: str) -> Room:
        return self.rooms[room_id]

    def make_new_player(self, name: str = "Игрок") -> Player:
        p = Player(name)
        p.current_room = self.start_room
        return p

    def make_item_by_id(self, item_id: str) -> Item:
        proto = self.raw["items"][item_id]
        t = proto["type"]
        if t == "potion":
            return Potion(item_id, proto["name"], proto["heal"], proto.get("description", ""))
        if t == "weapon":
            return Weapon(item_id, proto["name"], proto["bonus_damage"], proto.get("description", ""))
        if t == "key":
            return Key(item_id, proto["name"], proto["opens"], proto.get("description", ""))
        raise ValueError(f"Неизвестный тип предмета: {t}")