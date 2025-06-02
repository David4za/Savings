import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

from millify import millify

st.title("Withdraw Plan")

col1, col2, col3 = st.columns(3)

with col1:
    withdraw = st.number_input("Monthly withdrawl amount", value=2000, min_value=0)
    FV = st.number_input("Total Savings", value=500000, min_value=0)
with col2:
    r = st.number_input("Annual expected interest rate", value=2, min_value = 0)
with col3:
    inflation = st.number_input("Annual inflationrate", value=2,  min_value= 1)

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
    balances = []


    while balance >= monthly_withdraw:
        if months >= 900:
            break
        else:
                
            balance = balance - monthly_withdraw
            balance = balance * (1 + monthly_interest)
            months +=1
            balances.append({
                "Month": months,
                "Balance":balance})

        df = pd.DataFrame(balances)
        df['Year'] = np.floor(df['Month'] / 12).astype(int) + 1
        df = df.groupby('Year').agg({'Balance':'last'}).reset_index()
    #adjusted_balance = [b / ((1 + inflation_dec) ** (month/12)) for month, b in enumerate(balances)]

    return df

# ---------- Page -----------
if st.button("Calculate"):
    df = withdraw_analysis(monthly_withdraw=withdraw,
                           total_savings=FV,
                           interest=r,
                           inflation=inflation)
    
    if not df.empty:
        total_years = df.loc[df.index[-1], "Year"]
        total_withdraw = (withdraw * total_years) * 12

        col_1, col_2 = st.columns(2)
        
        col_1.metric("Total Years", f"{millify(total_years)}")
        col_2.metric("Total Withdrawn", f"{millify(total_withdraw)}")

        fig_1 = px.line(
            df,
            x = "Year",
            y = "Balance",
            markers=True,
            title="Balance by Year"
        )

        st.plotly_chart(fig_1, use_container_width=True)