from __future__ import annotations

import json
from pathlib import Path

from .config import SAVE_PATH
from .pet import Pet
from .species import Species

SAVE_VERSION = 1


class SaveError(Exception):
    """Сохранение не удалось прочитать: файл битый, чужой или другого формата."""

def _pet_to_dict(pet: Pet) -> dict[str, object]:

    return {
        "name": pet.name,
        "species": pet.species.value,
        "satiety": pet.satiety,
        "mood": pet.mood,
        "energy": pet.energy,
        "health": pet.health,
        "age": pet.age,
        "alive": pet.alive,
        "affection_streak": pet.affection_streak,
    }


def _pet_from_dict(payload: dict[str, object]) -> Pet:
    try:
        species = Species(payload["species"])
    except KeyError as error:
        raise SaveError(f"в сохранении нет вида питомца (поле {error})") from error
    except ValueError as error:
        raise SaveError(
            f"неизвестный вид питомца: {payload['species']!r}"
        ) from error

    try:
        return Pet(
            name=str(payload["name"]),
            species=species,
            satiety=int(payload["satiety"]),
            mood=int(payload["mood"]),
            energy=int(payload["energy"]),
            health=int(payload["health"]),
            age=int(payload["age"]),
            alive=bool(payload["alive"]),
            affection_streak=int(payload.get("affection_streak", 0)),
        )
    except KeyError as error:
        raise SaveError(f"в сохранении нет поля {error}") from error
    except (TypeError, ValueError) as error:
        raise SaveError(f"испорченное значение в сохранении: {error}") from error


def save_state(pet: Pet, best_age: int, path: Path = SAVE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "version": SAVE_VERSION,
        "best_age": int(best_age),
        "pet": _pet_to_dict(pet),
    }
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    temporary.replace(path)


def load_state(path: Path = SAVE_PATH) -> tuple[Pet | None, int]:

    if not path.exists():
        return None, 0

    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as error:
        raise SaveError(f"не удалось открыть файл: {error}") from error

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as error:
        raise SaveError(f"файл не является корректным JSON ({error})") from error

    if not isinstance(data, dict):
        raise SaveError("ожидался объект JSON, а не список или число")

    version = data.get("version")
    if version != SAVE_VERSION:
        raise SaveError(
            f"версия сохранения {version!r} не поддерживается "
            f"(игра умеет {SAVE_VERSION})"
        )

    pet_payload = data.get("pet")
    if not isinstance(pet_payload, dict):
        raise SaveError("в сохранении нет данных питомца")

    try:
        best_age = int(data.get("best_age", 0))
    except (TypeError, ValueError) as error:
        raise SaveError(f"испорченный рекорд в сохранении: {error}") from error

    return _pet_from_dict(pet_payload), best_age


def clear(path: Path = SAVE_PATH) -> None:
    path.unlink(missing_ok=True)