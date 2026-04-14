import streamlit as st

from millify import millify

from pages.calculations.withdrawals import withdraw_analysis
from pages.charts.withdrawal_charts import balance_by_year_chart
from pages.components.summary_cards import (
    inject_summary_styles,
    summary_card,
    summary_grid_spacer,
)

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
        withdrawal_ratio = total_withdraw / FV if FV else 0

        st.markdown("### Summary")
        st.caption("Estimated drawdown timeline and cash withdrawn")
        inject_summary_styles()
        summary_grid_spacer()
        col_1, col_2, col_3, col_4 = st.columns(4)
        with col_1:
            summary_card(
                "Plan Duration",
                f"{total_years:.1f} yrs",
                f"{int(total_months)} monthly withdrawals",
                "#00A878",
                "linear-gradient(135deg, #DDF9EC 0%, #F7FFFB 100%)",
            )
        with col_2:
            summary_card(
                "Total Withdrawn",
                f"€{millify(total_withdraw)}",
                f"{withdrawal_ratio:.0%} of starting savings",
                "#2D9CDB",
                "linear-gradient(135deg, #E2F3FF 0%, #F8FCFF 100%)",
            )
        with col_3:
            summary_card(
                "Monthly Withdrawal",
                f"€{millify(withdraw)}",
                "Fixed monthly cash flow",
                "#F2994A",
                "linear-gradient(135deg, #FFF0DD 0%, #FFFBF6 100%)",
            )
        with col_4:
            summary_card(
                "Starting Savings",
                f"€{millify(FV)}",
                f"{r}% return and {inflation}% inflation",
                "#EB5757",
                "linear-gradient(135deg, #FFE8E8 0%, #FFFAFA 100%)",
            )

        fig_1 = balance_by_year_chart(df)
        st.plotly_chart(fig_1, use_container_width=True)
