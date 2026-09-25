# JP621 Final Project - Dungeon

A text-based dungeon adventure game made in Python.

## How to Run

Start a new game:

```text
python main.py --new-game
```

Load a saved game:

```text
python main.py --load data/save1.json
```

## Commands

* `look` — Look around
* `go <direction>` — Move
* `take <item>` — Pick up an item
* `use <item>` — Use an item
* `inventory` — Show inventory
* `talk` — Talk to an NPC
* `talk <person>` — Talk to a specific NPC
* `attack <enemy>` — Fight an enemy
* `save` — Save the game
* `load` — Load the game
* `help` — Show commands
* `quit` — Exit the game

## World Map

```text
Entrance
/      \
Hall    Library
|  \       |
|   Crypt  |
|     |    |
Armory  Treasury
    \    /
   Throne Room
```

## Game Features

* 7 rooms
* Multiple paths
* 6+ items
* Potions, weapons and keys
* Goblin and Skeleton enemies
* NPC dialogue
* Turn-based combat
* Inventory system
* Locked doors
* Save and load system
* Win condition

## Project Structure

```text
main.py
models/
    character.py
    item.py
    room.py
engine/
    combat.py
    save_manager.py
    world_loader.py
data/
    world.json
    save1.json
```

## Goal

Explore the dungeon, collect items, defeat enemies, unlock doors and reach the throne room.
