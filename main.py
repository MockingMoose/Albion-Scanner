import json
import os

from scanner.scan import batched_scan, build_item_list, chunk_items_by_url_limit, generate_enchants
from storage.storage import save_results, load_results
from scanner.flip_scan import run_flip_scan
import analysis.enchant_profit as ep

if __name__ == "__main__":
    #cities = ["Lymhurst"]
    #results = batched_scan(cities)
    #save_results(results)
    #print(f"Scan complete. Saved {len(results)} entries.")

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    STORAGE_FILE = os.path.join(BASE_DIR, "albion-scanner/data", "all_items.json")

    data = load_results()

    def load_results():
        with open(STORAGE_FILE , "r") as f:
            return json.load(f)
        
    items = load_results()
    grouped = ep.group_data(data)

    lowest = ep.get_lowest_sell(grouped)

    results = (run_flip_scan(items, lowest, grouped, False))

    def save_results(results):
        with open("C:/repos/albion-scanner/albion-frontend/public/profits.json", "w") as f:
            json.dump(results, f, indent=2)

    save_results(results)
