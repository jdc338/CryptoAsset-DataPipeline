import os

import pandas as pd
import requests
import json

if os.path.exists("env.py"):
    import env

COINMARKETCAP_API_KEY = os.environ.get("CMC_API_KEY")

"""
Retrieving data for the top 30 cryptocurrencies by market cap from the
CoinMarketCap API.

"""


def retrieve_top_cryptos():
    top_n_cryptos = 30

    api_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

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


"""
Cleaning and Transforming data using Pandas

"""


import json  # Import the json module

def clean_crypto_data(crypto_data):
    crypto_df = pd.DataFrame(crypto_data)

    # 1. Handle Missing Values
    crypto_df.dropna(subset=["quote"], inplace=True)

    # 2. Convert the 'quote' column to a JSON string
    crypto_df['quote'] = crypto_df['quote'].apply(lambda x: json.dumps(x))

    # 4. Convert the 'quote' column back to dictionaries
    crypto_df['quote'] = crypto_df['quote'].apply(lambda x: json.loads(x))

    # 5. Standardize and Clean Text Data
    crypto_df["name"] = crypto_df["name"].str.strip()
    crypto_df["symbol"] = crypto_df["symbol"].str.upper()

    # 6. Outlier Detection and Handling (removing rows with outlier prices)
    price_upper_limit = (
        crypto_df["quote"].apply(lambda x: x["USD"]["price"]).quantile(0.99)
    )
    crypto_df = crypto_df[
        crypto_df["quote"].apply(lambda x: x["USD"]["price"]) <= price_upper_limit
    ]

    # 7. Data Validation (removing rows with negative market cap)
    crypto_df = crypto_df[
        crypto_df["quote"].apply(lambda x: x["USD"]["market_cap"]) >= 0
    ]

    # 8. Column Renaming and Reordering
    crypto_df.rename(columns={"name": "asset"}, inplace=True)
    crypto_df = crypto_df[
        ["symbol", "asset", "quote", "last_updated"]
    ]

    # Extract market_cap_usd from quote
    crypto_df["market_cap_usd"] = crypto_df["quote"].apply(
        lambda x: x["USD"]["market_cap"]
    )

    return crypto_df


if __name__ == "__main__":
    top_cryptos_data = retrieve_top_cryptos()
    if top_cryptos_data:
        cleaned_crypto_df = clean_crypto_data(top_cryptos_data)
        print(cleaned_crypto_df)
