from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .config import (
    FEED_MOOD_GAIN,
    FEED_SATIETY_GAIN,
    FIRE_BREATH_MOOD_GAIN,
    HEAL_HEALTH_GAIN,
    HEAL_MOOD_COST,
    PAT_MOOD_GAINS,
    PLAY_ENERGY_COST,
    PLAY_MIN_ENERGY,
    PLAY_MOOD_GAIN,
    PLAY_SATIETY_COST,
    PLAY_TIRED_HEALTH_LOSS,
    PLAY_TIRED_MOOD_GAIN,
    STAT_MAX,
)
from .pet import Pet, clamp
from .species import Species


@dataclass(frozen=True)
class Action:

    key: str
    label: str
    run: Callable[[Pet], list[str]]


def feed(pet: Pet) -> list[str]:

    if pet.satiety >= STAT_MAX:
        return [f"{pet.name} уже сыт — еда пропала зря, ход потерян."]
    pet.satiety = clamp(pet.satiety + FEED_SATIETY_GAIN)
    pet.mood = clamp(pet.mood + FEED_MOOD_GAIN)
    return [f"{pet.name} поел."]


def play(pet: Pet) -> list[str]:
    if pet.energy < PLAY_MIN_ENERGY:
        pet.mood = clamp(pet.mood + PLAY_TIRED_MOOD_GAIN)
        pet.health = clamp(pet.health - PLAY_TIRED_HEALTH_LOSS)
        return [f"{pet.name} слишком устал — игра вышла ему во вред."]
    pet.mood = clamp(pet.mood + PLAY_MOOD_GAIN)
    pet.energy = clamp(pet.energy - PLAY_ENERGY_COST)
    pet.satiety = clamp(pet.satiety - PLAY_SATIETY_COST)
    return [f"{pet.name} наигрался и повеселел."]


def rest(pet: Pet) -> list[str]:
    profile = pet.profile
    pet.energy = clamp(pet.energy + profile.rest_energy_gain)
    if profile.rest_health_gain:
        pet.health = clamp(pet.health + profile.rest_health_gain)
    if pet.species is Species.ROBOT:
        return [f"{pet.name} зарядился."]
    return [f"{pet.name} выспался."]


def fire_breath(pet: Pet) -> list[str]:
    pet.mood = clamp(pet.mood + FIRE_BREATH_MOOD_GAIN)
    return [f"{pet.name} дохнул огнём — настроение взлетело!"]


def heal(pet: Pet) -> list[str]:
    pet.health = clamp(pet.health + HEAL_HEALTH_GAIN)
    pet.mood = clamp(pet.mood - HEAL_MOOD_COST)
    return [f"{pet.name} полечился, но лекарство невкусное."]


def pat(pet: Pet) -> list[str]:
    gain = PAT_MOOD_GAINS[min(pet.affection_streak, len(PAT_MOOD_GAINS) - 1)]
    pet.affection_streak += 1
    pet.mood = clamp(pet.mood + gain)
    if gain == 0:
        return [f"{pet.name} уже привык к ласке — эффекта нет."]
    return [f"{pet.name} рад вниманию."]


def skip(pet: Pet) -> list[str]:
    return [f"{pet.name} просто переждал ход."]


FEED = Action("feed", "Покормить", feed)
PLAY = Action("play", "Поиграть", play)
HEAL = Action("heal", "Полечить", heal)
PAT = Action("pat", "Погладить", pat)
FIRE_BREATH = Action("fire_breath", "Дыхание огнём", fire_breath)
SKIP = Action("skip", "Пропустить ход", skip)


def actions_for(pet: Pet) -> list[Action]:
    actions = [
        FEED,
        PLAY,
        Action("rest", pet.profile.rest_action_name, rest),
        HEAL,
        PAT,
    ]
    if pet.profile.has_fire_breath:
        actions.append(FIRE_BREATH)
    actions.append(SKIP)
    return actions


def perform(pet: Pet, action: Action) -> list[str]:
    if action.key != PAT.key:
        pet.affection_streak = 0

    notes = list(action.run(pet))
    notes.extend(pet.die_if_needed())
    if pet.alive:
        notes.extend(pet.tick())
    return notes