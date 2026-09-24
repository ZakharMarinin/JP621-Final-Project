import argparse
import sys
from pathlib import Path
from types import SimpleNamespace

from engine.world_loader import WorldLoader, World
from engine.save_manager import SaveManager, apply_world_state
from engine.combat import run_combat
from models.character import Player
from models.room import Room


WORLD_PATH = "data/world.json"
DEFAULT_SAVE = "data/save1.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Подземелье — текстовый квест.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--new-game", action="store_true", help="Начать новую игру")
    group.add_argument("--load", metavar="FILE", help="Загрузить сохранение")
    return parser.parse_args()


def describe_room(world: World, player: Player) -> None:
    room = world.get_room(player.current_room)
    print(f"\n=== {player.current_room} ===")
    print(room.description)

    if room.items:
        print("\nПредметы:")
        for it in room.items:
            print(f"  • {it.name} ({it.item_id})")

    if room.enemies:
        print("\nПротивники:")
        for e in room.enemies:
            print(f"  - {e.name} (HP {e.hp}/{e.max_hp}, урон {e.damage})")

    if room.npcs:
        print("\nПерсонажи:")
        for n in room.npcs:
            print(f"  - {n.name}")

    if room.exits:
        print("\nВыходы: " + ", ".join(room.exits.keys()))
        for direction, key_id in room.locked_exits.items():
            print(f"  (выход '{direction}' заперт — нужен предмет '{key_id}')")
    else:
        print("\nВыходов нет.")


def show_inventory(player: Player) -> None:
    print(f"\n=== Инвентарь ({len(player.inventory)} предметов) ===")
    if player.inventory.is_empty():
        print("  (пусто)")
        return
    for it in player.inventory.all():
        print(f"  • {it.name} ({it.item_id}) — {it.description}")


def do_take(world: World, player: Player, arg: str, world_state: dict) -> None:
    room = world.get_room(player.current_room)
    if not arg:
        print("Укажите, что взять. Пример: take rusty_key")
        return
    item = room.remove_item(arg)
    if item is None:
        print(f"В комнате нет предмета '{arg}'.")
        return
    player.inventory.add(item)
    world_state.setdefault("taken_items", []).append(item.item_id)
    print(f"Вы взяли: {item.name}.")


def do_use(world: World, player: Player, arg: str, world_state: dict) -> None:
    if not arg:
        print("Укажите, что использовать. Пример: use health_potion")
        return
    item = player.inventory.get(arg)
    if item is None:
        print(f"В инвентаре нет предмета '{arg}'.")
        return

    room = world.get_room(player.current_room)
    context = SimpleNamespace(room=room, world_state=world_state, world=world)

    # полиморфный вызов: каждый класс сам решает, что делать
    print(item.use(player, context))

    if item.is_consumable():
        player.inventory.remove(item.item_id)

def do_go(world: World, player: Player, arg: str, world_state: dict) -> bool:
    if not arg:
        print("Укажите направление, например: go north")
        return False
    room = world.get_room(player.current_room)
    direction = arg.lower()
    if direction not in room.exits:
        print(f"Нельзя пойти на '{direction}'. Доступно: {', '.join(room.exits) or '—'}")
        return False
    if direction in room.locked_exits:
        key_id = room.locked_exits[direction]
        if not player.inventory.has(key_id):
            print(f"Выход '{direction}' заперт. Нужен предмет: {key_id}.")
            return False
        del room.locked_exits[direction]
        world_state.setdefault("opened_exits", []).append([room.room_id, direction])
        print(f"Вы открываете дверь '{direction}' ключом и проходите.")

    player.current_room = room.exits[direction]
    return True


def do_talk(world: World, player: Player, arg: str, world_state: dict) -> None:
    if not arg:
        print("С кем поговорить? Пример: talk old_guard")
        return
    room = world.get_room(player.current_room)
    needle = arg.lower()
    npc = None
    for n in room.npcs:
        if needle in n.name.lower() or needle == getattr(n, "npc_id", "").lower():
            npc = n
            break
    if npc is None:
        print(f"Здесь нет НПС '{arg}', но есть: {', '.join(n.name for n in room.npcs) or '—'}")
        return

    print(f"\n{npc.name}: \"{npc.talk()}\"")

    if npc.reward and not player.inventory.has(npc.reward):
        reward_item = world.make_item_by_id(npc.reward)
        player.inventory.add(reward_item)
        world_state.setdefault("taken_items", []).append(npc.reward)
        print(f"\n{npc.name} даёт вам: {reward_item.name}.")
        npc.reward = None


