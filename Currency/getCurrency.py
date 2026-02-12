import requests
from datetime import datetime
import json

API_URL = "https://poeez.com/api/Economy/pc/Phrecia%202.0"

def get_todays_points():
    resp = requests.get(API_URL)
    resp.raise_for_status()
    data = resp.json()

    today = datetime.fromisoformat(data["timestamp"]).date()
    results = {}

    for item_name, item_data in data["summary"].items():
        for key in ("chaosPlottingPoints", "divinePlottingPoints"):
            for point in item_data.get(key, []):
                point_day = datetime.fromisoformat(point["day"]).date()

                if point_day == today and point["volume"] > 100 and point["bid"] < 0.33:
                    # Keep only the highest volume per item and that are worth at least 3 chaos
                    if (
                        item_name not in results
                        or point["volume"] > results[item_name]["volume"]
                    ):
                        results[item_name] = {
                            "item": item_name,
                            "day": point["day"],
                            "volume": point["volume"]
                        }

    return list(results.values())

if __name__ == "__main__":
    points = get_todays_points()
    with open("Currency/currency.json", "w") as f:
        json.dump(points, f, indent=2)
