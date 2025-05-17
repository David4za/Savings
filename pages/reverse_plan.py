import streamlit as st

st.title("Reverse Engineering our Savings")

# ---- USER INPUTS ----
col1, col2 = st.columns(2)

with col1:
    FV = st.number_input("Desired amount (EUR)", min_value = 0)
with col2:    
    r = st.number_input("Annual expected interest rate", min_value = 0)
    t = st.number_input("Number of years you are planning to save", min_value = 0)

def reverse_engineer_fixed_amount(FV: float, r: float, t: int) -> float:

    # compounding perioids per year
    n = 12
    r_decimal = r/100

    if FV != 0:
        P = (FV * (r_decimal/n)) / ((1 + r_decimal/n)**(n*t) - 1)
    return P

if t:
    P = reverse_engineer_fixed_amount(FV=FV, r=r, t=t)
    st.write(f"`{P:.2f}`")