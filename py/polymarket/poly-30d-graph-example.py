import requests
from datetime import datetime

SLUGS = {
    "JUN": "will-the-iranian-regime-fall-by-june-30",
    "DEC": "will-the-iranian-regime-fall-by-the-end-of-2026"
}

def get_token_id(slug):
    url = f"https://gamma-api.polymarket.com/markets?slug={slug}"
    try:
        resp = requests.get(url).json()
        if resp and isinstance(resp, list):
            token_ids = resp[0].get('clobTokenIds')
            if token_ids:
                return token_ids.strip('[]"').split(',')[0].strip(' "')
    except: pass
    return None

def get_history(token_id, label):
    """Fetch history using the 'interval' parameter to avoid timestamp range errors."""
    url = "https://clob.polymarket.com/prices-history"
    params = {
        "market": token_id,
        "interval": "1m",   # Requests the last 1 month of data
        "fidelity": 1440    # One data point per day (1440 minutes)
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    if 'history' not in data or not data['history']:
        print(f"⚠️ No data for {label}. Response: {data}")
        return {}

    # Map history to { 'YYYY-MM-DD': price }
    return {datetime.fromtimestamp(p['t']).strftime('%Y-%m-%d'): p['p'] for p in data['history']}

def main():
    ids = {k: get_token_id(v) for k, v in SLUGS.items()}
    if not all(ids.values()):
        print("Error: Could not find Token IDs.")
        return

    history_jun = get_history(ids['JUN'], "JUNE")
    history_dec = get_history(ids['DEC'], "DEC")

    print("\nYYYY-MM-DD, %JUN, %DEC, %SPREAD")
    print("-" * 40)

    # Sort by date to show chronological order
    all_dates = sorted(set(history_jun.keys()) & set(history_dec.keys()))
    
    for date in all_dates:
        p_jun, p_dec = history_jun[date], history_dec[date]
        spread = p_dec - p_jun
        print(f"{date}, {p_jun*100:5.1f}%, {p_dec*100:5.1f}%, {spread*100:7.1f}%")

if __name__ == "__main__":
    main()