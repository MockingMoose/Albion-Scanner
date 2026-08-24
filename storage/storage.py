import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STORAGE_FILE = os.path.join(BASE_DIR, "storage", "market_data.json")

def save_results(results, destination):
    print("Saving results to", destination)
    with open(destination, "w") as f:
        json.dump(results, f, indent=2)

def load_results(source):
    print("Loading data from", source)
    with open(source, "r") as f:
        return json.load(f)

def load_items():
    with open("./data/items_name.json", "r", encoding="utf-8") as f:
        items_data = json.load(f)

    item_names = {}

    for item in items_data:
        unique = item.get("UniqueName")
        if not unique:
            continue 

        localized = item.get("LocalizedNames")

        if isinstance(localized, dict):
            name = localized.get("EN-US", unique)
        else:
            name = unique

        item_names[unique] = name

    return item_names