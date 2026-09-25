def start_combat(player, enemy):
    print()
    print(f"A fight started with {enemy.name}!")

    while player.is_alive and enemy.is_alive:
        print()
        print(f"Your HP: {player.hp}/{player.max_hp}")
        print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")

        print("1. Attack")
        print("2. Run")

        choice = input("> ").lower()

        if choice == "1" or choice == "attack":
            player.attack(enemy)

            if enemy.is_alive:
                enemy.attack(player)

        elif choice == "2" or choice == "run":
            print("You ran away.")
            return "run"

        else:
            print("Invalid choice.")

    if player.is_alive:
        print(f"You defeated {enemy.name}!")
        return "win"

    print("You lost the fight.")
    return "lose"