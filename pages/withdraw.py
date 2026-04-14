import streamlit as st

from millify import millify

from pages.calculations.withdrawals import withdraw_analysis
from pages.charts.withdrawal_charts import balance_by_year_chart

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
def cached_withdraw_analysis(
    monthly_withdraw: float,
    total_savings: float,
    interest: float,
    inflation: float,
):
    return withdraw_analysis(
        monthly_withdraw=monthly_withdraw,
        total_savings=total_savings,
        interest=interest,
        inflation=inflation,
    )

# ---------- Page -----------
if st.button("Calculate"):
    df = cached_withdraw_analysis(
        monthly_withdraw=withdraw,
        total_savings=FV,
        interest=r,
        inflation=inflation,
    )
    
    if not df.empty:
        total_months = df.loc[df.index[-1], "Month"]
        total_years = total_months / 12
        total_withdraw = df.loc[df.index[-1], "Total Withdrawn"]

        col_1, col_2 = st.columns(2)
        
        col_1.metric("Total Years", f"{total_years:.1f}")
        col_2.metric("Total Withdrawn", f"{millify(total_withdraw)}")

        fig_1 = balance_by_year_chart(df)
        st.plotly_chart(fig_1, use_container_width=True)
