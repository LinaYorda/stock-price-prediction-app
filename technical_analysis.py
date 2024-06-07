import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def calculate_technical_indicators(data):
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
    data['RSI'] = calculate_rsi(data['Close'], 14)
    data['MACD'], data['Signal'] = calculate_macd(data['Close'])
    data['Upper Band'], data['Lower Band'] = calculate_bollinger_bands(data['Close'])
    return data

def calculate_rsi(series, period):
    delta = series.diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_macd(series, fast_period=12, slow_period=26, signal_period=9):
    fast_ema = series.ewm(span=fast_period, adjust=False).mean()
    slow_ema = series.ewm(span=slow_period, adjust=False).mean()
    macd = fast_ema - slow_ema
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    return macd, signal

def calculate_bollinger_bands(series, window=20, num_std_dev=2):
    sma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    upper_band = sma + (std * num_std_dev)
    lower_band = sma - (std * num_std_dev)
    return upper_band, lower_band

def show_technical_analysis_page():
    st.title("Technical Analysis")
    st.sidebar.header("User Input")
    
    ticker = st.sidebar.text_input("Enter the ticker:", "AAPL")
    start_date = st.sidebar.date_input("Start Date", datetime(2020, 1, 1))
    end_date = st.sidebar.date_input("End Date", datetime.now())
    
    if ticker:
        data = yf.download(ticker, start=start_date, end=end_date)
        if not data.empty:
            data = calculate_technical_indicators(data)
            
            st.subheader(f"{ticker} Stock Price and Technical Indicators")
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'],
                                         name='Candlestick'))
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], line=dict(color='blue', width=1), name='SMA 20'))
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], line=dict(color='orange', width=1), name='SMA 50'))
            fig.add_trace(go.Scatter(x=data.index, y=data['EMA_20'], line=dict(color='red', width=1), name='EMA 20'))
            fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], line=dict(color='purple', width=1), name='RSI'))
            fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], line=dict(color='green', width=1), name='MACD'))
            fig.add_trace(go.Scatter(x=data.index, y=data['Signal'], line=dict(color='magenta', width=1), name='Signal'))
            fig.add_trace(go.Scatter(x=data.index, y=data['Upper Band'], line=dict(color='grey', width=1), name='Upper Band'))
            fig.add_trace(go.Scatter(x=data.index, y=data['Lower Band'], line=dict(color='grey', width=1), name='Lower Band'))
            
            fig.update_layout(
                title=f'{ticker} Stock Price and Technical Indicators', 
                xaxis_title='Date', 
                yaxis_title='Price',
                width=1000,  # Adjust the width here
                height=700  # Adjust the height here
            )
            st.plotly_chart(fig)
        else:
            st.error("No data found for the given ticker symbol.")
    else:
        st.warning("Please enter a ticker symbol.")

if __name__ == "__main__":
    show_technical_analysis_page()

