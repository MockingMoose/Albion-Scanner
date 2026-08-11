import json
import os
import requests
import time


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ITEMS_FILE = os.path.join(BASE_DIR, "data", "items.json")
CITIES = ["Caerleon", "Bridgewatch", "Martlock", "Fort Sterling", "Limhurst", "Thetford"]
BASE_URL = "https://www.albion-online-data.com/api/v2/stats/prices/"

with open(ITEMS_FILE, "r") as f:
    ITEMS = json.load(f)

def generate_enchants(item_id):
    return [item_id] + [f'{item_id}@{i}' for i in range(1, 4)]

def build_item_list():
    all_items = []
    for category in ITEMS:
        for item_id in ITEMS[category]:
            all_items.append(item_id)
            all_items.extend(generate_enchants(item_id))
    return all_items

def batched_scan():
    results = []
    items = build_item_list()
    #city_string = ','.join(CITIES)

    CHUNK_SIZE  = 100

    for i in range(0, len(items), CHUNK_SIZE):
        chunk = items[i:i + CHUNK_SIZE]
        item_string = ",".join(chunk)

        url = f"{BASE_URL}{item_string}.json?locations=Bridgewatch"

        response = requests.get(url)
        time.sleep(0.25)  # rate limit

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
            print("Error fetching batch starting at index", i)

    return results

if __name__ == "__main__":
    print("Running batched scanner test...\n")

    results = batched_scan()

    for entry in results[:20]:
        print(entry)

    print(f"\nTotal entries scanned: {len(results)}")
    