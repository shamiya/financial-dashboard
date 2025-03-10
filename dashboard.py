import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# ---- 1️⃣ Define List of Top Companies ----
TOP_COMPANIES = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "NVIDIA (NVDA)": "NVDA",
    "Alphabet (GOOG)": "GOOG",
    "Amazon (AMZN)": "AMZN",
    "Meta (META)": "META",
    "Tesla (TSLA)": "TSLA",
    "Berkshire Hathaway (BRK-B)": "BRK-B",
    "UnitedHealth (UNH)": "UNH",
    "Johnson & Johnson (JNJ)": "JNJ"
}

# ---- 2️⃣ Function to Fetch Stock Data ----


@st.cache_data
def get_stock_data(ticker, period="1mo"):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

# ---- 3️⃣ Function to Fetch Real-Time Data ----


def get_realtime_data(ticker):
    stock = yf.Ticker(ticker)
    latest_data = stock.history(period="1d")  # Get today's data
    return latest_data


# ---- 4️⃣ Streamlit UI ----
st.title("📊 Top 10 Companies Stock Market Dashboard with Candlestick Chart")

# 🎯 **Green Button for Real-Time Data**
col1, col2 = st.columns([0.8, 0.2])  # Layout
with col2:
    if st.button("⚡ Real-Time Data", key="real_time", help="Click to fetch latest stock data", use_container_width=True):
        realtime = True
    else:
        realtime = False

# Select a company from dropdown
selected_company = st.selectbox(
    "Select a company:", list(TOP_COMPANIES.keys()))
ticker_symbol = TOP_COMPANIES[selected_company]

# Fetch Data (Real-Time if Button Clicked)
if realtime:
    historical_data = get_realtime_data(ticker_symbol)
    st.success("✅ Showing Real-Time Data")
else:
    historical_data = get_stock_data(ticker_symbol)
    st.info("📅 Showing Last Month's Data")

# ---- 5️⃣ Display Candlestick Chart ----
if not historical_data.empty:
    st.subheader(f"Candlestick Chart for {selected_company} ({ticker_symbol})")

    fig = go.Figure(data=[go.Candlestick(
        x=historical_data.index,
        open=historical_data["Open"],
        high=historical_data["High"],
        low=historical_data["Low"],
        close=historical_data["Close"],
        increasing_line_color="green",
        decreasing_line_color="red"
    )])

    fig.update_layout(
        title=f"{selected_company} Stock Price ({'Real-Time' if realtime else 'Last Month'})",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig)

    # ---- 6️⃣ Explanation Note ----
    st.markdown("""
    ### 📌 How to Read the Candlestick Chart:
    - **Body** → Difference between **Open & Close** prices.
    - **Green (Bullish)** → Closed **higher** than it opened.
    - **Red (Bearish)** → Closed **lower** than it opened.
    - **Wicks (shadows)** show **high & low** extremes.
    - Understanding this chart helps in **trading pattern recognition**.
    """)

    # ---- 7️⃣ Show Table of Stock Data ----
    st.subheader(
        f"📊 Stock Data Table ({'Real-Time' if realtime else 'Last Month'})")
    st.dataframe(
        historical_data[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index())

else:
    st.warning("No data available for the selected company.")
