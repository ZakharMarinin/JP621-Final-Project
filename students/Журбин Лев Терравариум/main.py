import sys
import json
import os
import argparse
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


# ==========================================
# вспомогательные цвета (ANSI)
# ==========================================
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def print_success(msg: str):
    print(f"{Colors.GREEN}✔ {msg}{Colors.RESET}")


def print_warning(msg: str):
    print(f"{Colors.YELLOW} {msg}{Colors.RESET}")


def print_error(msg: str):
    print(f"{Colors.RED} Ошибка: {msg}{Colors.RESET}")


def print_info(msg: str):
    print(f"{Colors.CYAN}{msg}{Colors.RESET}")


# ==========================================
# 1. ООП модели питомцев (Абстракция, Инкапсуляция, Наследование, Полиморфизм)
# ==========================================
class Pet(ABC):
    """абстрактивный класс питомца."""

    def __init__(self, name: str, species: str, created_at: str = None, last_updated: str = None,
                 stats: dict = None, state: str = "awake", history: list = None):
        self.name = name
        self.species = species

        now_str = datetime.now().isoformat(timespec='seconds')
        self.created_at = created_at or now_str
        self.last_updated = last_updated or now_str

        # Инкапсуляция показателей
        default_stats = {"hunger": 0, "energy": 100, "health": 100, "mood": 100}
        stats = stats or default_stats

        self._hunger = stats.get("hunger", 0)
        self._energy = stats.get("energy", 100)
        self._health = stats.get("health", 100)
        self._mood = stats.get("mood", 100)

        self.state = state  # "awake", "sleeping", "sick", "dead"
        self.history = history if history is not None else []

    # Геттеры и сеттеры с валидацией границ [0, 100]
    @property
    def hunger(self):
        return self._hunger

    @hunger.setter
    def hunger(self, val):
        self._hunger = max(0, min(100, val))

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, val):
        self._energy = max(0, min(100, val))

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, val):
        self._health = max(0, min(100, val))

    @property
    def mood(self):
        return self._mood

    @mood.setter
    def mood(self, val):
        self._mood = max(0, min(100, val))

    def add_history(self, event: str, details: str):
        now_str = datetime.now().isoformat(timespec='seconds')
        self.history.append({"timestamp": now_str, "event": event, "details": details})

    @abstractmethod
    def update_over_time(self, hours_passed: float):
        """Расчет изменения характеристик со временем."""
        pass

    @abstractmethod
    def feed(self):
        """Покормить питомца."""
        pass

    @abstractmethod
    def play(self):
        """Поиграть с питомцем."""
        pass

    def sleep(self):
        if self.state == "dead":
            return False, "Мертвый питомец не может спать."
        if self.state == "sleeping":
            self.state = "awake"
            self.add_history("wake", "Питомец проснулся.")
            return True, f"{self.name} проснулся!"
        else:
            self.state = "sleeping"
            self.add_history("sleep", "Питомец уложен спать.")
            return True, f"{self.name} теперь спит."

    def heal(self, inventory):
        if self.state == "dead":
            return False, "Нельзя вылечить мертвого питомца."
        if self.health >= 100:
            return False, f"{self.name} полностью здоров!"
        if inventory.get("medkits", 0) <= 0:
            return False, "В инвентаре нет аптечек!"

        inventory["medkits"] -= 1
        self.health += 30
        if self.state == "sick" and self.health > 40:
            self.state = "awake"
        self.add_history("healed", "Использована аптечка, здоровье +30.")
        return True, f"{self.name} подлечен! Текущее здоровье: {self.health}. Осталось аптечек: {inventory['medkits']}."

    def to_dict(self):
        return {
            "name": self.name,
            "species": self.species,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "stats": {
                "hunger": self.hunger,
                "energy": self.energy,
                "health": self.health,
                "mood": self.mood
            },
            "state": self.state,
            "history": self.history
        }


# --- Подклассы (Наследование + Полиморфизм) ---

