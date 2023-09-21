import sqlite3
from datasource import retrieve_top_cryptos
from datatransformation import clean_crypto_data

def create_and_insert_data(dataframe):
    """
    Inserts data from a Pandas DataFrame into an SQLite database.

    This function connects to an SQLite database named 'crypto_data.db' and
    inserts the data from the provided DataFrame into a table.
    If the table already exists, it will be replaced with the new data.

    Parameters:
        dataframe (pandas.DataFrame): The DataFrame containing cryptocurrency
        data to be inserted.

    Returns:
        None
    """
    conn = sqlite3.connect("crypto_data.db")
    dataframe.to_sql("cryptocurrencies", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    top_cryptos_data = retrieve_top_cryptos()
    if top_cryptos_data:
        cleaned_crypto_df = clean_crypto_data(top_cryptos_data)
        create_and_insert_data(cleaned_crypto_df)
        print(cleaned_crypto_df)
