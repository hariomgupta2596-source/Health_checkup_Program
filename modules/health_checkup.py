"""Utility functions for persisting health checkup data.
Inserts records into the checkups table and associated boolean conditions.
"""
from datetime import datetime
from typing import Dict, Any

from database.db_connection import engine
from database.db_setup import checkups, conditions


def save_checkup(user_id: int, data: Dict[str, Any]) -> int:
    """Insert a health-checkup record for the given user.

    Parameters
    ----------
    user_id: int
        Primary key of the authenticated user.
    data: dict
        Dictionary containing the fields collected from the form.
    """
    checkup_ins = checkups.insert().values(
        user_id=user_id,
        date=datetime.utcnow(),
        height_cm=data["height_cm"],
        weight_kg=data["weight_kg"],
        bmi=data["bmi"],
        blood_pressure=data.get("blood_pressure"),
        systolic=data.get("systolic"),
        diastolic=data.get("diastolic"),
        heart_rate=data.get("heart_rate"),
        temperature=data.get("temperature"),
        sleep_hours=data.get("sleep_hours"),
        exercise_days=data.get("exercise_days"),
        water_intake=data.get("water_intake"),
        smoking=data.get("smoking"),
        alcohol=data.get("alcohol"),
        stress_level=data.get("stress_level"),
        other_conditions=data.get("other_conditions", ""),
        allergies=data.get("allergies", ""),
        medications=data.get("medications", ""),
        family_history=data.get("family_history", ""),
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