class Dragon(Pet):
    """Дракон: голод растет быстро, энергопотери медленные. 'Дыхание огнем' сильно поднимает настроение."""

    def update_over_time(self, hours: float):
        if self.state == "dead": return
        self.hunger += int(10 * hours)
        self.energy -= int(2 * hours)
        self.mood -= int(3 * hours)

        if self.hunger > 80:
            self.health -= int(5 * hours)
            if self.state != "sleeping": self.state = "sick"
        if self.health <= 0:
            self.state = "dead"
            self.add_history("died", "Дракон погиб от истощения.")

    def feed(self):
        if self.state == "sleeping": return False, "Дракон спит, его нельзя кормить!"
        if self.state == "dead": return False, "Питомец мертв."
        self.hunger -= 25
        self.mood += 5
        self.add_history("fed", "Покормили дракона, голод -25.")
        return True, f"Вы покормили дракона {self.name}! Голод: {self.hunger}."

    def play(self):
        if self.state == "sleeping": return False, "Дракон спит!"
        if self.state == "dead": return False, "Питомец мертв."
        if self.energy < 15: return False, "Слишком мало энергии для игры!"
        self.energy -= 15
        self.hunger += 10
        self.mood += 25  # Дракон получает много радости от игр
        self.add_history("played", "Дракон подышал огнем во время игры (+25 к настроению).")
        return True, f"Вы сыграли с {self.name}! Дракон подышал огнем! Настроение: {self.mood}."


class Robot(Pet):
    """Робо-пёс: не спит, а заряжается. Не болеет от голода, но ломается при нуле энергии."""

    def update_over_time(self, hours: float):
        if self.state == "dead": return
        self.energy -= int(8 * hours)
        self.hunger += int(3 * hours)

        if self.energy <= 0:
            self.health = 0
            self.state = "dead"
            self.add_history("died", "Батарея полностью разрядилась. Робо-пёс сломался.")

    def feed(self):
        if self.state == "dead": return False, "Робо-пёс сломан."
        self.hunger -= 30
        self.add_history("fed", "Смазаны шестеренки, 'голод' -30.")
        return True, f"Вы провели ТО {self.name}. Износ снижен."

    def play(self):
        if self.state == "dead": return False, "Робо-пёс сломан."
        if self.energy < 20: return False, "Низкий заряд батареи!"
        self.energy -= 20
        self.mood += 15
        self.add_history("played", "Игры с роботом, энергию -20, настроение +15.")
        return True, f"{self.name} выполнил трюки! Настроение: {self.mood}."

    def sleep(self):
        if self.state == "dead": return False, "Робо-пёс сломан."
        if self.state == "sleeping":
            self.state = "awake"
            self.add_history("wake", "Зарядка завершена.")
            return True, f"{self.name} снят с зарядки!"
        else:
            self.state = "sleeping"
            self.add_history("sleep", "Подключен к сети для зарядки.")
            return True, f"{self.name} подключен к зарядной станции."


class Cat(Pet):
    """Кот: голод растет медленно, но настроение падает быстро. Отлично восстанавливается во сне."""

    def update_over_time(self, hours: float):
        if self.state == "dead": return
        self.hunger += int(3 * hours)
        self.mood -= int(8 * hours)

        if self.state == "sleeping":
            self.energy += int(15 * hours)
            self.health += int(5 * hours)
        else:
            self.energy -= int(5 * hours)

        if self.hunger > 70 or self.mood < 10:
            self.health -= int(4 * hours)
            if self.state != "sleeping": self.state = "sick"
        if self.health <= 0:
            self.state = "dead"
            self.add_history("died", "Кот погиб.")

    def feed(self):
        if self.state == "sleeping": return False, "Кот спит, не будите его!"
        if self.state == "dead": return False, "Питомец мертв."
        self.hunger -= 20
        self.mood += 10
        self.add_history("fed", "Покормили кота лакомством.")
        return True, f"Вы покормили {self.name}. Голод: {self.hunger}."

    def play(self):
        if self.state == "sleeping": return False, "Кот спит!"
        if self.state == "dead": return False, "Питомец мертв."
        if self.energy < 10: return False, "Кот слишком устал!"
        self.energy -= 10
        self.mood += 20
        self.hunger += 5
        self.add_history("played", "Поиграли с котиком фантиком.")
        return True, f"Вы побегали с {self.name}! Настроение: {self.mood}."


