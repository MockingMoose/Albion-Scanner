import json
import os
import requests
import time


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ITEMS_FILE = os.path.join(BASE_DIR, "data", "all_items.json")
CITIES = ["Caerleon", "Bridgewatch", "Martlock", "Fort Sterling", "Limhurst", "Thetford"]
BASE_URL = "https://www.albion-online-data.com/api/v2/stats/prices/"

with open(ITEMS_FILE, "r") as f:
    BASE_ITEMS = json.load(f)

def generate_enchants(item_id):
    return [item_id] + [f'{item_id}@{i}' for i in range(1, 4)]

def build_item_list():
    all_items = []
    for item_id in BASE_ITEMS:
        all_items.extend(generate_enchants(item_id))
    return all_items

def chunk_items_by_url_limit(items, cities):
    max_len = 4096
    city_string = ",".join(cities)
    base_url = f"{BASE_URL}"
    suffix = f".json?locations={city_string}&qualities=1"

    chunks = []
    current = []

    for item in items:
        test_chunk = current + [item]
        item_string = ",".join(test_chunk)
        url = f"{base_url}{item_string}{suffix}"

        if len(url) > max_len:
            chunks.append(current)
            current = [item]
        else:
            current.append(item)

    if current:
        chunks.append(current)

    return chunks

def batched_scan(cities):
    results = []
    items = build_item_list()

    chunks = chunk_items_by_url_limit(items, cities)

    for chunk in chunks:
        item_string = ",".join(chunk)
        city_string = ",".join(cities)

        url = f"{BASE_URL}{item_string}.json?locations={city_string}&qualities=1"

        response = requests.get(url)
        time.sleep(0.25)

        if response.status_code == 200:

            data = response.json()
            for entry in data:
                city = entry["city"]
                sell = entry["sell_price_min"]
                buy = entry["buy_price_max"]

                if city == "0":
                    continue
                if sell == 0 and buy == 0:
                    continue

                results.append({
                    "item": entry["item_id"],
                    "city": city,
                    "sell_price": sell,
                    "buy_price": buy,
                    "last_sold": entry["sell_price_min_date"]
                })
        else:
            print("Error fetching chunk")

    return results

if __name__ == "__main__":
    print("Running batched scanner test...\n")

    results = batched_scan()

    for entry in results[:20]:
        print(entry)

    print(f"\nTotal entries scanned: {len(results)}")
    