import streamlit as st

import time
from millify import millify

from pages.calculations.future_savings import (
    future_value_annuity,
    inflation_adjustment,
    total_contributions,
)
from pages.charts.savings_charts import savings_over_time_chart
from pages.components.input_panel import (
    inject_input_panel_styles,
    input_helper,
    input_panel_header,
    input_section_title,
)
from pages.components.summary_cards import (
    inject_summary_styles,
    summary_card,
    summary_grid_spacer,
)


st.set_page_config(
    page_title="Wealth Planner",
    page_icon="💰",
    layout="wide"
)

st.title("Wealth Planner")
st.caption("Play with monthly savings, lump sums, interest rates etc to see how your wealth can grow.")

# ---- USER INPUTS ----
inject_input_panel_styles()
input_panel_header(
    "Assumptions",
    "Build the savings scenario",
    "Set your recurring savings, expected growth, time horizon, and optional one-off deposits.",
)

with st.container(border=True):
    input_section_title("Core assumptions")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        P = st.number_input(
            "Monthly saving",
            value=400,
            min_value=0,
            step=50,
            help="How much you plan to save each month.",
        )
    with col2:
        r = st.number_input(
            "Expected return (%)",
            value=7,
            min_value=0,
            max_value=30,
            help="Average yearly return assumption.",
        )
    with col3:
        t = st.number_input(
            "Saving period (years)",
            value=30,
            min_value=0,
            help="How many years you plan to save.",
        )
    with col4:
        inflation = st.number_input(
            "Inflation rate (%)",
            value=2,
            min_value=0,
            max_value=15,
            help="Used to estimate the inflation-adjusted value.",
        )

with st.container(border=True):
    input_section_title("One-off deposits")
    input_helper(
        "Add optional lump sums. A deposit after 20 years in a 30-year plan grows for the final 10 years."
    )
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
                "Add after year",
                min_value=0,
                max_value=t,
                step=1,
                key=f"lump_sum_year_{lump_sum_index}",
                help="Use 0 if this amount is invested today.",
            )
        if lump_sum_amount > 0:
            lump_sums.append((float(lump_sum_amount), int(years_from_now)))

@st.cache_data
def cached_future_value_annuity(
    monthly_contribution: float,
    lump_sums: tuple[tuple[float, int], ...],
    annual_rate: float,
    years: int,
):
    return future_value_annuity(
        monthly_contribution=monthly_contribution,
        lump_sums=lump_sums,
        annual_rate=annual_rate,
        years=years,
    )


@st.cache_data
def cached_inflation_adjustment(
    total_savings: float,
    inflation_rate: float,
    years: int,
) -> float:
    return inflation_adjustment(
        total_savings=total_savings,
        inflation_rate=inflation_rate,
        years=years,
    )

# ---- Calculations and Display ----
if st.button("Calculate", type="primary"):
    with st.spinner("Calculating ..."):
        time.sleep(1)
        st.success("Calculations complete!")
    lump_sums_for_calculation = tuple(lump_sums)
    df = cached_future_value_annuity(
        monthly_contribution=P,
        lump_sums=lump_sums_for_calculation,
        annual_rate=r,
        years=t,
    )
    if not df.empty:
        total_fv = df.loc[df.index[-1], "Total FV"]
        total_contrib = total_contributions(
            monthly_contribution=P,
            lump_sums=lump_sums_for_calculation,
            years=t,
        )
        total_interest = total_fv - total_contrib
        
        adjusted_savings = cached_inflation_adjustment(
            total_savings=total_fv,
            inflation_rate=inflation,
            years=t,
        )

    # ---- Metric Values ----
        st.markdown("### Summary")
        st.caption("Key figure overview at the end of the savings term")
        inject_summary_styles()
        interest_share = total_interest / total_fv if total_fv else 0
        inflation_gap = total_fv - adjusted_savings
        lump_sum_total = sum(amount for amount, _ in lump_sums_for_calculation)
        summary_grid_spacer()
        with st.container():
            col_1, col_2, col_3, col_4 = st.columns(4)
            with col_1:
                summary_card(
                    "Total Savings",
                    f"€{millify(total_fv)}",
                    f"Projected balance after {t} years",
                    "#00A878",
                    "linear-gradient(135deg, #DDF9EC 0%, #F7FFFB 100%)",
                )
            with col_2:
                summary_card(
                    "Total Contributions",
                    f"€{millify(total_contrib)}",
                    f"Includes €{millify(lump_sum_total)} in lump sums",
                    "#2D9CDB",
                    "linear-gradient(135deg, #E2F3FF 0%, #F8FCFF 100%)",
                )
            with col_3:
                summary_card(
                    "Interest Earned",
                    f"€{millify(total_interest)}",
                    f"{interest_share:.0%} of the final balance",
                    "#F2994A",
                    "linear-gradient(135deg, #FFF0DD 0%, #FFFBF6 100%)",
                )
            with col_4:
                summary_card(
                    "Inflation Adjusted",
                    f"€{millify(adjusted_savings)}",
                    f"€{millify(inflation_gap)} estimated purchasing-power drag",
                    "#EB5757",
                    "linear-gradient(135deg, #FFE8E8 0%, #FFFAFA 100%)",
                )
        fig_1 = savings_over_time_chart(df)
        st.plotly_chart(fig_1, use_container_width=True)
