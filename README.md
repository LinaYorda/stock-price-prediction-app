# Stock Price Prediction App

This Streamlit app predicts stock prices using historical data and displays relevant financial news and metrics. It leverages the Yahoo Finance API for historical stock data, Prophet for forecasting, Finnhub for financial metrics, and NewsAPI for news articles.

## Features

- **Historical Data Visualization**: Displays historical stock data with candlestick charts.
- **Stock Price Prediction**: Uses the Prophet library to predict future stock prices based on historical data.
- **Financial Metrics**: Fetches and displays financial metrics using the Finnhub API.
- **Latest News**: Fetches and displays the latest news articles related to the selected stock.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/stock-price-prediction-app.git
   cd stock-price-prediction-app
   ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```


3. **Run the application locally**

    ```bash
    streamlit run main.py
    ```


## Disclaimer

The information provided on this app is for informational purposes only and should not be construed as financial advice. The financial news and data displayed are based on publicly available sources and may not be accurate or up-to-date. Users should independently verify any information before making any investment decisions. The app developers are not responsible for any financial losses incurred based on the information provided.



### Acknowledgments

Thanks to Yahoo Finance for providing the stock data.
Thanks to Finnhub for providing financial metrics.
Thanks to NewsAPI for providing news articles.
Thanks to Prophet for the forecasting tool.
