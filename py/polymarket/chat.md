Could you write a script that prints the historical data, and spread for these two slugs: will-the-iranian-regime-fall-by-june-30, and will-the-iranian-regime-fall-by-the-end-of-2026?
I'm hoping to get the daily spread for the past, say, 30 days with output on each line that follows the format:
YYYY-MM-DD, %JUN, %DEC, %SPREAD

It gave me the following error:

```
  File "poly-30d-graph-example.py", line 47, in main
    history_jun = get_history(ids['JUN'])
                  ^^^^^^^^^^^^^^^^^^^^^^^
  File "poly-30d-graph-example.py", line 36, in get_history
    return {datetime.fromtimestamp(p['t']).strftime('%Y-%m-%d'): p['p'] for p in resp['history']}
                                                                                 ~~~~^^^^^^^^^^^
KeyError: 'history'
```

Ah, it seems we're asking for too much:
Requesting Historical Data...
⚠️ Warning: No history found for JUNE (ID: 38397507750621893057346880033441136112987238933685677349709401910643842844855). API Response: {'error': "invalid filters: 'startTs' and 'endTs' interval is too long"}
⚠️ Warning: No history found for DEC (ID: 10991849228756847439673778874175365458450913336396982752046655649803657501964). API Response: {'error': "invalid filters: 'startTs' and 'endTs' interval is too long"}
❌ Error: Missing history for one or both markets. Execution stopped.


Here's the output. What are you thoughts?

YYYY-MM-DD, %JUN, %DEC, %SPREAD
----------------------------------------
2026-02-05,  21.5%,  28.5%,     7.0%
2026-02-06,  21.5%,  30.5%,     9.0%
2026-02-07,  19.5%,  32.5%,    13.0%
2026-02-08,  20.5%,  33.5%,    13.0%
2026-02-09,  19.5%,  32.5%,    13.0%
2026-02-11,  19.5%,  33.5%,    14.0%
2026-02-12,  17.5%,  32.5%,    15.0%
2026-02-13,  19.0%,  31.5%,    12.5%
2026-02-14,  20.0%,  31.5%,    11.5%
2026-02-16,  19.5%,  34.5%,    15.0%
2026-02-19,  28.5%,  39.5%,    11.0%
2026-02-20,  23.5%,  40.5%,    17.0%
2026-02-21,  23.5%,  38.5%,    15.0%
2026-02-22,  23.5%,  39.5%,    16.0%
2026-02-23,  25.0%,  36.5%,    11.5%
2026-02-24,  23.5%,  36.5%,    13.0%
2026-02-25,  21.5%,  35.5%,    14.0%
2026-02-26,  23.5%,  35.5%,    12.0%
2026-02-27,  28.5%,  40.5%,    12.0%
2026-03-02,  36.5%,  47.5%,    11.0%
2026-03-03,  39.5%,  49.5%,    10.0%
2026-03-04,  38.5%,  50.5%,    12.0%

So far we've been using the word "spread" to describe the YES% difference between June and December. Is there a better way to refer to this value? I ask because I'd like to include the Bid-Ask spread in our analysis at some point, and I don't want to mix up the terms too much. Also, it seems it would also be useful to know the ratio between this DecYes%-JunYes% difference and the JunYes%. Is there a term for that? What does it say about the values?




I've updated the script to loop over the last five items in each array because bids are sorted by low to highest price, and asks are sorted by highest to lowest. I also added a spread column. Here are the results:

BIDS (Buy Yes)    | ASKS (Sell Yes)   | BIDS - ASKS (Buy - Sell Yes)
 30981.96 @ $0.38 |  38241.02 @ $0.39 |   -7259.06 @ $-0.01
117255.94 @ $0.37 |  88610.97 @ $0.4  |   28644.97 @ $-0.03
 88166.55 @ $0.36 |  44011.54 @ $0.41 |   44155.01 @ $-0.05
 35498.36 @ $0.35 |  48280.71 @ $0.42 |  -12782.35 @ $-0.07
    15894 @ $0.34 |  11052.89 @ $0.43 |    4841.11 @ $-0.09

What do you make of this?


Dec:

BIDS (Buy Yes)    | ASKS (Sell Yes)   | BIDS - ASKS (Buy - Sell Yes)
 16212.41 @ $0.5  |     63.37 @ $0.51 |   16149.04 @ $-0.01
 59280.48 @ $0.49 |  43334.14 @ $0.52 |   15946.34 @ $-0.03
 83989.69 @ $0.48 |   42945.6 @ $0.53 |   41044.09 @ $-0.05
 34595.66 @ $0.47 |   4496.79 @ $0.54 |   30098.87 @ $-0.07
  9967.74 @ $0.46 |  11016.85 @ $0.55 |   -1049.11 @ $-0.09



Marginal Probability
Relative Extension / Tail Weight / Implied Survival Odds / Survival Factor

