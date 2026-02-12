import requests
import re
import json
from bs4 import BeautifulSoup

URL = "https://poedb.tw/us/Divination_Cards"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

with open("Currency/CurrencyResults.json", "r") as f:
    valuable_Cards = json.load(f)
reward_set = {
    card["currencyTradeId"]
    for card in valuable_Cards
    if card.get("currencyTradeId")
}


cards = {}

# PoEDB renders each card as text blocks.
# We search for "Stack Size: 1 / X"

text = soup.get_text("\n")

# Regex:
# Capture card name (line before Stack Size)
pattern = re.findall(
    r"\n\s*([^\n]+?)\s*\n\s*Stack Size:\s*1\s*/\s*(\d+)\s*\n\s*([^\n]+)",
    text
)

results = []

for name, stack, reward in pattern:
    card_slug = name.strip().lower().replace(" ", "-")
    stack = int(stack)
    reward = reward.strip()

    if not (
        any(char.isdigit() for char in reward)
        or "Limit" in reward
        or "Disabled" in reward
        or "Item" in reward
        or "Jewel" in reward
        or "link" in reward
        or "Scarab" in reward
        or "Gem" in reward
        or "Blueprint" in reward
    ) and any(card_slug in trade_id for trade_id in reward_set):

        results.append({
            "name": card_slug,
            "stack_size": stack,
            "reward": reward
        })

# Save JSON
with open("Cards/cardResults.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Saved {len(results)} divination cards.")
