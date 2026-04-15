from html import escape
from pathlib import Path

import streamlit as st

COMPONENT_DIR = Path(__file__).parent
INPUT_PANEL_CSS = COMPONENT_DIR / "input_panel.css"


def inject_input_panel_styles() -> None:
    st.markdown(
        f"<style>{INPUT_PANEL_CSS.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


def input_panel_header(eyebrow: str, title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="input-panel-header">
            <div class="input-panel-header__eyebrow">{escape(eyebrow)}</div>
            <h2 class="input-panel-header__title">{escape(title)}</h2>
            <p class="input-panel-header__copy">{escape(copy)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def input_section_title(label: str) -> None:
    st.markdown(
        f"""
        <div class="input-panel-section-title">
            <span class="input-panel-section-title__marker"></span>
            <span class="input-panel-section-title__text">{escape(label)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def input_helper(copy: str) -> None:
    st.markdown(
        f'<p class="input-panel-helper">{escape(copy)}</p>',
        unsafe_allow_html=True,
    )
