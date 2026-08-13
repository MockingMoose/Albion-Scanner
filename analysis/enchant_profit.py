from storage.storage import load_results
from analysis.enchant_rules import ENCHANT_MATERIALS, ENCHANT_MAP
from collections import defaultdict

def get_item_type(item_id):
    if "@" in item_id:
        parts = item_id.split("@")
        parts = parts[0].split("_")
    else:
        parts = item_id.split("_")
    if len(parts) < 2:
        return "Unknown"
    return str(parts[1])

def get_item_tier(item_id):
    parts = item_id.split("_")
    if len(parts) <2:
        return "Unknown"
    return str(parts[0])

def get_item_enchant_level(item_id):
    name = item_id
    if "@" in name:
        parts = name.split("@")
        if parts[1] == '' or not (parts[1].isdigit()):
            return None
        return int(parts[1])
    else:
        return 0

def group_data(data):
    grouped = {}
    for entry in data:
        item_id = entry["item"]
        if item_id not in grouped:
            grouped[item_id] = []
        grouped[item_id].append(entry)
    return grouped
        
def get_lowest_sell(data: dict) -> dict:
    lowest = {}
    for item_id, entries in data.items():
        sell_prices = [e["sell_price"] for e in entries if e["sell_price"] > 0]
        if not sell_prices:
            lowest[item_id] = None
            continue
        lowest[item_id] = min(sell_prices)
    return lowest

def get_enchant_material_prices(lowest_prices: dict) -> dict:
    material_prices = {}
    for material_id in ENCHANT_MATERIALS:
        material_prices[material_id] = lowest_prices.get(material_id)
    print(material_prices)    
    return material_prices

def calculate_material_cost(materials: dict, prices: dict) -> dict:
    material_cost = {}
    for material, amount in materials.items():
        price = amount * prices.get(material)
        print(f'{material} {price}')
        material_cost[material] = price
    return material_cost

def get_materials(base_id: str, target_id: str) -> dict:
    enchant_level_materials = {
        1: "RUNE",
        2: "SOUL",
        3: "RELIC"
    }

    base_enchant = get_item_enchant_level(base_id)
    target_enchant = get_item_enchant_level(target_id)
    base_tier = get_item_tier(base_id)
    target_tier = get_item_tier(target_id)

    if target_enchant is None:
        print("Target Enchant Is None")
        return None

    if target_enchant < base_enchant:
        print("Cannot Enchant, Target level is less than base level")
        return None
    if base_id == target_id:
        print("Cannot Enchant, Item enchant levels are the same")
        return None

    target_item_type = get_item_type(target_id)
    base_item_type = get_item_type(base_id)

    if base_tier != target_tier:
        print("Item Tiers Do Not Match")
        return None
    if base_item_type != target_item_type:
        print("Item Types Do Not Match")
        return None


    if base_item_type not in ENCHANT_MAP:
        print("Item Type Does Not Exist")
        return None

    amount_per_level = ENCHANT_MAP[base_item_type]
    materials = defaultdict(int)
    for level in range(base_enchant + 1, target_enchant + 1):
        material_name = enchant_level_materials.get(level)
        if material_name is None:
            print("Cannot Enchant")
            return None
        material_id = f"{base_tier}_{material_name}"
        materials[material_id] += amount_per_level
    return dict(materials)
            
