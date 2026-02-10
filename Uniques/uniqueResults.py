import requests
import json

BASE_URL = (
    "https://poe.ninja/poe1/api/economy/stash/current/item/history"
    "?league=Phrecia+2.0&type={type}&id={id}"
)

with open("Uniques/uniques.json", "r") as f:
    items = json.load(f)

def fetch_items():
    results = []

    for parent_type, entries in items.items():
        for entry in entries:
            print(entry["name"])
            item_id = entry["id"]
            item_name = entry["name"]

            url = BASE_URL.format(
                type=parent_type,
                id=item_id
            )

            response = requests.get(url, timeout=10)
            response.raise_for_status()
            history = response.json()

            today = next(
                (h for h in history if h.get("daysAgo") == 0),
                None
            )

            if not today:
                continue

            results.append({
                "name": item_name,
                "value": today["value"],
                "count": today["count"]
            })

    return results




if __name__ == "__main__":
    items = fetch_items()

    with open("Uniques/uniqueResults.json", "w") as f:
        json.dump(items, f, indent=2)

    print(f"Saved {len(items)} items")
