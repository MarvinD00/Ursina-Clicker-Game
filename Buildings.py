import enum
from typing import Dict, Any
from Ressource import Ressource_type

class Building_type(enum.Enum):
    WOODCUTTER = 1
    STONE_MINE = 2
    GOLD_MINE = 3

class BuildingPrototype:
    """Template für Building-Eigenschaften"""
    def __init__(self, name: str, base_cost: Dict[Ressource_type, int], 
                 cost_multiplier: float, production: Dict[Ressource_type, int],
                 production_multiplier: float = 1.2, tick_interval: float = 1.0):
        self.name = name
        self.base_cost = base_cost  # Grundkosten für Level 1
        self.cost_multiplier = cost_multiplier  # Kostensteigerung pro Level
        self.production = production  # Produktion pro Tick
        self.production_multiplier = production_multiplier  # Produktionssteigerung pro Level
        self.tick_interval = tick_interval  # Sekunden zwischen Produktion

# Building Prototypes/Templates
BUILDING_PROTOTYPES: Dict[Building_type, BuildingPrototype] = {
    Building_type.WOODCUTTER: BuildingPrototype(
        name="Holzfäller",
        base_cost={Ressource_type.GOLD: 10},
        cost_multiplier=1.5,
        production={Ressource_type.WOOD: 1},
        production_multiplier=1.2,
        tick_interval=1.0
    ),
    
    Building_type.STONE_MINE: BuildingPrototype(
        name="Steinmine",
        base_cost={Ressource_type.GOLD: 25, Ressource_type.WOOD: 10},
        cost_multiplier=1.6,
        production={Ressource_type.STONE: 1},
        production_multiplier=1.25,
        tick_interval=1.0
    ),
    
    Building_type.GOLD_MINE: BuildingPrototype(
        name="Goldmine",
        base_cost={Ressource_type.GOLD: 50, Ressource_type.WOOD: 20, Ressource_type.STONE: 15},
        cost_multiplier=1.8,
        production={Ressource_type.GOLD: 2},
        production_multiplier=1.3,
        tick_interval=1.0
    )
}

class Building:
    def __init__(self, building_type: Building_type, level: int = 1):
        self.building_type = building_type
        self.level = level
        self.prototype = BUILDING_PROTOTYPES[building_type]
        
    def get_cost(self) -> Dict[Ressource_type, int]:
        """Calculates the cost for the next level"""
        cost = {}
        for resource_type, base_amount in self.prototype.base_cost.items():
            cost[resource_type] = int(base_amount * (self.prototype.cost_multiplier ** (self.level - 1)))
        return cost
    
    def get_production(self) -> Dict[Ressource_type, int]:
        """Calculates the current production per tick"""
        production = {}
        for resource_type, base_amount in self.prototype.production.items():
            production[resource_type] = int(base_amount * (self.prototype.production_multiplier ** (self.level - 1)))
        return production
    
    def get_upgrade_cost(self) -> Dict[Ressource_type, int]:
        """Calculates the cost for upgrading to the next level"""
        cost = {}
        for resource_type, base_amount in self.prototype.base_cost.items():
            cost[resource_type] = int(base_amount * (self.prototype.cost_multiplier ** self.level))
        return cost
    
    def upgrade(self):
        """Increases the level by 1"""
        self.level += 1
    
    def __str__(self):
        return f"{self.prototype.name} (Level {self.level})"