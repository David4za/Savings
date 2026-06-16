import streamlit as st

# ---- PAGE SETUP ----

fixed_plan = st.Page(
    page=r"pages/input_plan.py",
    title="Fixed Income Plan",
    icon=":material/savings:",
    default=True
)

reverse_plan = st.Page(
    page=r"pages/reverse_plan.py",
    title="Reverse engineering a plan",
    icon= ":material/local_atm:"
)

withdraw_plan = st.Page(
    page=r"pages/withdraw.py",
    title="Withdraw Plan",
    icon=":material/payments:"
)

math_overview = st.Page(
    page=r"pages/math_overview.py",
    title="How the math works",
    icon=":material/functions:",
)

# ---- PAGE NAVIGATION ----

pg = st.navigation({
    "Plans": [fixed_plan, reverse_plan, withdraw_plan],
    "Reference": [math_overview],
})

pg.run()