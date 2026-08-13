from scanner.scan import batched_scan
from storage.storage import save_results, load_results
from analysis.enchant_profit import calculate_material_cost, group_data, get_lowest_sell, get_materials, get_enchant_material_prices, get_item_type

if __name__ == "__main__":
    #results = batched_scan()
    #save_results(results)
    #print(f"Scan complete. Saved {len(results)} entries.")
    data = load_results()

    grouped = group_data(data)

    lowest = get_lowest_sell(grouped)
    needed_materials = get_materials("T6_CAPE@1", "T6_CAPE@2")
    material_prices = get_enchant_material_prices(lowest)

    
    print(calculate_material_cost(needed_materials, material_prices))