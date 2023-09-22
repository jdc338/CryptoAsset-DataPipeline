"""
Crypto Asset Data Dashboard

This Streamlit application serves as a dashboard for visualizing and analyzing
cryptocurrency data. It loads cryptocurrency data using the 'datatransformation'
module, processes it, and presents key insights and visualizations.

Features:
- Displays key insights about cryptocurrency market trends.
- Presents a table of the top 30 cryptocurrencies by market capitalization.
- Visualizes the most traded assets in the last 24 hours.

Technologies Used:
- Streamlit: An open-source Python library for creating custom web apps.
- Matplotlib: Used for generating data visualizations.
- 'datatransformation' module: Handles data retrieval and cleaning.

Functions:
- 'retrieve_top_cryptos': Retrieves cryptocurrency data from an external API.
- 'clean_crypto_data': Cleans and transforms the raw data for analysis.

How to Use:
1. Run this script to launch the Streamlit app - $streamlit run interface.py
2. Explore key insights and cryptocurrency data visualizations.
"""

import matplotlib.pyplot as plt
import streamlit as st

import datatransformation

# Loads cryptocurrency data and selects the top 30
top_cryptos_data = datatransformation.retrieve_top_cryptos()
cleaned_crypto_df = datatransformation.clean_crypto_data(top_cryptos_data).head(30)

# Define some custom CSS for styling
custom_css = """
<style>

h1 {
    color: #FF5733;  /* Header text color (e.g., orange) */
    font-size: 36px;
}
h2 {
    color: #0099FF;  /* Section header text color (e.g., blue) */
    font-size: 24px;
}

</style>
"""

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Display the title using Markdown
st.markdown("# Crypto Asset Data Dashboard")

# Section for insights
st.header("Key Insights")

# Calculations for key insight metrics
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

# Displays Insights
st.write(f"- **Volume 24h**: Trading volume over the last 24 hours stands at **${total_volume_24h_usd:,.2f} USD**.")
st.write(f"- **% Change**: That's {'up' if cleaned_crypto_df['Volume Change % (24hr)'].iloc[0] >= 0 else 'down'} by **{abs(cleaned_crypto_df['Volume Change % (24hr)'].iloc[0]):.2f}%** compared to yesterday.")
st.write(f"- **Biggest Mover:** The asset with the highest price change in the last 24 hours is **{highest_price_change_asset_name}** with a **{abs(float(highest_price_change_percentage_formatted))}% {'increase' if float(highest_price_change_percentage_formatted) >= 0 else 'decrease'}** in price.")

st.header("Top 30 Cryptocurrencies by Market Cap")
columns_to_format = ['Price (USD)', 'Trading Volume (24hr)', 'Market Cap (USD)',
                     'Price Change % (24hr)', 'Price Change % (7d)',
                     'Volume Change % (24hr)']

# Formats the selected columns to display values with 2 decimal places and
# include commas to break up larger numbers into more readable format.
for column in columns_to_format:
    cleaned_crypto_df[column] = (
        cleaned_crypto_df[column].apply(lambda x: "{:,.2f}".format(x)))
st.dataframe(cleaned_crypto_df.iloc[:29])

# Displays 10 most traded assets in bar chart format
top_10_volume_cryptos = cleaned_crypto_df.sort_values(by='Trading Volume (24hr)', ascending=True).head(10)
st.header("Most Traded Assets (Last 24hrs)")
fig1, ax1 = plt.subplots()
ax1.bar(top_10_volume_cryptos['Token Symbol'],
        top_10_volume_cryptos['Trading Volume (24hr)'])
ax1.set_xlabel('Token Symbol')
ax1.set_ylabel('Trading Volume')
st.pyplot(fig1)
