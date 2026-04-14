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
st.caption("Play with monthly savings, lump sums, interest rates etc to see how your wealth can grow.")

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
        st.markdown("#### Lump sums")
        st.caption("Add optional one-off deposits. A lump sum added after 20 years in a 30-year plan grows for the final 10 years.")
        lump_sum_count = st.number_input(
            "Number of lump sums",
            value=1,
            min_value=0,
            max_value=20,
            step=1,
            help="Set this to 0 if you do not plan any one-off deposits.",
        )
        lump_sums = []

        for lump_sum_index in range(lump_sum_count):
            amount_col, year_col = st.columns(2)
            with amount_col:
                lump_sum_amount = st.number_input(
                    f"Lump sum {lump_sum_index + 1} amount",
                    min_value=0,
                    step=500,
                    key=f"lump_sum_amount_{lump_sum_index}",
                )
            with year_col:
                years_from_now = st.number_input(
                    f"Add after year",
                    min_value=0,
                    max_value=t,
                    step=1,
                    key=f"lump_sum_year_{lump_sum_index}",
                    help="Use 0 if this amount is invested today.",
                )
            if lump_sum_amount > 0:
                lump_sums.append((float(lump_sum_amount), int(years_from_now)))

# ---- The Math -----

def effective_monthly_rate(annual_rate: float) -> float:
    """Convert an effective annual return into an equivalent monthly return."""
    return (1 + annual_rate / 100) ** (1 / 12) - 1


# cache decorator makes recalculation faster
@st.cache_data
def future_value_annuity(
    P: float,
    lump_sums: tuple[tuple[float, int], ...],
    r: float,
    t: int
) -> pd.DataFrame:
    """
    Takes the user inputs and returns future value by year.

    Assumes the annual rate is an effective annual return, lump sums are
    invested at their chosen year, and fixed monthly savings are added at
    month-end.
    """
    periods_per_year = 12
    monthly_rate = effective_monthly_rate(r)
    values = []

    for year in range(1, t+1):
        periods = periods_per_year * year
        FV = (
            P * ((1 + monthly_rate) ** periods - 1) / monthly_rate
            if monthly_rate > 0
            else P * periods
        )
        FV_L = 0
        for amount, years_from_now in lump_sums:
            lump_sum_periods = periods - years_from_now * periods_per_year
            if lump_sum_periods < 0:
                continue
            FV_L += (
                amount * (1 + monthly_rate) ** lump_sum_periods
                if monthly_rate > 0
                else amount
            )
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
    lump_sums_for_calculation = tuple(lump_sums)
    df = future_value_annuity(P=P, lump_sums=lump_sums_for_calculation, r=r, t=t)
    if not df.empty:
        total_fv = df.loc[df.index[-1], "Total FV"]
        total_lump_sum_contrib = sum(amount for amount, _ in lump_sums_for_calculation)
        total_contrib = P * 12 * t + total_lump_sum_contrib # value without interest
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
