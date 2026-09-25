import argparse
import sys
from storage.repository import Repository, StorageError
from services.pet_service import PetService, PetNotFoundError
from models.pet import PetIsDeadError, PetIsSleepingError, SPECIES_MAP


def print_pet_brief(pet):
    print(f"  {pet.name} | вид: {pet.SPECIES} | статус: {pet.status_text()}")


def main():
    parser = argparse.ArgumentParser(description="Терравариум — виртуальные питомцы")
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add-pet", help="Завести питомца")
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--species", required=True, choices=list(SPECIES_MAP.keys()))

    sub.add_parser("list", help="Список питомцев")

    for cmd in ["status", "feed", "play", "sleep", "heal", "release", "ability"]:
        sp = sub.add_parser(cmd)
        sp.add_argument("--name", required=True)

    p_hist = sub.add_parser("history")
    p_hist.add_argument("--name", required=True)
    p_hist.add_argument("-n", type=int, default=10)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    try:
        repo = Repository("data/pets.json")
        service = PetService(repo)

        if args.command == "add-pet":
            pet = service.add_pet(args.name, args.species)
            print(f"Создан питомец {pet.name} ({pet.SPECIES}). {pet.make_sound()}")

        elif args.command == "list":
            pets = service.list_pets()
            if not pets:
                print("Питомцев нет.")
            else:
                print("Питомцы:")
                for p in pets:
                    print_pet_brief(p)

        elif args.command == "status":
            pet = service.status(args.name)
            print(f"Имя: {pet.name}")
            print(f"Вид: {pet.SPECIES}")
            print(f"Состояние: {pet.status_text()}")
            print(f"Голод: {int(pet.hunger)}")
            print(f"Энергия: {int(pet.energy)}")
            print(f"Здоровье: {int(pet.health)}")
            print(f"Настроение: {int(pet.mood)}")

        elif args.command == "feed":
            print(service.feed(args.name))
        elif args.command == "play":
            print(service.play(args.name))
        elif args.command == "sleep":
            print(service.sleep(args.name))
        elif args.command == "heal":
            print(service.heal(args.name))
        elif args.command == "ability":
            print(service.ability(args.name))
        elif args.command == "release":
            confirm = input(f"Точно отпустить {args.name}? (y/n): ").lower()
            if confirm == "y":
                print(service.release(args.name))
            else:
                print("Отменено.")
        elif args.command == "history":
            records = service.history(args.name, args.n)
            if not records:
                print("История пуста.")
            else:
                for r in records:
                    print(f"[{r['timestamp']}] {r['event']}: {r['details']}")

    except (PetNotFoundError, PetIsDeadError, PetIsSleepingError,
            StorageError, ValueError) as e:
        print(f"Ошибка: {e}")
    except KeyboardInterrupt:
        print("\nПрервано.")


if __name__ == "__main__":
    sys.exit(main())