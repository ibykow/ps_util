import requests
import json

JUNE_YES_TOKEN_ID = "38397507750621893057346880033441136112987238933685677349709401910643842844855" 

def get_order_book(token_id):
    url = f"https://clob.polymarket.com/book?token_id={token_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        # 'bids' are sorted highest to lowest (Buy orders)
        # 'asks' are sorted lowest to highest (Sell orders)
        return data.get('bids', []), data.get('asks', [])
    return None, None

# Example usage with your June Token ID
bids, asks = get_order_book(JUNE_YES_TOKEN_ID)

print(f"{'BIDS (Buy Yes)':<17} | {'ASKS (Sell Yes)':<17} | BIDS - ASKS (Buy - Sell Yes)")

bids_len = len(bids)
asks_len = len(asks)

for i in range(5):
    b_p = bids[-i-1]['price'] if i < bids_len else "N/A"
    b_s = bids[-i-1]['size'] if i < bids_len else "N/A"
    a_p = asks[-i-1]['price'] if i < asks_len else "N/A"
    a_s = asks[-i-1]['size'] if i < asks_len else "N/A"

    d_s = float(b_s) - float(a_s)
    d_p = float(b_p) - float(a_p)
    print(f"{b_s:>9} @ ${b_p:<4} | {a_s:>9} @ ${a_p:<4} | {d_s:10.2f} @ ${d_p:.02f}")