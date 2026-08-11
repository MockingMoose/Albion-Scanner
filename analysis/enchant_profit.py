from storage.storage import load_results
from analysis.enchant_rules import ENCHANT_MATERIALS, ENCHANT_MAP

def get_item_type(item_id):
    parts = item_id.split("_")
    if len(parts) < 2:
        return "Unknown"
    return parts[1]

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
        
def get_lowest_sell(data):
    lowest = {}
    for item_id, entries in data.items():
        sell_prices = [e["sell_price"] for e in entries if e["sell_price"] > 0]
        if not sell_prices:
            lowest[item_id] = None
            continue
        lowest[item_id] = min(sell_prices)
    return lowest

def get_enchant_material_prices(lowest_prices):
    material_prices = {}
    for material_id in ENCHANT_MATERIALS:
        material_prices[material_id] = lowest_prices.get(material_id)
    return material_prices

def get_materials(base_id, target_id):
    item_type = get_item_type(base_id)
    material_cost = ENCHANT_MAP[item_type]

