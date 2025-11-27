import streamlit as st
import pandas as pd
import plotly.express as px

import time
from millify import millify

st.set_page_config(
    page_title="Future Savings Planner",
    page_icon="💰",
    layout="wide"
)

st.title("Future Savings Planner")
st.caption("Play with monthly savings, lumpsums, interest rates etc to see how your wealth can grow.")

# ---- USER INPUTS ----
with st.container():
    st.markdown("### Assumptions")
    st.write("Adjust the inputs to model your future savings")
    with st.expander("Investment Inputs", expanded=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            P = st.number_input(
                "Fixed amount to save per month", 
                value=400,
                min_value = 0,
                step=50,
                help="How much do you plan to save monthly"
                )
            L = st.number_input(
                "Lump Sum Amount", 
                min_value=0,
                step=500,
                help="Any amount you want to also add in the investment pool"
                )
        with col2:    
            r = st.number_input(
                "Annual expected interest rate (%)", 
                value=7,
                min_value = 0,
                max_value=30,
                help="Average yearly return (currently roughly 7%)"
                )
            t = st.number_input(
                "Number of years",
                value=30,
                min_value = 0,
                help="Number years you are planning to save"
                )
        with col3:
            inflation = st.number_input(
                "Annual inflationrate (%)", 
                value=2,
                min_value=0,
                max_value=15,
                help="Used to calculate inflation-adjust value (Governemnts aim for 2% p/y)"
                )

# ---- The Math -----

# cache decorator makes recalculation faster
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

# ajdust for inflation
@st.cache_data
def inflation_adjustment(total_savings: float, inflation_rate: float, t: int) -> float:
    infla_rate = inflation_rate/100
    return total_savings / ((1 + infla_rate)**t)

# ---- Calculations and Display ----
if st.button("Calculate", type="primary"):
    with st.spinner("Calculating ..."):
        time.sleep(1)
        st.success("Calculations complete!")
    df = future_value_annuity(P=P, L=L, r=r, t=t)
    if not df.empty:
        total_fv = df.loc[df.index[-1], "Total FV"]
        total_contrib = P * 12 * t + L # value without interest
        total_interest = total_fv - total_contrib
        
        adjusted_savings = inflation_adjustment(total_savings=total_fv,
                                                inflation_rate=inflation,
                                                t=t)

    # ---- Metric Values ----
        st.markdown("### Summary")
        st.caption("Key figure overview at the end of the savings term")
        with st.container():
            col_1, col_2, col_3, col_4 = st.columns(4)
            col_1.metric("Total Savings", f"€{millify(total_fv)}")
            col_2.metric("Total Contributions", f"{millify(total_contrib)}")
            col_3.metric("Total Interest Earned", f"{millify(total_interest)}")
            col_4.metric("Adjusted for Inflation", f"€{millify(adjusted_savings)}")

    # ---- Graph ----
        y_colums = ["Total FV"]
        if not (df['FV Annuity'] == 0).all():
            y_colums.append("FV Annuity")
        if not (df['FV Lump Sum'] == 0).all():
            y_colums.append("FV Lump Sum")
        
        fig_1 = px.line(
            df,
            x="Year",
            y=y_colums,
            markers=True,
            title="Savings Over Time",
            labels={
                "Year":"Year",
                "value":"Amount (€)",
                "variable": "Component"   
            })
        fig_1.update_layout(
            template="plotly_white",
            margin=dict(l=40, r=20, t=60, b=40),
            )
        
        st.plotly_chart(fig_1, use_container_width=True)