def apply_streamlit_chart_layout(fig, title: str) -> None:
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=24),
            x=0.02,
            xanchor="left",
        ),
        hovermode="x unified",
        legend=dict(
            title=None,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=12),
        ),
        margin=dict(l=24, r=24, t=86, b=48),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            zeroline=False,
            tickprefix="€",
            tickformat=",.0f",
        ),
    )
