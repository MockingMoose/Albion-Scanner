from scanner.scan import batched_scan
from storage.storage import save_results, load_results
from analysis.enchant_profit import group_data, get_lowest_sell

if __name__ == "__main__":
    results = batched_scan()
    save_results(results)
    print(f"Scan complete. Saved {len(results)} entries.")
    data = load_results()

    grouped = group_data(data)

    lowest = get_lowest_sell(grouped)

    print(lowest)
    #profits = find_best_enchant_profits(data)

    #for p in profits[:20]:
        #print(p)