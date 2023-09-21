import matplotlib.pyplot as plt
import streamlit as st

import datatransformation

# Load your cryptocurrency data and select the top 30
top_cryptos_data = datatransformation.retrieve_top_cryptos()
cleaned_crypto_df = datatransformation.clean_crypto_data(top_cryptos_data).head(30)

st.set_page_config(page_title="Crypto Asset Data Dashboard", layout="centered")

st.title("Crypto Asset Data Dashboard")

highest_price_change_asset = (
    cleaned_crypto_df.loc[cleaned_crypto_df['Price Change % (24hr)'].idxmax()])
highest_price_change_asset_name = (
    highest_price_change_asset['Asset'])
highest_price_change_percentage = (
    highest_price_change_asset['Price Change % (24hr)'])
highest_price_change_percentage_formatted = (
    f"{highest_price_change_percentage:.2f}")
total_volume_24h_usd = (
    cleaned_crypto_df['Trading Volume (24hr)'].sum())

# Section for insights
st.header("Key Insights")

st.write(f"- **Volume 24h**: Trading volume over the last 24 hours stands at **${total_volume_24h_usd:,.2f} USD**.")
st.write(f"- **% Change**: That's {'up' if cleaned_crypto_df['Volume Change % (24hr)'].iloc[0] >= 0 else 'down'} by **{abs(cleaned_crypto_df['Volume Change % (24hr)'].iloc[0]):.2f}%** compared to yesterday.")
st.write(f"- **Biggest Mover:** The asset with the highest price change in the last 24 hours is **{highest_price_change_asset_name}** with a **{abs(float(highest_price_change_percentage_formatted))}% {'increase' if float(highest_price_change_percentage_formatted) >= 0 else 'decrease'}** in price.")

st.header("Top 30 Cryptocurrencies by Market Cap")
columns_to_format = ['Price (USD)', 'Trading Volume (24hr)', 'Market Cap (USD)',
                     'Price Change % (24hr)', 'Price Change % (7d)',
                     'Volume Change % (24hr)']

# Format the selected columns to display values with 2 decimal places and
# include , to break up larger numbers into more readable format.
for column in columns_to_format:
    cleaned_crypto_df[column] = (
        cleaned_crypto_df[column].apply(lambda x: "{:,.2f}".format(x)))
st.dataframe(cleaned_crypto_df.iloc[:29])

top_10_volume_cryptos = cleaned_crypto_df.sort_values(by='Trading Volume (24hr)', ascending=True).head(10)
st.header("Most Traded Assets (Last 24hrs)")
fig1, ax1 = plt.subplots()
ax1.bar(top_10_volume_cryptos['Token Symbol'],
        top_10_volume_cryptos['Trading Volume (24hr)'])
ax1.set_xlabel('Token Symbol')
ax1.set_ylabel('Trading Volume')
st.pyplot(fig1)
