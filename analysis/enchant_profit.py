from analysis.enchant_rules import ENCHANT_MATERIALS, ENCHANT_MAP
from storage.storage import load_items
from collections import defaultdict
from datetime import timedelta, datetime

ITEM_NAMES = load_items()

def get_icon_url(item_id):
    return f"https://render.albiononline.com/v1/item/{item_id}.png"

def sold_recently(entries, days=3):
    if not entries:
        return False

    cutoff = datetime.now() - timedelta(days=days)

    for entry in entries:
        if entry.get("sell_price", 0) <= 0:
            continue

        date_str = entry.get("last_sold")
        if not date_str or date_str == "0001-01-01T00:00:00":
            continue

        try:
            last_update = datetime.fromisoformat(date_str)
        except ValueError:
            continue

        if last_update >= cutoff:
            return True

    return False

def strip(item_id):
    return item_id.split("@")[0]

def check_item_types_match(base_item, target_item):
    return strip(base_item) == strip(target_item)
    
def get_item_type(item_id):
    parts = item_id.split("@")[0].split("_")

    for part in parts:
        clean = part.strip().upper()
        if clean in ENCHANT_MAP:
            return clean

    return "Unknown"
    
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

    return material_prices

def calculate_material_cost(materials: dict, prices: dict) -> dict:
    breakdown = {}
    missing = []
    total = 0

    for material_id, qty in materials.items():
        unit_price = prices.get(material_id)
        if unit_price is None or unit_price <= 0:
            missing.append(material_id)
            continue

        cost = qty * unit_price
        breakdown[material_id] = cost
        total += cost

    if missing:
        return {
            "ok": False,
            "reason": "missing_prices", 
            "missing": missing,
            "breakdown": breakdown,
            "total": total
            }
    
    return {
        "ok": True,
        "breakdown": breakdown,
        "total": total
        }

def get_materials(base_id: str, target_id: str) -> dict:
    enchant_level_materials = {
        1: "RUNE",
        2: "SOUL",
        3: "RELIC"
    }

    base_enchant = get_item_enchant_level(base_id)
    target_enchant = get_item_enchant_level(target_id)
    base_tier = get_item_tier(base_id)

    if target_enchant is None:
        print("Target Enchant Is None")
        return None

    if target_enchant < base_enchant:
        print("Cannot Enchant, Target level is less than base level", base_id, target_id)
        return None
    
    if base_id == target_id:
        print("Cannot Enchant, Item enchant levels are the same", base_id, target_id)
        return None

    if not check_item_types_match(base_id, target_id):
        print("Items do not match", base_id, target_id)
        return None

    base_item_type = get_item_type(base_id)

    if base_item_type == "Unknown":
        return None

    if base_item_type not in ENCHANT_MAP:
        print("Item Type Does Not Exist", base_item_type)
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
            
def get_current_sell_price(item_id, lowest_prices):
    if item_id not in lowest_prices:
        return None
    return lowest_prices.get(item_id)

def evaluate_flip(base_id, target_id, lowest_prices, target_entries):
    reqired_materials = get_materials(base_id, target_id)
    
    if not sold_recently(target_entries):
        return {
            "ok": False,
            "reason": "not sold recently"
        }
    
    if reqired_materials is None:
        return {
            "ok": False,
            "reason": "invalid material requirements"
        }
    
    base_price = get_current_sell_price(base_id, lowest_prices)
    target_price = get_current_sell_price(target_id, lowest_prices)

    if base_price is None:
        return {
            "ok": False,
            "reason": "missing base price"
        }
    if target_price is None:
        return {
            "ok": False,
            "reason": "missing target price"
        }
    
    material_prices = get_enchant_material_prices(lowest_prices)
    cost_result = calculate_material_cost(reqired_materials, material_prices)

    if not cost_result["ok"]:
        return {
            "ok": False,
            "reason": "missing material prices",
            "missing": cost_result["missing"]
        }

    total_cost = base_price + cost_result["total"]
    profit = target_price - total_cost

    if profit <= 0:
        return {
            "ok": False,
            "reason": "profit is negative or zero"
        }

    return {
        "ok": True,
        "base_id": base_id,
        "base_icon": get_icon_url(base_id),
        "base_name": ITEM_NAMES.get(base_id, base_id),
        "base_enchant": get_item_enchant_level(base_id),
        "target_id": target_id,
        "target_icon": get_icon_url(target_id),
        "target_name": ITEM_NAMES.get(target_id, target_id),
        "target_enchant": get_item_enchant_level(target_id),
        "base_price": base_price,
        "target_price": target_price,
        "required_materials": reqired_materials,
        "material_cost": cost_result["total"],
        "total_cost": total_cost,
        "profit": profit
    }