import json

from scanner.scan import batched_scan
from storage.storage import save_results, load_results
import analysis.enchant_profit as ep

if __name__ == "__main__":
    #results = batched_scan()
    #save_results(results)
    #print(f"Scan complete. Saved {len(results)} entries.")
    data = load_results()

    grouped = ep.group_data(data)

    print(ep.get_item_type("T6_ARTEFACT_ARMOR_STAFF"))
    #lowest = get_lowest_sell(grouped)
    #needed_materials = get_materials("T6_CAPE", "T6_CAPE@2")
    #material_prices = get_enchant_material_prices(lowest)

    #print(get_current_sell_price("T4_BAG@2", lowest))
    #print(evaluate_flip("T4_BAG", "T4_BAG@2", lowest))
    