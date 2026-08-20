import requests
import time
from datetime import datetime

# --- CONFIGURATION ---
# Replace these with the actual Token IDs found in the browser Network tab
JUNE_TOKEN_ID = "38397507750621893057346880033441136112987238933685677349709401910643842844855"
DEC_TOKEN_ID  = "10991849228756847439673778874175365458450913336396982752046655649803657501964"

# Set a threshold for alerts (e.g., alert if spread moves by 2%)
INITIAL_SPREAD = 0.12 
THRESHOLD = 0.02 

def get_midpoint(token_id):
    """Fetches the live midpoint price from Polymarket CLOB."""
    url = f"https://clob.polymarket.com/midpoint?token_id={token_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return float(response.json().get('mid', 0))
    except Exception as e:
        print(f"Error fetching {token_id[:8]}...: {e}")
    return None

def monitor_spread():
    print(f"--- Monitoring Started at {datetime.now().strftime('%H:%M:%S')} ---")
    print(f"Targeting Spread: {INITIAL_SPREAD*100}% | Alert Threshold: +/-{THRESHOLD*100}%")
    
    while True:
        june_price = get_midpoint(JUNE_TOKEN_ID)
        dec_price = get_midpoint(DEC_TOKEN_ID)

        if june_price and dec_price:
            # Calculate the marginal probability (H2 window)
            current_spread = dec_price - june_price
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"[{timestamp}] June: {june_price:.2%} | Dec: {dec_price:.2%} | H2 Spread: {current_spread:.2%}")

            # Check for significant movement
            if abs(current_spread - INITIAL_SPREAD) >= THRESHOLD:
                print(f"⚠️ ALERT: Spread has shifted! Current: {current_spread:.2%}")
                # You could add a Telegram/Discord webhook call here
        
        # Poll every 60 seconds to avoid rate limits
        time.sleep(60)

if __name__ == "__main__":
    monitor_spread()