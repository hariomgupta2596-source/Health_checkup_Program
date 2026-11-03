import pytest
from datetime import datetime

from authentication import get_password_hash
from database.db_connection import engine
from database.db_setup import users, checkups, conditions, create_all
from modules.health_checkup import save_checkup

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    # Ensure fresh tables
    create_all()
    yield
    # Cleanup test data after each test
    with engine.begin() as conn:
        conn.execute(checkups.delete())
        conn.execute(conditions.delete())
        conn.execute(users.delete().where(users.c.username.like("test_user_%")))

def _create_test_user():
    username = f"test_user_{datetime.utcnow().timestamp()}"
    email = f"{username}@example.com"
    pwd_hash = get_password_hash("password")
    with engine.begin() as conn:
        result = conn.execute(users.insert().values(username=username, email=email, password_hash=pwd_hash, created_at=datetime.utcnow()))
        user_id = result.inserted_primary_key[0]
    return user_id

def test_save_checkup_and_retrieve():
    user_id = _create_test_user()
    data = {
        "height_cm": 170,
        "weight_kg": 70,
        "bmi": 24.22,
        "blood_pressure": "120/80",
        "heart_rate": 72,
        "temperature": 37.0,
        "sleep_hours": 7,
        "exercise_days": 3,
        "water_intake": 8,
        "smoking": "Never",
        "alcohol": "Never",
        "stress_level": "Low",
        "other_conditions": "",
        "diabetes": False,
        "hypertension": False,
        "asthma": False,
        "heart_disease": False,
        "thyroid": False,
    }
    checkup_id = save_checkup(user_id, data)
    # Verify checkup row exists
    with engine.connect() as conn:
        chk = conn.execute(checkups.select().where(checkups.c.id == checkup_id)).fetchone()
        assert chk is not None
        assert chk["bmi"] == data["bmi"]
        # Verify condition row linked via foreign key
        cond = conn.execute(conditions.select().where(conditions.c.checkup_id == checkup_id)).fetchone()
        assert cond is not None
        assert cond["diabetes"] == data["diabetes"]
