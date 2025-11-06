import enum

class Ressource_type(enum.Enum):
    GOLD = 1
    STONE = 2
    WOOD = 3
    FOOD = 4
    WATER = 5
    GLASS = 6
    METAL = 7
    PLASTIC = 8
    AIR = 9
    DICE = 10
    PEN = 11
    NOTEBOOK = 12
    FAT_COCONUT = 13
    HUGE_WEINER = 14
    SMALL_WEINER = 15
class Ressource:
    def __init__(self, ressource_type: Ressource_type, amount: int = 0):
        self.ressource_type = ressource_type
        self.amount = amount

    def add(self, amount: int):
        if (amount < 0):
            raise ValueError("Amount to add must be non-negative")
        self.amount += amount
    
    def subtract(self, amount: int):
        if (amount < 0):
            raise ValueError("Amount to subtract must be non-negative")
        if (self.amount - amount < 0):
            raise ValueError("Not enough resources to subtract the requested amount")
        self.amount -= amount

    def get_amount(self) -> int:
        return self.amount
    
    def get_type(self) -> Ressource_type:
        return self.ressource_type
    
    def __str__(self) -> str:
        return f"{self.ressource_type.name}: {self.amount}"
    
