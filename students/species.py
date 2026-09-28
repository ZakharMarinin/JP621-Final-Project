from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Species(str, Enum):

    DRAGON = "dragon"
    ROBOT = "robot"
    CAT = "cat"


@dataclass(frozen=True)
class SpeciesProfile:

    species: Species
    display_name: str
    tagline: str

    satiety_per_turn: int
    energy_per_turn: int
    mood_per_turn: int

    rest_action_name: str
    rest_energy_gain: int
    rest_health_gain: int

    hunger_hurts_health: bool
    zero_energy_health_loss: int

    has_fire_breath: bool

    death_message: str


DRAGON = SpeciesProfile(
    species=Species.DRAGON,
    display_name="Дракон",
    tagline="голодает быстро, зато энергия почти не тратится и есть дыхание огнём",
    satiety_per_turn=-3,
    energy_per_turn=-1,
    mood_per_turn=-1,
    rest_action_name="Уложить спать",
    rest_energy_gain=20,
    rest_health_gain=2,
    hunger_hurts_health=True,
    zero_energy_health_loss=5,
    has_fire_breath=True,
    death_message="Питомец погиб",
)

ROBOT = SpeciesProfile(
    species=Species.ROBOT,
    display_name="Робо-пёс",
    tagline="не спит, а заряжается; голод ему не страшен, но без энергии он ломается",
    satiety_per_turn=-2,
    energy_per_turn=-2,
    mood_per_turn=-1,
    rest_action_name="Зарядиться",
    rest_energy_gain=20,
    rest_health_gain=0,
    hunger_hurts_health=False,
    zero_energy_health_loss=8,
    has_fire_breath=False,
    death_message="Робо-пёс сломался",
)

CAT = SpeciesProfile(
    species=Species.CAT,
    display_name="Кот",
    tagline="голодает медленно, но скучает быстро; зато сон лечит лучше всех",
    satiety_per_turn=-1,
    energy_per_turn=-2,
    mood_per_turn=-2,
    rest_action_name="Уложить спать",
    rest_energy_gain=20,
    rest_health_gain=5,
    hunger_hurts_health=True,
    zero_energy_health_loss=5,
    has_fire_breath=False,
    death_message="Питомец погиб",
)

SPECIES: dict[Species, SpeciesProfile] = {
    Species.DRAGON: DRAGON,
    Species.ROBOT: ROBOT,
    Species.CAT: CAT,
}

SPECIES_ORDER: tuple[Species, ...] = (Species.DRAGON, Species.ROBOT, Species.CAT)