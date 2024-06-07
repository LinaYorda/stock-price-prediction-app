import streamlit as st
from sentiment_analysis import show_sentiment_analysis_page
from main import show_main_page, show_stock_prediction_page
from technical_analysis import show_technical_analysis_page

def main():
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Go to", ["Home", "News Sentiment Analysis", "Technical Analysis"])

    if page == "Home":
        show_main_page()
    elif page == "News Sentiment Analysis":
        show_sentiment_analysis_page()
    elif page == "Technical Analysis":
        show_technical_analysis_page()
        

if __name__ == "__main__":
    main()