import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Application", layout="wide")

st.title("📈 Stock Market Application")

# Sidebar
st.sidebar.header("Stock Settings")

ticker = st.sidebar.text_input("Stock Ticker", value="AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

ma_short = st.sidebar.slider("Short Moving Average", 5, 50, 20)
ma_long = st.sidebar.slider("Long Moving Average", 50, 200, 100)

# Fetch data
@st.cache_data
def load_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

data = load_data(ticker, start_date, end_date)

if data.empty:
    st.error("No data found. Check the ticker symbol.")
    st.stop()

# Indicators
data["MA_Short"] = data["Close"].rolling(ma_short).mean()
data["MA_Long"] = data["Close"].rolling(ma_long).mean()

# Price Chart
st.subheader(f"{ticker} Price Chart")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(data.index, data["Close"], label="Close Price", linewidth=2)
ax.plot(data.index, data["MA_Short"], label=f"MA {ma_short}")
ax.plot(data.index, data["MA_Long"], label=f"MA {ma_long}")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend()
st.pyplot(fig)

# Volume Chart
st.subheader("Volume")

fig2, ax2 = plt.subplots(figsize=(12, 3))
ax2.bar(data.index, data["Volume"], color="gray")
ax2.set_ylabel("Volume")
st.pyplot(fig2)

# Stats
st.subheader("Stock Statistics")
st.write(data.describe())
