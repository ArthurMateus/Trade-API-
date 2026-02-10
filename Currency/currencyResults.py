import requests
import json

BASE_URL = "https://poeez.com/api/Economy/pc/Phrecia%202.0/"

# Load items from api.json
with open("Currency/api.json", "r") as f:
    items = json.load(f)

CURRENCIES = [item["item"] for item in items]
print(CURRENCIES)

def get_latest_prices():
    results = []

    for currency in CURRENCIES:
        response = requests.get(BASE_URL + currency, timeout=10)
        response.raise_for_status()
        data = response.json()

        history = data.get("history", [])

        # Skip if no data
        if not history:
            continue

        latest = history[0]  # 🔥 already the latest hour

        results.append({
            "currencyTradeId": data["currencyTradeId"],
            "history": [latest]
        })

    with open("Currency/currencyResults.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


if __name__ == "__main__":
    get_latest_prices()
