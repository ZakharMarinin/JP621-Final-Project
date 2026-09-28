from __future__ import annotations

from collections.abc import Sequence

from .config import TARGET_AGE
from .pet import Pet

BAR_WIDTH = 20
FILLED = "#"
EMPTY = "-"


def bar(value: int, width: int = BAR_WIDTH) -> str:
    value = max(0, min(100, value))
    filled = round(value / 100 * width)
    return f"[{FILLED * filled}{EMPTY * (width - filled)}] {value:>3}"


def render_stats(pet: Pet) -> str:
    state = "жив" if pet.alive else "финал"
    lines = [
        f"{pet.name} — {pet.display_species}    возраст {pet.age}/{TARGET_AGE}    ({state})",
        f"  Сытость     {bar(pet.satiety)}",
        f"  Настроение  {bar(pet.mood)}",
        f"  Энергия     {bar(pet.energy)}",
        f"  Здоровье    {bar(pet.health)}",
    ]
    return "\n".join(lines)


def render_menu(labels: Sequence[str]) -> str:
    lines = ["Что делаем?"]
    for number, label in enumerate(labels, start=1):
        lines.append(f"  {number}. {label}")
    return "\n".join(lines)