# Фабричный метод для создания экземпляров питомцев
def create_pet_instance(data: dict) -> Pet:
    species = data.get("species")
    mapping = {"dragon": Dragon, "robot": Robot, "cat": Cat}
    cls = mapping.get(species)
    if not cls:
        raise ValueError(f"Неизвестный вид питомца: {species}")
    return cls(
        name=data["name"],
        species=species,
        created_at=data.get("created_at"),
        last_updated=data.get("last_updated"),
        stats=data.get("stats"),
        state=data.get("state", "awake"),
        history=data.get("history", [])
    )


# ==========================================
# 2. хранилище данных (STORAGE / REPOSITORY)
# ==========================================
class Storage:
    def __init__(self, filepath="data/pets.json"):
        self.filepath = filepath

    def load(self):
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            empty_data = {"pets": [], "resources": {"medkits": 2}}
            self.save(empty_data)
            return empty_data

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print_error(f"Поврежден файл базы данных {self.filepath}: {e}")
            sys.exit(1)

    def save(self, data):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


# ==========================================
# 3. сервис менеджмента и течения времени
# ==========================================
class PetService:
    def __init__(self, storage: Storage):
        self.storage = storage

    def _load_all(self):
        raw = self.storage.load()
        pets = [create_pet_instance(p) for p in raw.get("pets", [])]
        resources = raw.get("resources", {"medkits": 2})

        # Автоматический симуляционный "тик" времени при каждом запуске
        now = datetime.now()
        for pet in pets:
            last_dt = datetime.fromisoformat(pet.last_updated)
            hours_passed = (now - last_dt).total_seconds() / 3600.0
            if hours_passed > 0.01:
                pet.update_over_time(hours_passed)
                pet.last_updated = now.isoformat(timespec='seconds')

        return pets, resources

    def _save_all(self, pets, resources):
        data = {
            "pets": [p.to_dict() for p in pets],
            "resources": resources
        }
        self.storage.save(data)

    def add_pet(self, name: str, species: str):
        pets, resources = self._load_all()
        if any(p.name.lower() == name.lower() for p in pets):
            print_error(f"Питомец с именем '{name}' уже существует!")
            return

        if species not in ["dragon", "robot", "cat"]:
            print_error("Неверный вид! Допустимые виды: dragon, robot, cat")
            return

        new_pet_data = {"name": name, "species": species}
        new_pet = create_pet_instance(new_pet_data)
        new_pet.add_history("created", f"Питомец {name} создан.")
        pets.append(new_pet)

        self._save_all(pets, resources)
        print_success(f"Питомец {name} ({species}) успешно добавлен!")

    def list_pets(self):
        pets, _ = self._load_all()
        if not pets:
            print_info("У вас пока нет питомцев.")
            return

        print(f"\n{Colors.BOLD}=== Список ваших питомцев ==={Colors.RESET}")
        for p in pets:
            created_dt = datetime.fromisoformat(p.created_at)
            age_days = (datetime.now() - created_dt).days
            status_color = Colors.GREEN if p.state == "awake" else Colors.YELLOW if p.state == "sleeping" else Colors.RED
            print(
                f"• {Colors.BOLD}{p.name}{Colors.RESET} ({p.species}) | Возраст: {age_days} дн. | Статус: {status_color}{p.state}{Colors.RESET}")
        print()

    def get_status(self, name: str):
        pets, _ = self._load_all()
        pet = next((p for p in pets if p.name.lower() == name.lower()), None)
        if not pet:
            print_error(f"Питомец '{name}' не найден.")
            return

        print(f"\n{Colors.BOLD}--- Подробный статус: {pet.name} ({pet.species}) ---{Colors.RESET}")
        print(f"Состояние: {pet.state}")
        print(f"Голод:      [{'=' * (pet.hunger // 10):<10}] {pet.hunger}/100")
        print(f"Энергия:    [{'=' * (pet.energy // 10):<10}] {pet.energy}/100")
        print(f"Здоровье:   [{'=' * (pet.health // 10):<10}] {pet.health}/100")
        print(f"Настроение: [{'=' * (pet.mood // 10):<10}] {pet.mood}/100\n")

    def interact(self, name: str, action: str):
        pets, resources = self._load_all()
        pet = next((p for p in pets if p.name.lower() == name.lower()), None)
        if not pet:
            print_error(f"Питомец '{name}' не найден.")
            return

        if action == "feed":
            ok, msg = pet.feed()
        elif action == "play":
            ok, msg = pet.play()
        elif action == "sleep":
            ok, msg = pet.sleep()
        elif action == "heal":
            ok, msg = pet.heal(resources)
        else:
            print_error("Неизвестное действие!")
            return

        if ok:
            print_success(msg)
            self._save_all(pets, resources)
        else:
            print_warning(msg)

    def release_pet(self, name: str):
        pets, resources = self._load_all()
        pet = next((p for p in pets if p.name.lower() == name.lower()), None)
        if not pet:
            print_error(f"Питомец '{name}' не найден.")
            return

        confirm = input(f"Вы уверены, что хотите отпустить питомца {name}? (y/n): ")
        if confirm.lower() == 'y':
            pets = [p for p in pets if p.name.lower() != name.lower()]
            self._save_all(pets, resources)
            print_success(f"Питомец {name} был отпущен на волю.")

    def show_history(self, name: str, limit: int = 5):
        pets, _ = self._load_all()
        pet = next((p for p in pets if p.name.lower() == name.lower()), None)
        if not pet:
            print_error(f"Питомец '{name}' не найден.")
            return

        print(f"\n{Colors.BOLD}История событий {pet.name} (последние {limit}):{Colors.RESET}")
        for entry in pet.history[-limit:]:
            print(f"[{entry['timestamp']}] {entry['event']}: {entry['details']}")
        print()

    def stats_export(self):
        """Дополнительный функционал: экспорт и вывод общей статистики по всем питомцам."""
        pets, _ = self._load_all()
        if not pets:
            print_info("Нет данных для расчета статистики.")
            return

        oldest = min(pets, key=lambda p: datetime.fromisoformat(p.created_at))
        avg_health = sum(p.health for p in pets) / len(pets)

        print(f"\n{Colors.BOLD}===  Общая статистика Терравариума ==={Colors.RESET}")
        print(f"Всего питомцев: {len(pets)}")
        print(f"Самый старый питомец: {Colors.CYAN}{oldest.name}{Colors.RESET} (создан {oldest.created_at[:10]})")
        print(f"Среднее здоровье: {Colors.GREEN}{avg_health:.1f}/100{Colors.RESET}\n")


