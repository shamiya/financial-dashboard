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

# ---- 2️⃣ Fetch Stock Data Function ----


@st.cache_data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")  # Fetch last 1 month of data
    return hist


# ---- 3️⃣ Streamlit UI ----
st.title("📊 Top 10 Companies Stock Market Dashboard with Candlestick Chart")

# Select a company from dropdown
selected_company = st.selectbox(
    "Select a company:", list(TOP_COMPANIES.keys()))
ticker_symbol = TOP_COMPANIES[selected_company]

# Fetch data for selected stock
historical_data = get_stock_data(ticker_symbol)

# ---- 4️⃣ Display Candlestick Chart ----
if not historical_data.empty:
    st.subheader(f"Candlestick Chart for {selected_company} ({ticker_symbol})")

    fig = go.Figure(data=[go.Candlestick(
        x=historical_data.index,
        open=historical_data["Open"],
        high=historical_data["High"],
        low=historical_data["Low"],
        close=historical_data["Close"],
        increasing_line_color="green",  # Bullish (price went up)
        decreasing_line_color="red"     # Bearish (price went down)
    )])

    fig.update_layout(
        title=f"{selected_company} Stock Price (Last Month)",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig)

    # ---- 5️⃣ Explanation Note ----
    st.markdown("""
    ### 📌 How to Read the Candlestick Chart:
    - The **body** of each candle represents the difference between **open & close** prices.
    - **Green (Bullish)** → The stock closed **higher** than it opened.
    - **Red (Bearish)** → The stock closed **lower** than it opened.
    - The **wicks (shadows)** show the **highest & lowest** prices of the day.
    - Mastering this chart type helps in identifying **trading patterns & trends**.
    """)

    # ---- 6️⃣ Show Table of Stock Data ----
    st.subheader("📊 Stock Data Table (Last Month)")
    st.dataframe(
        historical_data[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index())

else:
    st.warning("No data available for the selected company.")
