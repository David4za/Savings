import pandas as pd
import plotly.express as px

from pages.charts.chart_theme import apply_streamlit_chart_layout

WITHDRAWAL_COLORS = {
    "Balance": "#00A878",
    "Adjusted Balance": "#EB5757",
}

WITHDRAWAL_LABELS = {
    "Balance": "Balance",
    "Adjusted Balance": "Inflation adjusted",
}


def balance_by_year_chart(df: pd.DataFrame):
    fig = px.line(
        df,
        x="Year",
        y=["Balance", "Adjusted Balance"],
        markers=True,
        title="Balance by Year",
        labels={
            "Year": "Year",
            "value": "Amount (€)",
            "variable": "Balance",
        },
        color_discrete_map=WITHDRAWAL_COLORS,
    )
    fig.for_each_trace(
        lambda trace: trace.update(
            name=WITHDRAWAL_LABELS.get(trace.name, trace.name),
            legendgroup=WITHDRAWAL_LABELS.get(trace.name, trace.name),
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "Year %{x}<br>"
                "Amount: €%{y:,.0f}"
                "<extra></extra>"
            ),
            line=dict(width=4, shape="spline", smoothing=0.55),
            marker=dict(size=7, line=dict(width=2, color="#FFFFFF")),
        )
    )
    apply_streamlit_chart_layout(fig, "Balance by Year")
    return fig
