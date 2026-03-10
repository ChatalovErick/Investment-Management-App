import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")

with st.container(border=True):
    st.title("Welcome to your Investment App")

    st.write("""
             
    This is your dashboard. 
              
    Use the sidebar to navigate to different sections of the app.
             
    """)

# -----------------------------------------------------------
# Load data
# -----------------------------------------------------------
df = pd.read_csv("data/investments.csv")
df["total_value"] = df["price"] * df["quantity"]

# -----------------------------------------------------------
# Summary metrics (Profit Margin + Total Balance)
# -----------------------------------------------------------

# Example calculations — adjust to your real logic
total_balance = df["total_value"].sum()

# If you have a "buy_price" column, you can compute profit
if "buy_price" in df.columns:
    df["initial_value"] = df["buy_price"] * df["quantity"]
    profit = total_balance - df["initial_value"].sum()
    profit_margin = (profit / df["initial_value"].sum()) * 100
else:
    profit_margin = 0

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.metric("Profit Margin", f"{profit_margin:.2f}%")

with col2:
    with st.container(border=True):
        st.metric("Total Balance", f"${total_balance:,.2f}")


# -----------------------------------------------------------
# Pie chart: Portfolio allocation
# -----------------------------------------------------------

with st.container(border=True):
    st.subheader("Portfolio Allocation")

    grouped = df.groupby("asset")["total_value"].sum().reset_index()

    pie_chart = (
        alt.Chart(grouped)
        .mark_arc()
        .encode(
            theta="total_value",
            color="asset",
            tooltip=["asset", "total_value"]
        )
    )

    st.altair_chart(pie_chart, use_container_width=True)
