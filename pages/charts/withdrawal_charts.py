import pandas as pd
import plotly.express as px

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
    fig.update_layout(
        template="plotly_white",
        title=dict(
            text="Balance by Year",
            font=dict(size=24, color="#111827"),
            x=0.02,
            xanchor="left",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FBFCFD",
        font=dict(color="#1F2937", family="Inter, Arial, sans-serif"),
        hovermode="x unified",
        legend=dict(
            title=None,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0)",
            font=dict(size=12),
        ),
        margin=dict(l=24, r=24, t=86, b=48),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor="rgba(17, 24, 39, 0.16)",
            tickfont=dict(color="rgba(17, 24, 39, 0.68)"),
            title=dict(font=dict(color="rgba(17, 24, 39, 0.72)")),
        ),
        yaxis=dict(
            gridcolor="rgba(17, 24, 39, 0.08)",
            zeroline=False,
            tickprefix="€",
            tickformat=",.0f",
            tickfont=dict(color="rgba(17, 24, 39, 0.68)"),
            title=dict(font=dict(color="rgba(17, 24, 39, 0.72)")),
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="rgba(17, 24, 39, 0.12)",
            font=dict(color="#111827"),
        ),
    )
    return fig
