from ursina import *
from Ressource import Ressource, Ressource_type
from typing import Dict
from Buildings import Building, Building_type

'''
Ressources and Counters Initialization
'''
def init_Ressources() -> Dict[Ressource_type, Ressource]:
    Ressources = {}
    for res_type in Ressource_type:
        Ressources[res_type] = Ressource(res_type, 0)
    return Ressources

def init_counters(Ressources: Dict[Ressource_type, Ressource]) -> Dict[str, Text]:
    counters = {}
    for res_type, res in Ressources.items():
        counters[res_type.name.lower()] = Text(text='0' , x=-0.8 + 0.1 * list(Ressource_type).index(res_type) , y=0.45 , z=-1 , scale=1 , origin=(0,0) , background=True)
    return counters

def init_buildings() -> Dict[Building_type, Building]:
    buildings = {}
    for b_type in Building_type:
        buildings[b_type] = Building(b_type, 1)
    return buildings

def buy_building(building_type: Building_type) -> None:
    """Buy/upgrade a building if enough resources are available"""
    building = buildings[building_type]
    upgrade_cost = building.get_upgrade_cost()
    
    # Check if can afford
    can_afford = True
    for res_type, cost in upgrade_cost.items():
        if Ressources[res_type].amount < cost:
            can_afford = False
            break
    
    if can_afford:
        # Pay the costs
        for res_type, cost in upgrade_cost.items():
            Ressources[res_type].amount -= cost
        
        # Upgrade the building
        building.upgrade()
        
        # Update UI 
        update_building_counters(buildings, building_counters, Ressources, building_buttons)
        update_resource_counters(Ressources, counters)
        
        # Update Tooltip with new costs
        btn = building_buttons[building_type]
        btn.tooltip.text = f'<gold>{building.prototype.name}\n<default>Produces {list(building.get_production().values())[0]} {list(building.get_production().keys())[0].name} every {building.prototype.tick_interval} seconds.\nCosts: ' + ', '.join([f'{amt} {res_type.name}' for res_type, amt in building.get_upgrade_cost().items()]) + f'.'

def init_buildings_buttons(buildings: Dict[Building_type, Building]) -> Dict[Building_type, Button]:
    building_buttons = {}
    for i, (b_type, building) in enumerate(buildings.items()):
        x_pos = -0.5 + (i * 0.35)
        y_pos = 0.1
        
        btn = Button(
            text=building.prototype.name, 
            color=color.dark_gray, 
            scale=.15, 
            disabled=True,
            x=x_pos,
            y=y_pos
        )
        btn.tooltip = Tooltip(f'<gold>{building.prototype.name}\n<default>Produces {list(building.get_production().values())[0]} {list(building.get_production().keys())[0].name} every {building.prototype.tick_interval} seconds.\nCosts: ' + ', '.join([f'{amt} {res_type.name}' for res_type, amt in building.get_upgrade_cost().items()]) + f'.')
        
        # Add onClick function
        btn.on_click = lambda b_type=b_type: buy_building(b_type)
        
        building_buttons[b_type] = btn
    return building_buttons

def init_buildings_counters(buildings: Dict[Building_type, Building]) -> Dict[Building_type, Text]:
    building_counters = {}
    for i, (b_type, building) in enumerate(buildings.items()):
        x_pos = -0.5 + (i * 0.35)
        y_pos = -0.05
        
        building_counters[b_type] = Text(
            text=f'Level: {building.level}', 
            x=x_pos, 
            y=y_pos, 
            z=-1, 
            scale=0.8, 
            origin=(0,0), 
            background=True
        )
    return building_counters

def update_building_counters(buildings: Dict[Building_type, Building], building_counters: Dict[Building_type, Text], 
                            resources: Dict[Ressource_type, Ressource], building_buttons: Dict[Building_type, Button]) -> None:
    '''update the building level counters'''
    for b_type, building in buildings.items():
        building_counters[b_type].text = f'Level: {building.level}'

    '''update the building buttons state based on available resources'''
    for b_type, building in buildings.items():
        upgrade_cost = building.get_upgrade_cost()
        can_afford = True
        
        # Check if can afford
        for res_type, cost in upgrade_cost.items():
            if resources[res_type].amount < cost:
                can_afford = False
                break
        
        if can_afford:
            building_buttons[b_type].disabled = False
            building_buttons[b_type].color = color.green
        else:
            building_buttons[b_type].disabled = True
            building_buttons[b_type].color = color.gray

def update_resource_counters(Ressources: Dict[Ressource_type, Ressource], counters: Dict[str, Text]) -> None:
    for res_type, res in Ressources.items():
        counters[res_type.name.lower()].text = str(res.amount)

def calculate_passive_income(resources: Dict[Ressource_type, Ressource], buildings: Dict[Building_type, Building]) -> None:
    """Calculate and add passive income from all buildings"""
    for building in buildings.values():
        production = building.get_production()
        for res_type, amount in production.items():
            resources[res_type].amount += amount

app = Ursina()
window.color = color._20

Ressources = init_Ressources()
counters = init_counters(Ressources)
buildings = init_buildings()
building_buttons = init_buildings_buttons(buildings)
building_counters = init_buildings_counters(buildings)

'''
Gold Button
'''
button_gold = Button(text='+', color=color.azure, scale= .125)

def button_gold_click() -> None:
    Ressources[Ressource_type.GOLD].amount += 1
    counters[Ressource_type.GOLD.name.lower()].text = str(Ressources[Ressource_type.GOLD].amount)

button_gold.on_click = button_gold_click

def tick() -> None:
    calculate_passive_income(Ressources, buildings)
    update_building_counters(buildings, building_counters, Ressources, building_buttons)
    update_resource_counters(Ressources, counters)
    invoke(tick, delay=1)




def update() -> None:
    pass  # Leer lassen oder andere Update-Logik hier

'''
Start first tick
1 tick = 1 second
'''
invoke(tick, delay=1)

app.run()