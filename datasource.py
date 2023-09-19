import requests
import os

if os.path.exists("env.py"):
    import env

COINMARKETCAP_API_KEY = os.environ.get('CMC_API_KEY')

"""
Retrieve data for the top cryptocurrencies by market cap from CoinMarketCap API.

"""
top_n_cryptos = 30

api_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

params = {
    "start": "1",
    "limit": str(top_n_cryptos),
    "convert": "USD",
    "sort": "market_cap",
    "CMC_PRO_API_KEY": COINMARKETCAP_API_KEY
}

response = requests.get(api_url, params=params)

if response.status_code == 200:
    crypto_data = response.json()['data']

else:
    print("Failed to retrieve data from CoinMarketCap API.")
