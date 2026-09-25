class Room:
    def __init__(self, room_id, description, exits, items=None, enemies=None, npcs=None):
        self.room_id = room_id
        self.description = description
        self.exits = exits
        self.items = items or []
        self.enemies = enemies or []
        self.npcs = npcs or []

    def describe(self):
        print()
        print(self.description)

        if self.items:
            print("Items:")
            for item in self.items:
                print(f"- {item.name}")

        if self.enemies:
            print("Enemies:")
            for enemy in self.enemies:
                print(f"- {enemy.name} (HP: {enemy.hp})")

        if self.npcs:
            print("People:")
            for npc in self.npcs:
                print(f"- {npc.name}")

        print("Exits:", ", ".join(self.exits.keys()))