def do_attack(world: World, player: Player, arg: str, world_state: dict) -> bool:
    room = world.get_room(player.current_room)
    if not room.enemies:
        print("Здесь некого атаковать")
        return False
    if not arg:
        print("Кого атаковать? Пример: attack goblin")
        return False

    needle = arg.lower()
    enemy = None
    for e in room.enemies:
        if needle in e.name.lower() or needle == getattr(e, "enemy_id", "").lower():
            enemy = e
            break

    if enemy is None:
        print(f"Здесь нет '{arg}'. Есть: {', '.join(e.name for e in room.enemies)}")
        return False

    result = run_combat(player, enemy)

    if result == "win":
        room.remove_enemy(enemy.name)
        world_state.setdefault("defeated_enemies", []).append(enemy.name)
        if enemy.loot:
            loot = world.make_item_by_id(enemy.loot)
            room.add_item(loot)
            print(f"С врага выпало: {loot.name}.")
        return True
    if result == "lose":
        print("\nВы проиграли. Игра завершена")
        print("Загрузите сохранение через --load или начните заново")
        sys.exit(0)
    return False


def check_win(world: World, player: Player, world_state: dict) -> bool:
    cond = world.win_condition or {}
    ctype = cond.get("type")

    if ctype == "defeat_enemy":
        return cond.get("enemy") in world_state.get("defeated_enemies", [])
    if ctype == "reach_room":
        return player.current_room == cond.get("room")
    if ctype == "collect_item":
        return player.inventory.has(cond.get("item"))
    return False


def game_loop(world: World, player: Player, world_state: dict, save_path: str) -> None:
    print("\n============ Приветствуем в подземелье! ============")
    print("Введите help для списка команд.")
    describe_room(world, player)

    while True:
        try:
            raw = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            return

        if not raw:
            continue

        parts = raw.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        try:
            if cmd in ("quit", "exit", "выход"):
                print("До встречи!")
                return

            elif cmd in ("help", "помощь", "?"):
                print("""
Команды:
  look                        — осмотреть комнату
  go <direction>              — перейти (north/south/east/west)
  inventory                   — инвентарь
  take <item_id>              — взять предмет
  use <item_id>               — использовать предмет
  talk <npc>                  — поговорить с НПС
  attack <enemy>              — атаковать противника
  save                        — сохранить игру
  quit                        — выйти
""")

            elif cmd in ("look", "осмотреться", "l"):
                describe_room(world, player)

            elif cmd in ("go", "идти", "ид"):
                do_go(world, player, arg, world_state)
                describe_room(world, player)
                if check_win(world, player, world_state):
                    print("\nПобеда! Вы прошли подземелье")
                    return

            elif cmd in ("inventory", "inv", "инвентарь", "i"):
                show_inventory(player)

            elif cmd in ("take", "взять"):
                do_take(world, player, arg, world_state)

            elif cmd in ("use", "использовать"):
                do_use(world, player, arg, world_state)

            elif cmd in ("talk", "говорить"):
                do_talk(world, player, arg, world_state)

            elif cmd in ("attack", "атаковать", "fight"):
                do_attack(world, player, arg, world_state)
                if check_win(world, player, world_state):
                    print("\nПобеда! Вы прошли подземелье")
                    return

            elif cmd in ("save", "сохранить"):
                SaveManager(save_path).save(player, world_state)
                print(f"Игра сохранена в {save_path}.")

            else:
                print(f"Неизвестная команда: '{cmd}'. Введите 'help'")

        except Exception as e:
            print(f"Ошибка при выполнении команды {e}")


def main() -> None:
    args = parse_args()

    try:
        world = WorldLoader(WORLD_PATH).load()
    except (FileNotFoundError, ValueError) as e:
        print(f"Не удалось загрузить мир: {e}")
        sys.exit(1)

    world_state = {"defeated_enemies": [], "taken_items": [], "opened_exits": [], "flags": {}}

    if args.new_game:
        player = world.make_new_player("Rodion")
        save_path = DEFAULT_SAVE
    else:
        save_path = args.load
        try:
            player, world_state = SaveManager(save_path).load(world)
        except (FileNotFoundError, ValueError) as e:
            print(f"Не удалось загрузить сохранение: {e}")
            sys.exit(1)
        apply_world_state(world, world_state)

    game_loop(world, player, world_state, save_path)


if __name__ == "__main__":
    main()