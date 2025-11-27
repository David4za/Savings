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

# ---- PAGE NAVIGATION ----

pg = st.navigation({
    "Plans":[fixed_plan, reverse_plan, withdraw_plan]
})

pg.run()