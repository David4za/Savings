import pandas as pd
import plotly.express as px


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
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=20, t=60, b=40),
    )
    return fig
