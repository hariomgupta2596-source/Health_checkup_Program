"""Database schema setup for Health Checkup Program.
Uses SQLAlchemy Core to define tables and create them if they do not exist.
"""
import os
from datetime import datetime

from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
)

# Import engine from db_connection
from .db_connection import engine

metadata = MetaData()

# ---------------------------------------------------------------------------
# Users table (authentication)
# ---------------------------------------------------------------------------
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False, unique=True),
    Column("email", String, nullable=False, unique=True),
    Column("password_hash", String, nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow),
)

# ---------------------------------------------------------------------------
# User Profiles – optional extra information
# ---------------------------------------------------------------------------
profiles = Table(
    "profiles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True),
    Column("display_name", String),
    Column("age", Integer),
    Column("gender", String),
    Column("created_at", DateTime, default=datetime.utcnow),
)

# ---------------------------------------------------------------------------
# Health Checkups – one per assessment
# ---------------------------------------------------------------------------
checkups = Table(
    "checkups",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("date", DateTime, default=datetime.utcnow, nullable=False),
    Column("height_cm", Float, nullable=False),
    Column("weight_kg", Float, nullable=False),
    Column("bmi", Float, nullable=False),
    Column("blood_pressure", String),
    Column("heart_rate", Integer),
    Column("temperature", Float),
    Column("sleep_hours", Float),
    Column("exercise_days", Integer),
    Column("water_intake", Integer),
    Column("smoking", String),
    Column("alcohol", String),
    Column("stress_level", String),
    Column("other_conditions", Text),
    Column("created_at", DateTime, default=datetime.utcnow),
)

# ---------------------------------------------------------------------------
# Health Conditions – many‑to‑many relationship via a simple JSON‑like column
# We store boolean flags for common conditions; for extensibility we also keep a
# free‑text field in the checkups table (other_conditions).
# ---------------------------------------------------------------------------
conditions = Table(
    "conditions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("checkup_id", Integer, ForeignKey("checkups.id", ondelete="CASCADE"), nullable=False),
    Column("diabetes", Boolean, default=False),
    Column("hypertension", Boolean, default=False),
    Column("asthma", Boolean, default=False),
    Column("heart_disease", Boolean, default=False),
    Column("thyroid", Boolean, default=False),
)

def create_all():
    """Create all tables if they do not already exist."""
    metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_all()
