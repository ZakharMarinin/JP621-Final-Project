class Inventory:
    def __init__(self, medkits=3):
        self.medkits = medkits

    def use_medkit(self):
        if self.medkits <= 0:
            return False
        self.medkits -= 1
        return True

    def to_dict(self):
        return {"medkits": self.medkits}

    @classmethod
    def from_dict(cls, data):
        return cls(data.get("medkits", 3))