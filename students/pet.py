from __future__ import annotations

from dataclasses import dataclass

from .config import (
    HUNGER_HEALTH_PENALTY,
    HUNGER_MOOD_PENALTY,
    MOOD_HEALTH_PENALTY,
    START_ENERGY,
    START_HEALTH,
    START_MOOD,
    START_SATIETY,
    STAT_MAX,
    STAT_MIN,
    TARGET_AGE,
)
from .species import SPECIES, Species, SpeciesProfile


def clamp(value: int) -> int:
    return max(STAT_MIN, min(STAT_MAX, value))


@dataclass
class Pet:

    name: str
    species: Species
    satiety: int = START_SATIETY
    mood: int = START_MOOD
    energy: int = START_ENERGY
    health: int = START_HEALTH
    age: int = 0
    alive: bool = True

    affection_streak: int = 0

    @property
    def profile(self) -> SpeciesProfile:
        return SPECIES[self.species]

    @property
    def display_species(self) -> str:
        return self.profile.display_name

    @property
    def is_adult(self) -> bool:
        return self.age >= TARGET_AGE

    @property
    def death_message(self) -> str:
        return self.profile.death_message

    def die_if_needed(self) -> list[str]:
        if self.alive and self.health <= 0:
            self.alive = False
            return [self.death_message]
        return []

    def tick(self) -> list[str]:
        if not self.alive:
            return []

        notes: list[str] = []
        profile = self.profile

        self.satiety = clamp(self.satiety + profile.satiety_per_turn)
        self.energy = clamp(self.energy + profile.energy_per_turn)
        self.mood = clamp(self.mood + profile.mood_per_turn)

        if self.satiety <= 0:
            if profile.hunger_hurts_health:
                self.health = clamp(self.health - HUNGER_HEALTH_PENALTY)
                notes.append(f"{self.name} голодает — здоровье падает.")
            else:
                self.mood = clamp(self.mood - HUNGER_MOOD_PENALTY)
                notes.append(f"{self.name} голоден, но для робота это не опасно.")

        if self.energy <= 0:
            self.health = clamp(self.health - profile.zero_energy_health_loss)
            if profile.species is Species.ROBOT:
                notes.append(f"{self.name} разрядился — кажется, он ломается.")
            else:
                notes.append(f"{self.name} совсем без сил — здоровье тает.")

        if self.mood <= 0:
            self.health = clamp(self.health - MOOD_HEALTH_PENALTY)
            notes.append(f"{self.name} совсем приуныл — здоровье тает.")

        self.age += 1
        notes.extend(self.die_if_needed())

        return notes