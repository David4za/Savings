import streamlit as st

from millify import millify

from pages.calculations.reverse_savings import reverse_engineer_fixed_amount
from pages.components.summary_cards import (
    inject_summary_styles,
    summary_card,
    summary_grid_spacer,
)

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
        total_contributions = P * 12 * t

        st.markdown("### Summary")
        st.caption("Monthly savings needed to reach the target amount")
        inject_summary_styles()
        summary_grid_spacer()
        col_1, col_2, col_3, col_4 = st.columns(4)
        with col_1:
            summary_card(
                "Monthly Needed",
                f"€{P:.2f}",
                "Fixed amount to save each month",
                "#00A878",
                "linear-gradient(135deg, #DDF9EC 0%, #F7FFFB 100%)",
            )
        with col_2:
            summary_card(
                "Target Amount",
                f"€{millify(FV)}",
                f"Goal after {t} years",
                "#2D9CDB",
                "linear-gradient(135deg, #E2F3FF 0%, #F8FCFF 100%)",
            )
        with col_3:
            summary_card(
                "Total Saved",
                f"€{millify(total_contributions)}",
                "Cash contributed before growth",
                "#F2994A",
                "linear-gradient(135deg, #FFF0DD 0%, #FFFBF6 100%)",
            )
        with col_4:
            summary_card(
                "Expected Return",
                f"{r}%",
                "Annual compounding assumption",
                "#EB5757",
                "linear-gradient(135deg, #FFE8E8 0%, #FFFAFA 100%)",
            )
    
