from models.pet import create_pet, PetIsDeadError, PetIsSleepingError


class PetNotFoundError(Exception):
    pass


class PetService:
    def __init__(self, repository):
        self.repo = repository

    def _all(self):
        return self.repo.load_pets()

    def _find(self, name):
        for p in self._all():
            if p.name.lower() == name.lower():
                return p
        raise PetNotFoundError(f"Питомец '{name}' не найден.")

    def _tick_all(self):
        pets = self._all()
        for p in pets:
            p.tick()
        inv = self.repo.load_inventory()
        self.repo.save_pets(pets, inv)
        return pets

    def add_pet(self, name, species):
        pets = self._tick_all()
        if any(p.name.lower() == name.lower() for p in pets):
            raise ValueError(f"Имя '{name}' уже занято.")
        pet = create_pet(species, name)
        pet.add_history("created", f"Создан питомец вида {species}")
        pets.append(pet)
        inv = self.repo.load_inventory()
        self.repo.save_pets(pets, inv)
        return pet

    def list_pets(self):
        return self._tick_all()

    def status(self, name):
        self._tick_all()
        return self._find(name)

    def feed(self, name):
        self._tick_all()
        pet = self._find(name)
        msg = pet.feed()
        self._save(pet)
        return msg

    def play(self, name):
        self._tick_all()
        pet = self._find(name)
        msg = pet.play()
        self._save(pet)
        return msg

    def sleep(self, name):
        self._tick_all()
        pet = self._find(name)
        msg = pet.sleep()
        self._save(pet)
        return msg

    def heal(self, name):
        self._tick_all()
        pet = self._find(name)
        inv = self.repo.load_inventory()
        msg = pet.heal(inv)
        pets = self._all()
        for i, p in enumerate(pets):
            if p.name.lower() == name.lower():
                pets[i] = pet
                break
        self.repo.save_pets(pets, inv)
        return msg

    def ability(self, name):
        self._tick_all()
        pet = self._find(name)
        msg = pet.special_ability()
        self._save(pet)
        return msg

    def release(self, name):
        self._tick_all()
        pet = self._find(name)
        pets = [p for p in self._all() if p.name.lower() != name.lower()]
        inv = self.repo.load_inventory()
        self.repo.save_pets(pets, inv)
        return f"{pet.name} отпущен."

    def history(self, name, n=10):
        self._tick_all()
        pet = self._find(name)
        return pet.history[-n:]

    def _save(self, updated_pet):
        pets = self._all()
        for i, p in enumerate(pets):
            if p.name.lower() == updated_pet.name.lower():
                pets[i] = updated_pet
                break
        inv = self.repo.load_inventory()
        self.repo.save_pets(pets, inv)