import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from prophet import Prophet
import plotly.graph_objects as go
import requests
import finnhub
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv

load_dotenv()


st.title("Stock Price App - Forecasting and News")
st.write("The information provided on this app is for informational purposes only and should not be construed as financial advice.")

# Sidebar for user inputs
st.sidebar.header("Selected Period")
start_date = st.sidebar.date_input("From:", datetime(2000, 1, 1))
end_date = st.sidebar.date_input("To:", datetime(2021, 12, 31))

st.sidebar.header("Selected Ticker")
ticker = st.sidebar.text_input("Enter the ticker:", 'DOW')

st.sidebar.header("Prediction Years")
prediction_years = st.sidebar.slider("Years of Prediction:", 1, 10, 1)

finnhub_api_key = "cpg0cn1r01ql1vn3f1ngcpg0cn1r01ql1vn3f1o0"
finnhub_client = finnhub.Client(api_key=finnhub_api_key)


@st.cache_data
def load_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            st.error(f"No data found for ticker {ticker}. Are you sure this is the ticker symbol?")
            return None
        data.reset_index(inplace=True)
        return data
    except Exception as e:
        st.error(f"Failed to download data for ticker {ticker}: {e}")
        return None



def fetch_basic_financials(ticker):
    finnhub_api_key = os.getenv("FINNHUB_API_KEY")
    finnhub_client = finnhub.Client(api_key=finnhub_api_key)
    try:
        financials = finnhub_client.company_basic_financials(ticker, 'all')
        return financials
    except Exception as e:
        st.error(f"Failed to fetch basic financials for ticker {ticker}: {e}")
        return None

def fetch_news(ticker):
    news_api_key = os.getenv("NEWSAPI_KEY")  
    newsapi = NewsApiClient(api_key=news_api_key)
    from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    to_date = datetime.now().strftime('%Y-%m-%d')
    try:
        all_articles = newsapi.get_everything(q=ticker,
                                              from_param=from_date,
                                              to=to_date,
                                              language='en',
                                              sort_by='relevancy',
                                              page=1)
        if all_articles['status'] == 'ok':
            return all_articles['articles']
        else:
            st.error(f"Failed to fetch news: {all_articles}")
            return None
    except Exception as e:
        st.error(f"Failed to fetch news: {e}")
        return None

st.markdown(
    """
    <style>
    .large-table-container {
        width: 90%;
        overflow-x: auto;
    }
    table {
        width: 90%;
        border-collapse: collapse;
    }
    th, td {
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    th {
        background-color: #f2f2f2;
    }
    </style>
    """,
    unsafe_allow_html=True
)


if ticker:
    data = load_data(ticker, start_date, end_date)
    if data is not None:
        st.write(f"## {ticker} Historical Data")
        fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                                             open=data['Open'],
                                             high=data['High'],
                                             low=data['Low'],
                                             close=data['Close'])])
        fig.update_layout(title=f'{ticker} Stock Price', xaxis_title='Date', yaxis_title='Price')
        st.plotly_chart(fig)
        df = data[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})

        if len(df) < 2 or df['y'].isna().sum() > 0:
            st.error("Not enough data available to fit the model. Please choose a different date range or ticker.")
        else:
            # Initiating the model and fitting the data
            model = Prophet()
            model.fit(df)
            future = model.make_future_dataframe(periods=365 * prediction_years)
            forecast = model.predict(future)

            st.write(f"## {ticker} Forecast Data")
            fig1 = model.plot(forecast)
            st.pyplot(fig1)
            fig2 = model.plot_components(forecast)
            st.pyplot(fig2)


        st.write(f"## {ticker} Finnhub Data Fundamentals")
        basic_financials = fetch_basic_financials(ticker)
        if basic_financials:
            metrics = basic_financials.get("metric", {})
            if metrics:
                financials_data = {key: str(value) for key, value in metrics.items()}
                financials_df = pd.DataFrame(list(financials_data.items()), columns=['Metric', 'Value'])
                st.write('<div class="large-table-container">', unsafe_allow_html=True)
                st.write(financials_df.to_html(index=False), unsafe_allow_html=True)
                st.write('</div>', unsafe_allow_html=True)
            else:
                st.write("No data available.")

        st.write(f"## {ticker} News")
        news_articles = fetch_news(ticker)
        if news_articles:
            for article in news_articles[:5]:
                st.write(f"### {article['title']}")
                st.write(f"Published at: {article['publishedAt']}")
                st.write(f"{article['description']}")
                st.write(f"[Read more]({article['url']})")
                st.write("---")

    else:
        st.error("Failed to load data. Please check the ticker symbol and try again.")
else:
    st.write("Enter a valid ticker symbol to see the data.")

