import requests

# Example Token ID for the June Market
TOKEN_ID = "38397507750621893057346880033441136112987238933685677349709401910643842844855"

def get_order_book_analysis(token_id):
    url = f"https://clob.polymarket.com/book?token_id={token_id}"
    resp = requests.get(url).json()
    
    bids = resp.get('bids', [])
    asks = resp.get('asks', [])

    print(f"{'CUMULATIVE BIDS':<18} | {'CUMULATIVE ASKS':<18} | {'IMBALANCE':<12} | {'LIQ. COST'}")
    print("-" * 75)

    cum_bid_size = 0
    cum_ask_size = 0

    # Look at the top 5 levels
    for i in range(5):
        # Handle Bids (Buyers)
        if i < len(bids):
            b_p = float(bids[-i-1]['price'])
            b_s = float(bids[-i-1]['size'])
            cum_bid_size += b_s
            bid_str = f"{cum_bid_size:>9.0f} @ ${b_p:.2f}"
        else:
            bid_str = "N/A"

        # Handle Asks (Sellers)
        if i < len(asks):
            a_p = float(asks[-i-1]['price'])
            a_s = float(asks[-i-1]['size'])
            cum_ask_size += a_s
            ask_str = f"{cum_ask_size:>9.0f} @ ${a_p:.2f}"
        else:
            ask_str = "N/A"

        # Calculate Imbalance (Difference in cumulative size)
        imbalance = cum_bid_size - cum_ask_size
        
        # Calculate Liquidity Cost (The Spread at this level)
        # Note: At level 0, this is the standard Bid-Ask Spread
        liq_cost = a_p - b_p if (i < len(bids) and i < len(asks)) else 0

        print(f"{bid_str:<18} | {ask_str:<18} | {imbalance:>12.0f} | ${liq_cost:.2f}")

if __name__ == "__main__":
    get_order_book_analysis(TOKEN_ID)