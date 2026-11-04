"""Utility functions for UI helpers.
Provides `load_css()` to inject the custom stylesheet and `card_wrapper()` to wrap UI blocks in a styled card.
"""
import os
import streamlit as st

def load_css():
    """Read the `assets/styles.css` file and inject it via `st.markdown`.
    Should be called at the top of any Streamlit page.
    """
    css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "styles.css")
    if os.path.isfile(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("Custom CSS file not found; default Streamlit styling will be used.")

def card_wrapper(content_func):
    """Wrap a Streamlit UI block inside a styled card.
    `content_func` is a callable that draws the inner UI.
    """
    st.markdown('<div class="card">', unsafe_allow_html=True)
    content_func()
    st.markdown('</div>', unsafe_allow_html=True)
