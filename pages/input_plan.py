import streamlit as st
import pandas as pd
import plotly.express as px

from millify import millify

st.title("Savings Plan")

# ---- USER INPUTS ----
col1, col2 = st.columns(2)

with col1:
    P = st.number_input("Fixed amount to save per month (EUR)", min_value = 0)
    L = st.number_input("Lump Sum Amount (EUR)", min_value=0)
with col2:    
    r = st.number_input("Annual expected interest rate", min_value = 0)
    t = st.number_input("Number of years you are planning to save", min_value = 0)

# ---- The Math -----

# cahce decorator makes recalculation faster
@st._cache_data
def future_value_annuity(P: float, L: float, r: float, t: int) -> pd.DataFrame:
    """
    Takes the user inputs and based on that and a compounding
    period of 12 (months per year) give the Future Value
    """
    # compounding perioids per year
    n = 12
    r_decimal = r/100
    values = []

    for year in range(1, t+1):
        FV = P * ((1 + r_decimal/n)**(n*year) -1) / (r_decimal/n) if r_decimal > 0 else P * n * year
        FV_L = L * (1 + r_decimal/n)**(n*year) if r_decimal > 0 else L
        total = FV + FV_L
        values.append({
            "Year":year,
            "FV Annuity": FV,
            "FV Lump Sum": FV_L,
            "Total FV": total
        })

    return pd.DataFrame(values)

# ---- Calculations and Display ----
if st.button("Calculate"):
    df = future_value_annuity(P=P, L=L, r=r, t=t)
    if not df.empty:
        total_fv = df.loc[df.index[-1], "Total FV"]
        total_contrib = P * 12 * t + L # value without interest
        total_interest = total_fv - total_contrib

    # ---- Metric Values ----
        col_1, col_2, col_3 = st.columns(3)
        col_1.metric("Total savings", f"€{millify(total_fv)}")
        col_2.metric("Total Contributions", f"{millify(total_contrib)}")
        col_3.metric("Total Interest Earned", f"{millify(total_interest)}")

    # ---- Graph ----
        fig_1 = px.line(
            df,
            x="Year",
            y=["FV Annuity", "FV Lump Sum", "Total FV"],
            markers=True,
            title="Savings Over Time")
        
        st.plotly_chart(fig_1, use_container_width=True)