import requests
import json

BASE_URL = (
    "https://poe.ninja/poe1/api/economy/stash/current/item/overview"
    "?league=Phrecia+2.0&type="
)

ITEM_TYPES = ["UniqueWeapon", "UniqueArmour", "UniqueJewel", "UniqueAccessory", "UniqueFlask"]

with open("Cards/cardResults.json", "r") as f:
    cards = json.load(f)
reward_set = {card["reward"] for card in cards if card["reward"]}

def fetch_items():
    results = {}

    for item_type in ITEM_TYPES:
        print(item_type)

        response = requests.get(BASE_URL + item_type, timeout=10)
        response.raise_for_status()
        data = response.json()

        results[item_type] = []

        for entry in data.get("lines", []):
            if (entry["chaosValue"] > 50 and "Foulborn" not in entry["name"] 
                and "Replica" not in entry["name"] 
                and any(reward in entry["name"] for reward in reward_set)
                and "Precursor's" not in entry["name"]):
                results[item_type].append({
                    "id": entry["id"],
                    "icon": entry["icon"],
                    "name": entry["name"]
                })

    return results

if __name__ == "__main__":
    items = fetch_items()

    with open("Uniques/uniques.json", "w") as f:
        json.dump(items, f, indent=2)

    print(f"Saved {len(items)} items")
