import json
import pandas as pd

from datasource import retrieve_top_cryptos

def clean_crypto_data(crypto_data):
    """
    Cleans and transforms cryptocurrency data using Pandas.

    This function takes a DataFrame of cryptocurrency data as input and performs
    several data cleaning and transformation steps. It removes missing values,
    standardizes and cleans text data, handles outliers, validates data,
    renames columns, and extracts specific metrics from the 'quote' column.
    The resulting DataFrame is ready for further analysis.

    Args:
        crypto_data (DataFrame): A DataFrame containing cryptocurrency data.

    Returns:
        DataFrame: A cleaned and transformed DataFrame ready for analysis.

    Example:
        To clean and transform cryptocurrency data, you can call the function as follows:
        cleaned_data = clean_crypto_data(crypto_data)
    """
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
        crypto_df["quote"].apply(lambda x: x["USD"]["price"]) <= price_upper_limit]

    # 4. Data Validation (removing rows with negative market cap)
    crypto_df = crypto_df[
        crypto_df["quote"].apply(lambda x: x["USD"]["market_cap"]) >= 0]

    # 5. Column Renaming and Reordering
    crypto_df.rename(columns={"name": "Asset"}, inplace=True)
    crypto_df.rename(columns={"symbol": "Token Symbol"}, inplace=True)
    crypto_df.rename(columns={"last_updated": "Last Updated"}, inplace=True)

    # 6. Extract specific metrics from 'quote', rename and create new columns
    crypto_df["Price (USD)"] = (
        crypto_df["quote"].apply(lambda x: x["USD"]["price"]))
    crypto_df["Trading Volume (24hr)"] = (
        crypto_df["quote"].apply(lambda x: x["USD"]["volume_24h"]))
    crypto_df["Market Cap (USD)"] = (
        crypto_df["quote"].apply(lambda x: x["USD"]["market_cap"]))
    crypto_df["Volume Change % (24hr)"] = (
        crypto_df["quote"].apply(lambda x: x["USD"]["volume_change_24h"]))
    crypto_df["Price Change % (24hr)"] = (
        crypto_df["quote"].apply(lambda x: x["USD"]["percent_change_24h"]))
    crypto_df["Price Change % (7d)"] = (
        crypto_df["quote"].apply(lambda x: x["USD"]["percent_change_7d"]))

    # 7. Reorder columns
    crypto_df = crypto_df[["Token Symbol", "Asset", "Market Cap (USD)",
                           "Price (USD)", "Price Change % (24hr)",
                           "Price Change % (7d)", "Trading Volume (24hr)",
                           "Volume Change % (24hr)", "Last Updated"]]
    return crypto_df
