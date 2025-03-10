import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

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
    hist = stock.history(period="5d")  # Last 5 days of data
    return hist


# ---- 3️⃣ Streamlit UI ----
st.title("📊 Top 10 Companies Stock Market Dashboard")

# ---- 4️⃣ Fetch Data for All Top Companies ----
all_data = []
for name, symbol in TOP_COMPANIES.items():
    try:
        data = get_stock_data(symbol)
        if not data.empty:
            latest_data = data.iloc[-1]  # Get latest day's data
            all_data.append([
                name, symbol, latest_data["Open"], latest_data["High"],
                latest_data["Low"], latest_data["Close"], latest_data["Volume"]
            ])
    except Exception as e:
        st.error(f"Error fetching {symbol}: {e}")

# ---- 5️⃣ Create DataFrame ----
columns = ["Company", "Ticker", "Open", "High", "Low", "Close", "Volume"]
df = pd.DataFrame(all_data, columns=columns)

# ---- 6️⃣ Sorting & Ranking ----
ranking_metric = st.selectbox(
    "Rank by:", ["Open", "High", "Low", "Close", "Volume"])
df_sorted = df.sort_values(
    by=ranking_metric, ascending=False).reset_index(drop=True)

# ---- 7️⃣ Display Data ----
st.dataframe(df_sorted)

# ---- 8️⃣ Plot Graph ----
fig = px.bar(df_sorted, x="Company", y=ranking_metric, color="Company",
             title=f"Top 10 Companies Ranked by {ranking_metric}")
st.plotly_chart(fig)
