import pandas as pd
import plotly.express as px


def balance_by_year_chart(df: pd.DataFrame):
    return px.line(
        df,
        x="Year",
        y=["Balance", "Adjusted Balance"],
        markers=True,
        title="Balance by Year",
        color_discrete_sequence=["#00BB88", "#FF0000"],
    )
