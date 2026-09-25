from abc import ABC, abstractmethod
from datetime import datetime


class PetIsDeadError(Exception):
    """Питомец мёртв — с ним нельзя взаимодействовать."""
    pass


class PetIsSleepingError(Exception):
    """Питомец спит — действие запрещено."""
    pass


class Pet(ABC):
    HUNGER_RATE = 1.0
    ENERGY_SLEEP_RATE = 3.0
    MOOD_DECAY = 1.0
    HEALTH_SLEEP_GAIN = 1.0
    SICK_HUNGER = 80
    SICK_MOOD = 15
    SICK_ENERGY = 10

    SPECIES = "unknown"

    def __init__(self, name, created_at=None, last_updated=None,
                 hunger=30, energy=80, health=100, mood=80,
                 state="awake", history=None):
        self.name = name
        self.created_at = created_at or datetime.now().isoformat()
        self.last_updated = last_updated or self.created_at
        self._hunger = hunger
        self._energy = energy
        self._health = health
        self._mood = mood
        self.state = state
        self.history = history or []

    @property
    def hunger(self):
        return self._hunger

    @hunger.setter
    def hunger(self, value):
        self._hunger = max(0, min(100, value))

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        self._energy = max(0, min(100, value))

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = max(0, min(100, value))

    @property
    def mood(self):
        return self._mood

    @mood.setter
    def mood(self, value):
        self._mood = max(0, min(100, value))

    @abstractmethod
    def make_sound(self):
        pass

    @abstractmethod
    def special_ability(self):
        pass

    def add_history(self, event, details=""):
        self.history.append({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "event": event,
            "details": details,
        })

    def is_alive(self):
        return self.state != "dead"

    def _check_alive(self):
        if not self.is_alive():
            raise PetIsDeadError(f"{self.name} мёртв. Можно только смотреть историю.")

    def is_sick(self):
        return self._hunger >= self.SICK_HUNGER or \
               self._mood <= self.SICK_MOOD or \
               self._energy <= self.SICK_ENERGY

    def status_text(self):
        if self.state == "dead":
            return "мёртв"
        if self.is_sick():
            return "болен"
        if self.state == "asleep":
            return "спит"
        return "жив"

    def feed(self):
        self._check_alive()
        if self.state == "asleep":
            raise PetIsSleepingError(f"{self.name} спит — нельзя кормить.")
        self.hunger -= 20
        self.mood += 5
        self.add_history("fed", "Голод снижен на 20")
        return f"{self.make_sound()} {self.name} покормлен."

    def play(self):
        self._check_alive()
        if self.state == "asleep":
            raise PetIsSleepingError(f"{self.name} спит — нельзя играть.")
        if self._energy < 15:
            return f"{self.name} слишком устал для игры."
        self.mood += 15
        self.energy -= 15
        self.hunger += 10
        self.add_history("played", "Настроение +15, энергия -15")
        return f"{self.make_sound()} {self.name} поиграл и повеселел."

    def sleep(self):
        self._check_alive()
        if self.state == "asleep":
            self.state = "awake"
            self.add_history("woke_up", "Питомец проснулся")
            return f"{self.name} проснулся."
        self.state = "asleep"
        self.add_history("slept", "Питомец заснул")
        return f"{self.name} заснул."

    def heal(self, inventory):
        self._check_alive()
        if not self.is_sick():
            return f"{self.name} не болен — лечение не нужно."
        if not inventory.use_medkit():
            return "Аптечек нет!"
        self.health += 30
        self.mood += 10
        self.add_history("healed", "Здоровье +30, использована аптечка")
        return f"{self.name} вылечен."

    def tick(self):
        if not self.is_alive():
            return
        now = datetime.now()
        last = datetime.fromisoformat(self.last_updated)
        hours = (now - last).total_seconds() / 3600
        if hours <= 0:
            return

        self.hunger += hours * self.HUNGER_RATE * 2
        self.mood -= hours * self.MOOD_DECAY

        if self.state == "asleep":
            self.energy += hours * self.ENERGY_SLEEP_RATE * 3
            self.health += hours * self.HEALTH_SLEEP_GAIN
        else:
            self.energy -= hours * 2

        if self.is_sick():
            self.health -= hours * 2
            self.add_history("sick", "Питомец заболел")

        if self._health <= 0:
            self.state = "dead"
            self.add_history("died", "Питомец умер")

        self.last_updated = now.isoformat(timespec="seconds")

    def to_dict(self):
        return {
            "name": self.name,
            "species": self.SPECIES,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "stats": {
                "hunger": int(self._hunger),
                "energy": int(self._energy),
                "health": int(self._health),
                "mood": int(self._mood),
            },
            "state": self.state,
            "history": self.history,
        }


class Dragon(Pet):
    SPECIES = "dragon"
    HUNGER_RATE = 1.5
    ENERGY_SLEEP_RATE = 2.0

    def make_sound(self):
        return "Р-р-р!"

    def special_ability(self):
        self.mood += 25
        self.add_history("ability", "Дыхание огнём: настроение +25")
        return f"{self.name} дышит огнём! Настроение +25."


class RobotDog(Pet):
    SPECIES = "robot"
    HUNGER_RATE = 0.5
    ENERGY_SLEEP_RATE = 5.0
    HEALTH_SLEEP_GAIN = 0.0
    SICK_HUNGER = 200

    def is_sick(self):
        return self._energy <= 0

    def make_sound(self):
        return "Бип-буп!"

    def special_ability(self):
        self.energy += 20
        self.add_history("ability", "Подзарядка: энергия +20")
        return f"{self.name} подзарядился. Энергия +20."

    def tick(self):
        super().tick()
        if self._energy <= 0 and self.is_alive():
            self.state = "dead"
            self.add_history("died", "Робот сломался")


class Cat(Pet):
    SPECIES = "cat"
    HUNGER_RATE = 0.7
    MOOD_DECAY = 2.0
    HEALTH_SLEEP_GAIN = 3.0

    def make_sound(self):
        return "Мяу!"

    def special_ability(self):
        self.mood += 20
        self.energy += 10
        self.add_history("ability", "Мурчание: настроение +20, энергия +10")
        return f"{self.name} мурчит. Настроение +20, энергия +10."


SPECIES_MAP = {
    "dragon": Dragon,
    "robot": RobotDog,
    "cat": Cat,
}


def create_pet(species, name):
    cls = SPECIES_MAP.get(species)
    if not cls:
        raise ValueError(f"Неизвестный вид: {species}. Доступно: {list(SPECIES_MAP)}")
    return cls(name=name)