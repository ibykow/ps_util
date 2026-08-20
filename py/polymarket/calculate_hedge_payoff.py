def calculate_hedge_payoff(jun_price, dec_price, investment=100):
    # Cost to buy 1 share of each
    # Strategy: Buy 1 Jun-YES and 1 Dec-NO
    dec_no_price = 1.0 - dec_price
    total_cost_per_share = jun_price + dec_no_price
    shares = investment / total_cost_per_share

    print(f"--- Hedge Analysis: Jun-YES & Dec-NO ($ {investment} total) ---")
    print(f"Shares Purchased: {shares:.2f}")
    print("-" * 50)

    # Scenario 1: Happens by June 30
    # Jun-YES pays $1, Dec-NO pays $0 (because event happened)
    s1_payout = shares * 1.0
    s1_profit = s1_payout - investment
    
    # Scenario 2: Happens in H2 (The "Death Zone")
    # Jun-YES pays $0, Dec-NO pays $0
    s2_payout = 0
    s2_profit = s2_payout - investment

    # Scenario 3: Never happens
    # Jun-YES pays $0, Dec-NO pays $1.0
    s3_payout = shares * 1.0
    s3_profit = s3_payout - investment

    print(f"1. Early (Before June):  Profit ${s1_profit:>6.2f} ({s1_profit/investment:>5.1%})")
    print(f"2. Delayed (H2 Window):  Profit ${s2_profit:>6.2f} ({s2_profit/investment:>5.1%})")
    print(f"3. Never (After 2026):  Profit ${s3_profit:>6.2f} ({s3_profit/investment:>5.1%})")

# Using your March 4th values: Jun 38.5%, Dec 50.5%
calculate_hedge_payoff(0.385, 0.505)