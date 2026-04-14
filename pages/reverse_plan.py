import streamlit as st

from pages.calculations.reverse_savings import reverse_engineer_fixed_amount

st.title("Reverse Engineer Savings")

# ---- USER INPUTS ----
col1, col2, col3 = st.columns(3)

with col1:
    FV = st.number_input("Desired total amount", value=650000, min_value = 0)
with col2:    
    r = st.number_input("Annual expected interest rate (%)", value=5, min_value = 0)
with col3:
    t = st.number_input("Number of years to save", value=30,  min_value = 0)

@st.cache_data
def cached_reverse_engineer_fixed_amount(
    future_value: float,
    annual_rate: float,
    years: int,
) -> float:
    return reverse_engineer_fixed_amount(
        future_value=future_value,
        annual_rate=annual_rate,
        years=years,
    )

if st.button("Analyse"):
    if t:
        P = cached_reverse_engineer_fixed_amount(
            future_value=FV,
            annual_rate=r,
            years=t,
        )

        # need to use index because technically, st.columns
        # returns a list
        col1 = st.columns(1)[0]
        col1.metric("Fixed Monthly Amount Needed", f"€{P:.2f}")
    
