import os

from scanner.scan import batched_scan
from storage.storage import save_results, load_results
from scanner.flip_scan import run_flip_scan
import analysis.enchant_profit as ep

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def run_full_scan(cities, premium):
    print("Running scan with city: ", cities)
    results = batched_scan(cities)
    save_results(results, "storage/market_data.json")

    print(f"Scan complete. Saved {len(results)} entries.")
    source = os.path.join(BASE_DIR, "storage/market_data.json")
    data = load_results(source)
    source = os.path.join(BASE_DIR, "data/all_items.json")
    items = load_results(source)

    grouped = ep.group_data(data)
    lowest = ep.get_lowest_sell(grouped)
    results = (run_flip_scan(items, lowest, grouped, premium))
    destination = os.path.join(BASE_DIR, "storage/profits.json")
    save_results(results, destination)