# CryptoAsset-DataPipeline

## Objective

The objective of this cryptocurrency data analysis platform is to gather, clean, and analyze real-time data for the top 1000 cryptocurrencies by market capitalization using the CoinMarketCap API. The project aims to provide valuable insights into cryptocurrency market trends, including price fluctuations, trading volume, and price change percentages over various timeframes. By storing the cleaned data in an SQLite database, the project enables efficient data retrieval and empowers users to interact with the data through an intuitive Streamlit web interface. This project ultimately seeks to facilitate data-driven decision-making in the cryptocurrency space and enhance the understanding of cryptocurrency market dynamics.

## Technologies Used
- [CoinMarketCap API](https://coinmarketcap.com/api/documentation/v1/)
- [Streamlit](https://streamlit.io/)
- [Matplotlib](https://matplotlib.org/stable/users/index.html)

### CoinMarketCap API
The CoinMarketCap API is used to retrieve data for the top 1000 cryptocurrencies by market capitalization, providing various metrics such as price and trading volume.

- [CoinMarketCap API](https://coinmarketcap.com/api/documentation/v1/)

### Streamlit
Streamlit is used to create an interactive web interface for querying the cryptocurrency data and displaying insights.

- [Streamlit Website](https://www.streamlit.io/)

### Matplotlib
Matplotlib is used for creating data visualizations, including bar charts for cryptocurrency trading volume.

- [Matplotlib](https://matplotlib.org/stable/users/index.html)

## Setup

### Prerequisites

1. Python 3.x
2. Pip

### Installation

1. Clone the repository.

    ```bash
    git clone git@github.com:jdc338/CryptoAsset-DataPipeline.git
    ```

2. Navigate into the directory.

    ```bash
    cd CryptoAsset-DataPipeline
    ```

3. Setting Up a Virtual Environment.

    To isolate the project dependencies, it's recommended to create a virtual environment.
    Run the following commands in your terminal to create and activate a virtual environment:

    **On macOS and Linux:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    **On Windows:**

    ```bash
    python -m venv venv
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\venv\Scripts\activate
    ```

4. Install the required packages.

    ```bash
    pip install -r requirements.txt
    ```

### API Keys

1. You'll need an API key from CoinMarket Cap.
2. Create a file named `env.py` in the project root directory.
3. Store your API keys in `env.py` as environment variables. For example:

    ```python
    os.environ.setdefault("CMC_API_KEY", "YOUR_API_KEY")
    ```

## Usage
1. **User Interaction**

    ```bash
    streamlit run interface.py
    ```

## Minimal Viable Product (MVP)

1. Evidence that appropriate and justified tools were used to extract the data.
2. Evidence that data is cleaned and transformed to the desired format.
3. Evidence of appropriate data handling practices
4. Data storage facility chosen, facilitated and justified.
5. Code is well-organised and easy to read.
6. Clear documentation of each step.

## Contributors

- James Corfe [@jdc338](https://github.com/jdc338)


**I hope you enjoy the dashboard!**
