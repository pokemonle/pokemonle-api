

class PokemonDataStats:
    def __init__(self, hp: int, attack: int, defense: int, special_attack: int, special_defense: int, speed: int):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed

    def total(self) -> int:
        return self.hp + self.attack + self.defense + self.special_attack + self.special_defense + self.speed

    def __repr__(self):
        return f"PokemonDataStats(hp={self.hp}, attack={self.attack}, defense={self.defense}, special_attack={self.special_attack}, special_defense={self.special_defense}, speed={self.speed})"

    def json(self) -> dict:
        return {
            "hp": self.hp,
            "attack": self.attack,
            "defense": self.defense,
            "special_attack": self.special_attack,
            "special_defense": self.special_defense,
            "speed": self.speed,
        }
