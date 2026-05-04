import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import time

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# 1. Database Connection
# Replace with your actual credentials from your .env file
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

st.set_page_config(page_title="Crypto Silver Monitor", layout="wide")

def load_data():
    query = "SELECT * FROM crypto_silver ORDER BY extracted_at DESC"
    df = pd.read_sql(query, engine)
    df['extracted_at'] = pd.to_datetime(df['extracted_at'], format='mixed')
    return df

# 2. Sidebar Filters
st.sidebar.header("Dashboard Settings ⚙️")
all_data = load_data()
coin_options = all_data['coin_name'].unique().tolist()
selected_coins = st.sidebar.multiselect("Select Coins", coin_options, default=coin_options[:2])

# 3. Main Dashboard UI
st.title("🪙 Real-Time Crypto Analytics")
st.write(f"Last updated: {time.strftime('%H:%M:%S')}")

# Filter the data based on selection
display_df = all_data[all_data['coin_name'].isin(selected_coins)]

if not display_df.empty:
    # --- TOP ROW: Metrics ---
    cols = st.columns(len(selected_coins))
    for i, coin in enumerate(selected_coins):
        coin_data = display_df[display_df['coin_name'] == coin].iloc[0] # Get latest row
        cols[i].metric(
            label=f"{coin.upper()} Price", 
            value=f"${coin_data['price']:,.2f}", 
            delta=f"{coin_data['price_diff']:,.4f} (5m)"
        )

    # --- MIDDLE ROW: Price Trends ---
    st.subheader("📈 Price History (Silver Layer)")
    fig_line = px.line(display_df, x="extracted_at", y="price", color="coin_name", template="plotly_dark")
    st.plotly_chart(fig_line, use_container_width=True)

    # --- BOTTOM ROW: Volatility ---
    st.subheader("📊 Price Change (5-Minute Intervals)")
    # Color logic for Red/Green bars
    display_df['change_type'] = display_df['price_diff'].apply(lambda x: 'Gain' if x >= 0 else 'Loss')
    fig_bar = px.bar(
        display_df, 
        x="extracted_at", 
        y="price_diff", 
        color="change_type",
        color_discrete_map={'Gain': '#00CC96', 'Loss': '#EF553B'},
        barmode="group",
        template="plotly_dark"
    )
    fig_bar.update_xaxes(type='category')
    st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.warning("Please select at least one coin to view data.")

# 4. Auto-Refresh Logic (reruns the script every 60 seconds)
time.sleep(60)
st.rerun()