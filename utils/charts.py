"""Utility functions for generating Plotly visualizations for the Health Checkup Program.

The functions operate on pandas DataFrames that are built from the SQLite `checkups` table. Only the essential charts needed for the dashboard are implemented, but more can be added later.
"""
import pandas as pd
import plotly.express as px

from database.db_connection import engine
from database.db_setup import checkups

def load_user_checkups(user_id: int) -> pd.DataFrame:
    """Return a DataFrame with all checkups for the given user.

    Columns: id, date, bmi, blood_pressure, heart_rate, temperature,
    sleep_hours, exercise_days, water_intake, smoking, alcohol, stress_level.
    """
    cols = [
        checkups.c.id,
        checkups.c.date,
        checkups.c.bmi,
        checkups.c.blood_pressure,
        checkups.c.heart_rate,
        checkups.c.temperature,
        checkups.c.sleep_hours,
        checkups.c.exercise_days,
        checkups.c.water_intake,
        checkups.c.smoking,
        checkups.c.alcohol,
        checkups.c.stress_level,
    ]
    stmt = (
        checkups.select()
        .with_only_columns(cols)
        .where(checkups.c.user_id == user_id)
        .order_by(checkups.c.date)
    )
    with engine.connect() as conn:
        rows = conn.execute(stmt).fetchall()
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows, columns=[c.name for c in cols])
    df["date"] = pd.to_datetime(df["date"])  # ensure datetime type
    return df

def bmi_trend_chart(df: pd.DataFrame):
    """Create a Plotly line chart showing BMI over time.
    Returns a Plotly Figure object (or ``None`` if no data).
    """
    if df.empty:
        return None
    fig = px.line(df, x="date", y="bmi", title="BMI Trend Over Time", markers=True)
    fig.update_layout(xaxis_title="Date", yaxis_title="BMI")
    return fig

def blood_pressure_chart(df: pd.DataFrame):
    """Create a Plotly scatter chart for systolic and diastolic pressure over time.
    The ``blood_pressure`` column is expected to be a string like ``"120/80"``.
    Returns a Plotly Figure (or ``None`` if parsing fails).
    """
    if df.empty:
        return None
    # Split the BP string into systolic and diastolic columns
    def split_bp(bp: str):
        try:
            systolic, diastolic = bp.split("/")
            return int(systolic), int(diastolic)
        except Exception:
            return None, None
    systolic, diastolic = zip(*df["blood_pressure"].apply(split_bp))
    df = df.copy()
    df["systolic"] = systolic
    df["diastolic"] = diastolic
    df = df.dropna(subset=["systolic", "diastolic"])
    if df.empty:
        return None
    fig = px.scatter(df, x="date", y=["systolic", "diastolic"], title="Blood Pressure Over Time")
    fig.update_layout(xaxis_title="Date", yaxis_title="mmHg")
    return fig
