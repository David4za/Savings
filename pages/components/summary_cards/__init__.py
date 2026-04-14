from pathlib import Path

import streamlit as st

COMPONENT_DIR = Path(__file__).parent
SUMMARY_CARD_CSS = COMPONENT_DIR / "summary_cards.css"
SUMMARY_CARD_HTML = COMPONENT_DIR / "summary_card.html"


def inject_summary_styles() -> None:
    st.markdown(
        f"<style>{SUMMARY_CARD_CSS.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


def summary_grid_spacer() -> None:
    st.markdown('<div class="summary-grid-spacer"></div>', unsafe_allow_html=True)


def summary_card(
    label: str,
    value: str,
    detail: str,
    accent: str,
    background: str,
) -> None:
    template = SUMMARY_CARD_HTML.read_text(encoding="utf-8")
    st.markdown(
        template.format(
            label=label,
            value=value,
            detail=detail,
            accent=accent,
            background=background,
        ),
        unsafe_allow_html=True,
    )
