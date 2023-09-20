import os

import pandas as pd
import requests
import json
import sqlite3

if os.path.exists("env.py"):
    import env

COINMARKETCAP_API_KEY = os.environ.get("CMC_API_KEY")

"""
Retrieving data for the top 30 cryptocurrencies by market cap from the
CoinMarketCap API.
WHAT ARE THE PARAMETERS AND WHAT IT RETURNS.... LOOK AT EXAMPLES..

"""


def retrieve_top_cryptos():
    top_n_cryptos = 1000

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
WHAT ARE THE PARAMETERS AND WHAT IT RETURNS....

"""


def clean_crypto_data(crypto_data):
    crypto_df = pd.DataFrame(crypto_data)

    # 1. Handle Missing Values
    crypto_df.dropna(subset=["quote"], inplace=True)

    # 2. Standardize and Clean Text Data
    crypto_df["name"] = crypto_df["name"].str.strip()
    crypto_df["symbol"] = crypto_df["symbol"].str.upper()

    # 3. Outlier Detection and Handling (removing rows with outlier prices)
    price_upper_limit = (
        crypto_df["quote"].apply(lambda x: x["USD"]["price"]).quantile(0.99)
    )
    crypto_df = crypto_df[
        crypto_df["quote"].apply(lambda x: x["USD"]["price"]) <= price_upper_limit
    ]

    # 4. Data Validation (removing rows with negative market cap)
    crypto_df = crypto_df[
        crypto_df["quote"].apply(lambda x: x["USD"]["market_cap"]) >= 0
    ]

    # 5. Column Renaming and Reordering
    crypto_df.rename(columns={"name": "asset"}, inplace=True)

    # 6. Extract specific metrics from 'quote' and create separate columns
    crypto_df["price_usd"] = crypto_df["quote"].apply(lambda x: x["USD"]["price"])
    crypto_df["volume_24h_usd"] = crypto_df["quote"].apply(lambda x: x["USD"]["volume_24h"])
    crypto_df["market_cap_usd"] = crypto_df["quote"].apply(lambda x: x["USD"]["market_cap"])
    crypto_df["volume_change_24h"] = crypto_df["quote"].apply(lambda x: x["USD"]["volume_change_24h"])
    crypto_df["percent_change_24h"] = crypto_df["quote"].apply(lambda x: x["USD"]["percent_change_24h"])
    crypto_df["percent_change_7d"] = crypto_df["quote"].apply(lambda x: x["USD"]["percent_change_7d"])

    # 7. Extract volume_change_24h and percent_change_24h as percentages

    # 8. Reorder columns as needed
    crypto_df = crypto_df[["symbol", "asset", "market_cap_usd", "price_usd", "percent_change_24h", "percent_change_7d", "volume_24h_usd", "volume_change_24h", "last_updated"]]

    return crypto_df





def create_and_insert_data(dataframe):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("crypto_data.db")

    # Use the DataFrame to_sql method to insert data into the database
    dataframe.to_sql("cryptocurrencies", conn, if_exists="replace", index=False)

    # Commit and close the connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    top_cryptos_data = retrieve_top_cryptos()
    if top_cryptos_data:
        cleaned_crypto_df = clean_crypto_data(top_cryptos_data)
        # Call the function to insert data into the database
        create_and_insert_data(cleaned_crypto_df)
        print(cleaned_crypto_df)
