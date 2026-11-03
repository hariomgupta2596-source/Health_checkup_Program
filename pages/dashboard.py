import streamlit as st
import pandas as pd
from datetime import datetime

from utils.charts import load_user_checkups, bmi_trend_chart, blood_pressure_chart

def render():
    """Health Dashboard page – shows latest checkup and interactive charts."""
    if "user_id" not in st.session_state:
        st.warning("🔒 Please log in to view the dashboard.")
        st.stop()

    st.header("📊 Health Dashboard")

    # Load all checkups for the current user
    df = load_user_checkups(st.session_state.user_id)
    if df.empty:
        st.info("No health data available. Complete a health checkup first.")
        return

    # Latest checkup (most recent date)
    latest = df.iloc[-1]
    st.subheader(f"Latest Checkup – {latest['date'].strftime('%Y-%m-%d %H:%M')}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("BMI", f"{latest['bmi']:.2f}")
    with col2:
        st.metric("Heart Rate", f"{latest['heart_rate']} bpm")
    with col3:
        st.metric("Temperature", f"{latest['temperature']} °C")
    with col4:
        st.metric("Blood Pressure", latest['blood_pressure'])

    st.divider()
    # Lifestyle metrics
    st.subheader("🏃 Lifestyle Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Sleep", f"{latest['sleep_hours']} hrs/day")
    with col2:
        st.metric("Exercise", f"{latest['exercise_days']} days/week")
    with col3:
        st.metric("Water Intake", f"{latest['water_intake']} glasses/day")

    st.divider()
    # Charts section
    st.subheader("📈 Trends & Visualisations")
    # BMI trend line chart
    bmi_fig = bmi_trend_chart(df)
    if bmi_fig:
        st.plotly_chart(bmi_fig, use_container_width=True)
    else:
        st.info("No BMI data to plot.")

    # Blood pressure scatter chart
    bp_fig = blood_pressure_chart(df)
    if bp_fig:
        st.plotly_chart(bp_fig, use_container_width=True)
    else:
        st.info("No blood pressure data to plot.")
