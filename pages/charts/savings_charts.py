import pandas as pd
import plotly.express as px

from pages.charts.chart_theme import apply_streamlit_chart_layout

SAVINGS_COLORS = {
    "Total FV": "#00A878",
    "FV Annuity": "#2D9CDB",
    "FV Lump Sum": "#F2994A",
}

SAVINGS_LABELS = {
    "Total FV": "Total savings",
    "FV Annuity": "Monthly savings",
    "FV Lump Sum": "Lump sums",
}


def savings_over_time_chart(df: pd.DataFrame):
    y_columns = ["Total FV"]
    if not (df["FV Annuity"] == 0).all():
        y_columns.append("FV Annuity")
    if not (df["FV Lump Sum"] == 0).all():
        y_columns.append("FV Lump Sum")

    fig = px.line(
        df,
        x="Year",
        y=y_columns,
        markers=True,
        title="Savings Over Time",
        labels={
            "Year": "Year",
            "value": "Amount (€)",
            "variable": "Component",
        },
        color_discrete_map=SAVINGS_COLORS,
    )
    fig.for_each_trace(
        lambda trace: trace.update(
            name=SAVINGS_LABELS.get(trace.name, trace.name),
            legendgroup=SAVINGS_LABELS.get(trace.name, trace.name),
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
    apply_streamlit_chart_layout(fig, "Savings Over Time")
    return fig
