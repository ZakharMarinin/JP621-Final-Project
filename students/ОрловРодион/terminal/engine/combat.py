from models.character import Character


def run_combat(player: Character, enemy: Character, input_fn=input, print_fn=print) -> str:
    # пошаговый бой

    print_fn(f"\nНачался бой: {player.name} (HP {player.hp}/{player.max_hp}) "
             f"против {enemy.name} (HP {enemy.hp}/{enemy.max_hp})")

    while player.is_alive() and enemy.is_alive():
        print_fn(f"\n--- Ваш ход (HP {player.hp}/{player.max_hp}) | "
                 f"{enemy.name}: {enemy.hp}/{enemy.max_hp} ---")
        print_fn("Команды [a]таковать  [f]бежать")

        raw = input_fn("> ").strip().lower()

        if raw in ("a", "а", "attack", "атаковать", "удар", "бить"):
            print_fn(player.attack(enemy))

            if not enemy.is_alive():
                print_fn(f"\n{enemy.name} побеждён")
                return "win"

            print_fn(enemy.attack(player))

            if not player.is_alive():
                print_fn(f"\n{player.name} погибает")
                return "lose"

        elif raw in ("f", "ф", "flee", "бежать", "убежать", "побег"):
            import random
            if random.random() < 0.5:
                print_fn("Вы в ужасе, позорно сбежали :()")
                return "flee"
            print_fn("Вам не удалось сбежать")
            print_fn(enemy.attack(player))
            if not player.is_alive():
                print_fn(f"\n{player.name} погибает")
                return "lose"

        else:
            print_fn("Неизвестная команда. Введите 'a' для атаки или 'f' для побега.")

    return "win" if player.is_alive() else "lose"