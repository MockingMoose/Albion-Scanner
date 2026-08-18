from analysis.enchant_profit import evaluate_flip, get_item_enchant_level
from scanner.scan import generate_enchants

def run_flip_scan(base_items, lowest_prices, grouped):
    results = []

    for base in base_items:

        enchants = generate_enchants(base)

        for target in enchants:
            if target == base:
                continue
            target_entries = grouped.get(target, [])
            if not target_entries:
                continue
            result = evaluate_flip(base, target, lowest_prices, target_entries)
            if result["ok"]:
                results.append(result)

        if enchants[1] in lowest_prices:
            target_entries = grouped.get(enchants[2], [])
            if target_entries:
                result = evaluate_flip(enchants[1], enchants[2], lowest_prices, target_entries)
                if result["ok"]:
                    results.append(result)

            target_entries = grouped.get(enchants[3], [])
            if target_entries:
                result = evaluate_flip(enchants[1], enchants[3], lowest_prices, target_entries)
                if result["ok"]:
                    results.append(result)

        if enchants[2] in lowest_prices:
            target_entries = grouped.get(enchants[3], [])
            if target_entries:
                result = evaluate_flip(enchants[2], enchants[3], lowest_prices, target_entries)
                if result["ok"]:
                    results.append(result)
    results.sort(key=lambda r: r["profit"], reverse=True)
    return results