import os
import requests

if os.path.exists("env.py"):
    import env

COINMARKETCAP_API_KEY = os.environ.get("CMC_API_KEY")

def retrieve_top_cryptos():
    """
    Retrieves data for the top 1000 cryptocurrencies by market cap from the
    CoinMarketCap API.

    This function sends a request to the CoinMarketCap API to retrieve data for
    the top cryptocurrencies based on market capitalization. The data includes
    metrics such as price and trading volume.

    Returns:
        list: A list of cryptocurrency data, where each item represents a
        cryptocurrency and its metrics.

    Note:
        The data returned by this function includes various metrics, which can
        be further processed and transformed in other parts of the code.
    """

    top_n_cryptos = 1000

    api_url = (
        "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest")

    params = {
        "start": "1",
        "limit": str(top_n_cryptos),
        "convert": "USD",
        "sort": "market_cap",
        "CMC_PRO_API_KEY": COINMARKETCAP_API_KEY,
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        crypto_data = response.json()["data"]
        return crypto_data
    else:
        print("Failed to retrieve data from CoinMarketCap API.")
        return []
