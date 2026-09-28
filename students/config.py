from __future__ import annotations

from pathlib import Path

# --- Цель игры ---------------------------------------------------------------
# Сколько ходов нужно прожить, чтобы питомец вырос (победа).
TARGET_AGE = 30

# --- Границы статов ----------------------------------------------------------
STAT_MIN = 0
STAT_MAX = 100

# --- Стартовые статы новорождённого питомца ----------------------------------
START_SATIETY = 40
START_MOOD = 40
START_ENERGY = 40
START_HEALTH = 40

# --- Урон, когда стат на нуле ------------------------------------------------
HUNGER_HEALTH_PENALTY = 5
HUNGER_MOOD_PENALTY = 3

# Уныние: если настроение упало до нуля, питомец огорчается.
MOOD_HEALTH_PENALTY = 3

# --- Действия игрока ---------------------------------------------------------
FEED_SATIETY_GAIN = 12
FEED_MOOD_GAIN = 1

# Игра
PLAY_MOOD_GAIN = 16
PLAY_ENERGY_COST = 8
PLAY_SATIETY_COST = 3
PLAY_MIN_ENERGY = 15
PLAY_TIRED_MOOD_GAIN = 4
PLAY_TIRED_HEALTH_LOSS = 3

# Дыхание огнём
FIRE_BREATH_MOOD_GAIN = 18

# Лечение
HEAL_HEALTH_GAIN = 15
HEAL_MOOD_COST = 5

# Ласка: эффект тает, если гладить каждый ход подряд
PAT_MOOD_GAINS = (6, 4, 2, 0)

# --- Хранилище ---------------------------------------------------------------
SAVE_PATH = Path(__file__).resolve().parent.parent / "data" / "save.json"