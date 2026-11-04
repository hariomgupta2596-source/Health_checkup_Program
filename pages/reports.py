import streamlit as st
from datetime import datetime
import pandas as pd
from utils.ui import load_css, card_wrapper
from utils.charts import load_user_checkups
from utils.pdf_generator import generate_checkup_pdf


def render():
    """Reports page – lets the user download a PDF of their latest health checkup."""
    load_css()
    def page_body():
        if "user_id" not in st.session_state:
            st.warning("🔒 Please log in to view reports.")
            st.stop()
        st.header("📄 Health Reports")
        # Load user's checkups to get the latest record ID
        df = load_user_checkups(st.session_state.user_id)
        if df.empty:
            st.info("No health data available. Complete a health checkup first.")
            return
        latest_id = df.iloc[-1]["id"]
        latest_date = df.iloc[-1]["date"].strftime("%Y-%m-%d %H:%M")
        st.subheader(f"Latest Checkup – {latest_date}")
        # Offer PDF download
        if st.button("Generate PDF Report"):
            try:
                pdf_bytes = generate_checkup_pdf(st.session_state.user_id, checkup_id=latest_id)
                st.success("✅ PDF generated successfully!")
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_bytes,
                    file_name=f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                )
            except Exception as e:
                st.error(f"Failed to generate PDF: {e}")
    card_wrapper(page_body)
