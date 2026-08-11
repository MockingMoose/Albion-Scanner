import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STORAGE_FILE = os.path.join(BASE_DIR, "storage", "market_data.json")

def save_results(results):
    with open(STORAGE_FILE, "w") as f:
        json.dump(results, f, indent=2)

def load_results():
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)
    