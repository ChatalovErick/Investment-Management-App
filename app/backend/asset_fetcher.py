import pandas as pd
import streamlit as st
import finnhub
import requests

# -----------------------------
# Finnhub client (for stocks)
# -----------------------------

api_key = "d6s4hlpr01qrb5i8jupgd6s4hlpr01qrb5i8juq0"
client = finnhub.Client(api_key=api_key)

# -----------------------------
# Price functions
# -----------------------------
@st.cache_data(ttl=900)
def get_stock_price(ticker):
    try:
        q = client.quote(ticker)
        return q["c"]
    except:
        return None
    
@st.cache_data(ttl=900)
def get_crypto_price(ticker):
    try:
        symbol = f"{ticker.upper()}USDT"
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        data = requests.get(url).json()
        return float(data["price"])
    except:
        return None

# -----------------------------
# Unified price function
# -----------------------------

@st.cache_data(ttl=900)
def get_current_price(asset_type, ticker):
    asset_type = asset_type.lower()

    if asset_type == "stock":
        return get_stock_price(ticker)

    if asset_type == "crypto":
        return get_crypto_price(ticker)

    return None
