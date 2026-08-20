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

def get_history(token_id):
    url = "https://clob.polymarket.com/prices-history"
    params = {"market": token_id, "interval": "1m", "fidelity": 1440}
    response = requests.get(url, params=params).json()
    if 'history' not in response: return {}
    return {datetime.fromtimestamp(p['t']).strftime('%Y-%m-%d'): p['p'] for p in response['history']}

def main():
    ids = {k: get_token_id(v) for k, v in SLUGS.items()}
    if not all(ids.values()): return

    history_jun = get_history(ids['JUN'])
    history_dec = get_history(ids['DEC'])

    # Header with new terminology
    print(f"{'DATE':<12} | {'%JUN':<7} | {'%DEC':<7} | {'MARGINAL':<10} | {'REL. EXTENSION'}")
    print("-" * 65)

    all_dates = sorted(set(history_jun.keys()) & set(history_dec.keys()))
    
    for date in all_dates:
        p_j, p_d = history_jun[date], history_dec[date]
        
        # 1. Marginal Probability (Chance of happening specifically in H2)
        marginal = p_d - p_j
        
        # 2. Relative Extension (Ratio of H2 risk to H1 risk)
        # We use a safety check to avoid division by zero
        ratio = (marginal / p_j) if p_j > 0 else 0
        
        print(f"{date:<12} | {p_j:6.1%} | {p_d:6.1%} | {marginal:9.1%} | {ratio:.2f}")

if __name__ == "__main__":
    main()