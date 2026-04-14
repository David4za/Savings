import streamlit as st
import pandas as pd
import plotly.express as px

from millify import millify

st.title("Withdraw Plan")

col1, col2, col3 = st.columns(3)

with col1:
    withdraw = st.number_input("Monthly withdrawal amount", value=2000, min_value=0)
    FV = st.number_input("Total Savings", value=500000, min_value=0)
with col2:
    r = st.number_input("Annual expected interest rate (%)", value=2, min_value = 0)
with col3:
    inflation = st.number_input("Annual inflation rate (%)", value=2,  min_value= 0)

@st.cache_data
def withdraw_analysis(monthly_withdraw: float,
                       total_savings: float, 
                       interest: float,
                       inflation: float):
    
    r_decimal = interest/100
    inflation_dec = inflation/100
    monthly_interest = (1 + r_decimal) ** (1/12) - 1
    balance = total_savings
    months = 0
    total_withdrawn = 0
    balances = []

    if monthly_withdraw <= 0 or total_savings <= 0:
        return pd.DataFrame(columns=[
            "Year",
            "Balance",
            "Adjusted Balance",
            "Month",
            "Total Withdrawn"
        ])

    while balance > 0:
        if months >= 1200:
            break

        withdrawal_amount = min(monthly_withdraw, balance)
        balance -= withdrawal_amount
        total_withdrawn += withdrawal_amount
        balance *= 1 + monthly_interest
        months += 1

        balances.append({
            "Month": months,
            "Year": (months - 1) // 12 + 1,
            "Balance": balance,
            "Adjusted Balance": balance / (1 + inflation_dec) ** (months / 12),
            "Total Withdrawn": total_withdrawn
        })

    df = pd.DataFrame(balances)
    df = df.groupby('Year').agg({
        'Balance':'last',
        'Adjusted Balance':'last',
        'Month':'last',
        'Total Withdrawn':'last'
    }).reset_index()

    return df

# ---------- Page -----------
if st.button("Calculate"):
    df = withdraw_analysis(monthly_withdraw=withdraw,
                           total_savings=FV,
                           interest=r,
                           inflation=inflation)
    
    if not df.empty:
        total_months = df.loc[df.index[-1], "Month"]
        total_years = total_months / 12
        total_withdraw = df.loc[df.index[-1], "Total Withdrawn"]

        col_1, col_2 = st.columns(2)
        
        col_1.metric("Total Years", f"{total_years:.1f}")
        col_2.metric("Total Withdrawn", f"{millify(total_withdraw)}")

        fig_1 = px.line(
            df,
            x = "Year",
            y = ["Balance", "Adjusted Balance"],
            markers=True,
            title="Balance by Year",
            color_discrete_sequence = ["#00BB88", "#FF0000"]
        )

        st.plotly_chart(fig_1, use_container_width=True)
