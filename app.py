import os
import streamlit as st
from datetime import datetime

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Health Checkup Program",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Load custom CSS (if present)
# ---------------------------------------------------------------------------
css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
if os.path.isfile(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
if "checkups" not in st.session_state:
    st.session_state.checkups = []

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
if "user_id" not in st.session_state:
    # Show only authentication options
    page = st.sidebar.radio(
        "Navigation",
        ["Login", "Register"],
        index=0,
    )
else:
    page = st.sidebar.radio(
        "Navigation",
        ["Home", "Health Checkup", "Health Dashboard", "Reports", "Guidelines"],
    )

# ---------------------------------------------------------------------------
# Render the selected page – each page is a modest module exposing a `render()`
# ---------------------------------------------------------------------------
if page == "Home":
    from pages import home
    home.render()
elif page == "Health Checkup":
    from pages import health_checkup
    health_checkup.render()
elif page == "Health Dashboard":
    from pages import dashboard
    dashboard.render()
elif page == "Reports":
    from pages import reports
    reports.render()
elif page == "Guidelines":
    from pages import guidelines
    guidelines.render()