# ==========================================
# 4. CLI интерфейси обработка аргументов
# ==========================================
def main():
    storage = Storage("data/pets.json")
    service = PetService(storage)

    parser = argparse.ArgumentParser(description="Терравариум — консольный менеджер виртуальных питомцев.")
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # add-pet
    add_parser = subparsers.add_parser("add-pet", help="Завести питомца")
    add_parser.add_argument("--name", required=True, help="Имя питомца")
    add_parser.add_argument("--species", required=True, choices=["dragon", "robot", "cat"], help="Вид питомца")

    # list
    subparsers.add_parser("list", help="Список питомцев")

    # status
    status_parser = subparsers.add_parser("status", help="Статус питомца")
    status_parser.add_argument("--name", required=True, help="Имя питомца")

    # feed, play, sleep, heal
    for action in ["feed", "play", "sleep", "heal"]:
        act_parser = subparsers.add_parser(action, help=f"Выполнить действие {action}")
        act_parser.add_argument("--name", required=True, help="Имя питомца")

    # release
    rel_parser = subparsers.add_parser("release", help="Отпустить питомца")
    rel_parser.add_argument("--name", required=True, help="Имя питомца")

    # history
    hist_parser = subparsers.add_parser("history", help="История событий")
    hist_parser.add_argument("--name", required=True, help="Имя питомца")

    # stats (доп. баллы)
    subparsers.add_parser("stats", help="Вывести общую статистику")

    args = parser.parse_args()

    try:
        if args.command == "add-pet":
            service.add_pet(args.name, args.species)
        elif args.command == "list":
            service.list_pets()
        elif args.command == "status":
            service.get_status(args.name)
        elif args.command in ["feed", "play", "sleep", "heal"]:
            service.interact(args.name, args.command)
        elif args.command == "release":
            service.release_pet(args.name)
        elif args.command == "history":
            service.show_history(args.name)
        elif args.command == "stats":
            service.stats_export()
        else:
            parser.print_help()
    except Exception as e:
        print_error(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()