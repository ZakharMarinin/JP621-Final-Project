from __future__ import annotations

import sys

from game.actions import actions_for, perform
from game.config import SAVE_PATH, TARGET_AGE
from game.pet import Pet
from game.species import SPECIES, SPECIES_ORDER, Species
from game.storage import SaveError, clear, load_state, save_state
from game.ui import render_menu, render_stats

EXIT_LABEL = "Выйти из игры (прогресс сохранится)"


def choose_species() -> Species:
    print("Кого заведём в терравариуме?")
    for number, species in enumerate(SPECIES_ORDER, start=1):
        profile = SPECIES[species]
        print(f"  {number}. {profile.display_name} — {profile.tagline}")

    while True:
        raw = input(f"Номер (1-{len(SPECIES_ORDER)}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(SPECIES_ORDER):
            return SPECIES_ORDER[int(raw) - 1]
        print("  Не понял. Введи число из списка.")


def choose_name(species: Species) -> str:
    default = SPECIES[species].display_name
    raw = input(f"Как назовём? (Enter — «{default}»): ").strip()
    return raw or default


def ask_choice(count: int) -> int:
    while True:
        raw = input(f"Твой выбор (1-{count}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= count:
            return int(raw)
        print("  Не понял. Введи номер из меню.")


def ask_yes_no(question: str) -> bool:
    yes = {"да", "д", "y", "yes", "1"}
    no = {"нет", "н", "n", "no", "0"}
    while True:
        raw = input(f"{question} (да/нет): ").strip().lower()
        if raw in yes:
            return True
        if raw in no:
            return False
        print("  Ответь «да» или «нет».")


def new_pet() -> Pet:
    species = choose_species()
    name = choose_name(species)
    pet = Pet(name=name, species=species)
    print()
    print(f"В терравариуме появился {pet.display_species} по имени {pet.name}!")
    print(f"Цель: прожить {TARGET_AGE} ходов, не дав ему умереть.")
    print()
    return pet


def play_game(pet: Pet, record: int) -> bool:
    while pet.alive and not pet.is_adult:
        print(render_stats(pet))
        print()
        actions = actions_for(pet)
        labels = [action.label for action in actions] + [EXIT_LABEL]
        print(render_menu(labels))

        choice = ask_choice(len(labels))
        if choice == len(labels):
            save_state(pet, record)
            print()
            print("Выходим. Прогресс сохранён — питомец будет ждать тебя.")
            return False

        print()
        for note in perform(pet, actions[choice - 1]):
            print(f"  • {note}")
        print()

        save_state(pet, record)

    return True


def finish_line(pet: Pet) -> str:
    if pet.is_adult:
        return f"{pet.name} вырос! Ты продержался {pet.age} ходов из {TARGET_AGE}."
    return f"{pet.name}: {pet.death_message.lower()}. Прожито ходов: {pet.age}."


def main() -> None:
    if "--reset" in sys.argv:
        clear()
        print("Сохранение стёрто — начинаем с чистого листа.")
        print()

    try:
        pet, record = load_state()
    except SaveError as error:
        print("Не удалось прочитать сохранение:")
        print(f"  {error}")
        print(f"  Файл: {SAVE_PATH}")
        print()
        if not ask_yes_no("Стереть его и начать заново?"):
            return
        clear()
        pet, record = None, 0

    if pet is not None and pet.alive and not pet.is_adult:
        print("Продолжаем прошлую партию.")
        print()

    while True:
        if pet is None:
            pet = new_pet()

        if pet.alive and not pet.is_adult:
            if not play_game(pet, record):
                return

        record = max(record, pet.age)
        save_state(pet, record)

        print(render_stats(pet))
        print()
        print(finish_line(pet))
        print(f"Личный рекорд: {record} ходов.")
        print()

        if not ask_yes_no("Завести нового питомца?"):
            print(f"Пока! Питомец ждёт тебя (сохранение: {SAVE_PATH.name}).")
            return
        print()
        pet = None


if __name__ == "__main__":
    main()