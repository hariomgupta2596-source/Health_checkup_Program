"""Utility functions for persisting health checkup data.

The `save_checkup` function inserts a new record into the `checkups` table and the
associated boolean condition flags into the `conditions` table.
"""
from datetime import datetime
from typing import Dict, Any

from database.db_connection import engine
from database.db_setup import checkups, conditions


def save_checkup(user_id: int, data: Dict[str, Any]):
    """Insert a health‑checkup record for the given user.

    Parameters
    ----------
    user_id: int
        Primary key of the authenticated user.
    data: dict
        Dictionary containing the fields collected from the form. Expected keys:
        ``height_cm, weight_kg, bmi, blood_pressure, heart_rate, temperature,
        sleep_hours, exercise_days, water_intake, smoking, alcohol,
        stress_level, other_conditions``.
    """
    # Insert the main checkup row
    checkup_ins = checkups.insert().values(
        user_id=user_id,
        date=datetime.utcnow(),
        height_cm=data["height_cm"],
        weight_kg=data["weight_kg"],
        bmi=data["bmi"],
        blood_pressure=data.get("blood_pressure"),
        heart_rate=data.get("heart_rate"),
        temperature=data.get("temperature"),
        sleep_hours=data.get("sleep_hours"),
        exercise_days=data.get("exercise_days"),
        water_intake=data.get("water_intake"),
        smoking=data.get("smoking"),
        alcohol=data.get("alcohol"),
        stress_level=data.get("stress_level"),
        other_conditions=data.get("other_conditions"),
        created_at=datetime.utcnow(),
    )
    with engine.begin() as conn:
        result = conn.execute(checkup_ins)
        checkup_id = result.inserted_primary_key[0]

        # Insert condition flags (boolean values)
        cond_ins = conditions.insert().values(
            checkup_id=checkup_id,
            diabetes=bool(data.get("diabetes")),
            hypertension=bool(data.get("hypertension")),
            asthma=bool(data.get("asthma")),
            heart_disease=bool(data.get("heart_disease")),
            thyroid=bool(data.get("thyroid")),
        )
        conn.execute(cond_ins)

    return checkup_id
