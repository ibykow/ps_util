import requests
import time

# Use the Gamma API to get details about a specific event slug
# EVENT_SLUG = "will-the-iranian-regime-fall-by-june-30"
EVENT_SLUG = "will-the-iranian-regime-fall-by-the-end-of-2026"
URL = f"https://gamma-api.polymarket.com/events?slug={EVENT_SLUG}"

def collect_data():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()[0]
        # Extract Yes/No prices
        for market in data['markets']:
            print(f"Market: {market['question']}")
            print(f"Outcome Prices: {market['outcomePrices']}")
    else:
        print("Error fetching data")

# Run every hour
while True:
    collect_data()
    time.sleep(3600)