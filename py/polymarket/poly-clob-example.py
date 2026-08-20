import requests

# Every outcome (like "Yes" for June) has a unique Token ID
# You find these IDs using the Gamma API or the URL on Polymarket
JUNE_YES_TOKEN_ID = "38397507750621893057346880033441136112987238933685677349709401910643842844855" 

def get_realtime_price(token_id):
    url = f"https://clob.polymarket.com/midpoint?token_id={token_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return float(response.json()['mid'])
    return None

price = get_realtime_price(JUNE_YES_TOKEN_ID)
print(f"Current Live Price: {price * 100:.2f}%")