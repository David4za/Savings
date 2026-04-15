import streamlit as st

from millify import millify

from pages.calculations.reverse_savings import reverse_engineer_fixed_amount
from pages.components.input_panel import (
    inject_input_panel_styles,
    input_panel_header,
    input_section_title,
)
from pages.components.summary_cards import (
    inject_summary_styles,
    summary_card,
    summary_grid_spacer,
)

st.title("Reverse Engineer Savings")

# ---- USER INPUTS ----
inject_input_panel_styles()
input_panel_header(
    "Assumptions",
    "Define the savings target",
    "Set the amount you want to reach, the expected return, and the time available to save.",
)

with st.container(border=True):
    input_section_title("Target assumptions")
    col1, col2, col3 = st.columns(3)

    with col1:
        FV = st.number_input(
            "Target amount",
            value=650000,
            min_value=0,
            help="The total savings amount you want to reach.",
        )
    with col2:
        r = st.number_input(
            "Expected return (%)",
            value=5,
            min_value=0,
            help="Average yearly return assumption.",
        )
    with col3:
        t = st.number_input(
            "Saving period (years)",
            value=30,
            min_value=0,
            help="How many years you have to reach the target.",
        )

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
    
