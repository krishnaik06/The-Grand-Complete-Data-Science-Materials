import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.title("Stock Market Dashboard")
tickers = ('TSLA', 'AAP', 'MSFT', 'BTC-USD', 'ETH-USD', 'GOOGL', 'AMZN', 'AAPL', 'NFLX', 'NVDA')

# Sidebar for user input
st.sidebar.header("Settings")
dropdown = st.sidebar.multiselect('Pick your assets', tickers, default=['GOOGL'])  # Set GOOGL as the default asset
start = st.sidebar.date_input('Start date', value=pd.to_datetime('2023-01-01'))
end = st.sidebar.date_input('End date', value=pd.to_datetime('today'))

# Fetch and display data
if len(dropdown) > 0:
    df = yf.download(dropdown, start=start, end=end)['Adj Close']
    df_candle = yf.download(dropdown, start=start, end=end)

    # Display cumulative returns line chart
    st.header('{}'.format(dropdown))
    st.line_chart(df.pct_change().cumsum())

    # Display raw data in a table
    st.write("Raw Data:")
    st.dataframe(df)

    # Display descriptive statistics
    st.write("Descriptive Statistics:")
    st.write(df.describe())

    # Add a download button for CSV
    csv_export_button = st.button("Export Data to CSV")
    if csv_export_button:
        df.to_csv('cumulative_returns_data.csv', index=False)
        st.success("Data exported to 'cumulative_returns_data.csv'")

    # Add informative text
    st.markdown("""
    * Cumulative Return: The cumulative return is calculated based on the percentage change in the adjusted close prices.
    """)

    # Plot candlestick chart at the bottom
    fig = go.Figure(data=[go.Candlestick(x=df_candle.index,
                                         open=df_candle['Open'],
                                         high=df_candle['High'],
                                         low=df_candle['Low'],
                                         close=df_candle['Close'])])
    st.plotly_chart(fig, use_container_width=True)
