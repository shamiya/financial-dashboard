import streamlit as st
import yfinance as yf
import plotly.express as px

# ---- 1️⃣ Fetch Stock Data Function ----


@st.cache_data
def get_stock_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    historical_data = ticker.history(period="1y")
    financials = ticker.financials
    actions = ticker.actions
    return historical_data, financials, actions


# ---- 2️⃣ Streamlit UI ----
st.title("📈 Stock Market Dashboard")

# Select stock from dropdown
stock_options = {"Apple (AAPL)": "AAPL", "Microsoft (MSFT)": "MSFT"}
selected_stock = st.selectbox("Select a company:", list(stock_options.keys()))

# Fetch data for selected stock
ticker_symbol = stock_options[selected_stock]
historical_data, financials, actions = get_stock_data(ticker_symbol)

# ---- 3️⃣ Stock Price Chart ----
st.subheader(f"{selected_stock} Stock Price (Last Year)")
fig = px.line(historical_data, x=historical_data.index,
              y="Close", title=f"{ticker_symbol} Closing Prices")
st.plotly_chart(fig)

# ---- 4️⃣ Financials Table ----
st.subheader(f"{selected_stock} Financials")
st.write(financials if not financials.empty else "No financial data available.")

# ---- 5️⃣ Stock Actions (Dividends & Splits) ----
st.subheader(f"{selected_stock} Dividends & Splits")
st.write(actions if not actions.empty else "No dividend or stock split data available.")
