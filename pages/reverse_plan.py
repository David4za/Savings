import streamlit as st

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
def reverse_engineer_fixed_amount(FV: float, r: float, t: int) -> float:

    periods = 12 * t
    monthly_rate = (1 + r / 100) ** (1 / 12) - 1

    if FV <= 0 or periods <= 0:
        return 0
    if monthly_rate == 0:
        return FV / periods
    return (FV * monthly_rate) / ((1 + monthly_rate) ** periods - 1)

if st.button("Analyse"):
    if t:
        P = reverse_engineer_fixed_amount(FV=FV, r=r, t=t)

        # need to use index because technically, st.columns
        # returns a list
        col1 = st.columns(1)[0]
        col1.metric("Fixed Monthly Amount Needed", f"€{P:.2f}")
    
