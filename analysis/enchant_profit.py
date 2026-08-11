from storage.storage import load_results

ENCHANT_MATERIALS = [
    "T4_RUNE","T5_RUNE","T6_RUNE","T7_RUNE","T8_RUNE",
    "T4_SOUL","T5_SOUL","T6_SOUL","T7_SOUL","T8_SOUL",
    "T4_RELIC","T5_RELIC","T6_RELIC","T7_RELIC","T8_RELIC"
    ]

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

