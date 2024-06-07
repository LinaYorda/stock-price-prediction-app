import streamlit as st
import pandas as pd
from textblob import TextBlob
from newsapi import NewsApiClient
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

def get_news(ticker, max_articles=20):
    newsapi = NewsApiClient(api_key=os.getenv("NEWSAPI_KEY"))
    try:
        news = newsapi.get_everything(q=ticker, language='en', sort_by='relevancy', page=1)
        if news['status'] == 'ok':
            return news['articles'][:max_articles]
        else:
            st.error(f"Error fetching news: {news.get('message', 'Unknown error')}")
            return []
    except Exception as e:
        st.error(f"Failed to fetch news: {e}")
        return []

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "Positive", polarity
    elif polarity < 0:
        return "Negative", polarity
    else:
        return "Neutral", polarity

def sentiment_analysis(articles):
    sentiment_results = []
    for article in articles:
        description = article.get('description')
        if description:
            sentiment, polarity = analyze_sentiment(description)
            sentiment_results.append((sentiment, polarity, article))
    return sentiment_results

def show_sentiment_analysis_page():
    st.title("Sentiment Analysis")
    st.sidebar.header("User Input")
    ticker = st.sidebar.text_input("Enter the ticker:", "DOW")

    if ticker:
        articles = get_news(ticker, max_articles=20)
        if articles:
            st.subheader(f"Recent News for {ticker}")
            sentiment_results = sentiment_analysis(articles)
            if sentiment_results:
                for sentiment, polarity, article in sentiment_results:
                    title = article.get('title', 'No title available')
                    description = article.get('description', 'No description available')
                    url = article.get('url', '#')
                    st.write(f"### {title}")
                    st.write(description)
                    st.write(f"Sentiment: **{sentiment}** (Polarity: {polarity:.2f})")
                    st.write(f"[Read more]({url})")
                    st.write('---')
                avg_polarity = sum(p[1] for p in sentiment_results) / len(sentiment_results)
                st.write(f"Overall Sentiment for {ticker} is {'Positive' if avg_polarity > 0 else 'Negative' if avg_polarity < 0 else 'Neutral'} (Average Polarity: {avg_polarity:.2f})")
            else:
                st.write("No valid descriptions available for sentiment analysis.")
        else:
            st.error("No news found for the ticker")
    else:
        st.warning("Please enter a ticker")

if __name__ == "__main__":
    show_sentiment_analysis_page()