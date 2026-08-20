import requests

SUBGRAPH_URL = "https://api.goldsky.com/api/public/project_cl6aw664f199101u87dz66v98/subgraphs/polymarket-orderbook/latest/gn"

query = """
{
  orderFilledEvents(first: 5, orderBy: timestamp, orderDirection: desc) {
    price
    timestamp
    targetTokenId
  }
}
"""

response = requests.post(SUBGRAPH_URL, json={'query': query})
trades = response.json()['data']['orderFilledEvents']

for trade in trades:
    print(f"Time: {trade['timestamp']}, Price: {trade['price']}")