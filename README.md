# Stock Price Prediction App



This Streamlit app predicts stock prices using historical data and displays relevant financial news and metrics. It leverages the [Yahoo Finance](https://finance.yahoo.com/) API for historical stock data, [Prophet](https://facebook.github.io/prophet/docs/quick_start.html) for forecasting, [Finnhub](https://finnhub.io/) for financial metrics, and [NewsAPI](https://newsapi.org/) for news articles.

#### Live Demo
You can see a live demo of the application [here](https://linayorda-stock-price-prediction-app-main-vyy79k.streamlit.app/).

## Features

- **Historical Data Visualization**: Displays historical stock data with candlestick charts.
- **Stock Price Prediction**: Uses the Prophet library to predict future stock prices based on historical data.
- **Financial Metrics**: Fetches and displays financial metrics using the Finnhub API.
- **Latest News**: Fetches and displays the latest news articles related to the selected stock.

## Stock Market Prediction

This application utilizes Facebook's Prophet library for stock market prediction. Prophet is a robust and flexible time series forecasting tool designed to handle various seasonal effects and support holidays and missing data. It is particularly effective for forecasting data with strong seasonal patterns and a history of observations over multiple seasons.

### How Prophet Works

Prophet models the time series data using an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. The model components are:

* Trend: Captures the long-term increase or decrease in the time series data.
* Seasonality: Accounts for periodic changes (e.g., weekly, yearly).
* Holidays: Incorporates the effects of holidays that impact the time series data.

### Using Prophet in the Application

* Data Collection: The application gathers historical stock prices using the yfinance library.
* Data Preparation: The collected data is processed and formatted to be compatible with the Prophet model. This involves creating a DataFrame with two columns: ds (date) and y (value, such as stock price).
* Model Training: The Prophet model is trained using the historical data. The model learns the trend, seasonality, and holiday effects from the data.
* Forecasting: Once trained, the model can predict future stock prices. The forecasts include both the predicted values and the uncertainty intervals.

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


