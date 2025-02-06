# Stock Market Dashboard

This is a Streamlit dashboard designed to visualize cumulative returns of stock or cryptocurrency assets over a specified time period. It also includes a candlestick chart using Plotly for a more detailed view of stock prices.

## Features

- **Interactive Cumulative Returns Chart**: Plot the cumulative returns of selected assets.
- **User Input**: Select assets, start date, and end date from the sidebar.
- **Data Table**: View the raw data in a table format.
- **Descriptive Statistics**: Display descriptive statistics for cumulative returns.
- **CSV Export**: Export the data to a CSV file for further analysis.
- **Candlestick Chart**: View stock prices with a candlestick chart for in-depth analysis.

## How to Run

1. Run the Streamlit app:
   streamlit run main.py
2. Open the provided URL in your web browser.
3. Use the sidebar to select assets, set the date range, and explore the dashboard.

## Default Asset

The default asset is set to Google (GOOGL). To change this, modify the default parameter in the multiselect function in the sidebar

Candlestick Chart
The app includes a candlestick chart for detailed analysis of stock prices. Users can toggle between the cumulative returns and the candlestick chart for selected assets.

## Dependencies
Streamlit

yfinance

Pandas

Matplotlib

Plotly

## Result


![Screenshot (293)](https://github.com/YugantGotmare/Stock_Market_Dashboard/assets/101650315/0548282e-e920-4f62-b68c-5a6e45455807)


![Screenshot (294)](https://github.com/YugantGotmare/Stock_Market_Dashboard/assets/101650315/38e4070f-26f2-47d8-bf7d-cc898d2db7f4)
