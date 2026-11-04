"""FastAPI backend for Health Checkup Program.

Exposes REST endpoints consumed by the Next.js frontend.
Reuses the existing Python modules (db_connection, db_setup,
authentication, modules/health_checkup, utils/pdf_generator).
"""

import sys
import os

# Add project root to sys.path so existing modules are importable
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from typing import Optional
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field

from database.db_connection import engine
from database.db_setup import users, checkups, create_all
from authentication import get_password_hash, verify_password
from modules.health_checkup import save_checkup
from utils.pdf_generator import generate_checkup_pdf

# Ensure tables exist
create_all()

app = FastAPI(title="Health Checkup API", version="1.0.0")

# ---------------------------------------------------------------------------
# CORS – allow all origins (suitable for local dev; restrict in production)
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------------------------

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    login_identifier: str  # username or email
    password: str


class CheckupRequest(BaseModel):
    name: str
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    blood_pressure: str
    heart_rate: int
    temperature: float
    sleep_hours: int
    exercise_days: int
    water_intake: int
    smoking: str
    alcohol: str
    stress_level: str
    other_conditions: str = ""
    diabetes: bool = False
    hypertension: bool = False
    asthma: bool = False
    heart_disease: bool = False
    thyroid: bool = False


# ---------------------------------------------------------------------------
# Helper: compute BMI and recommendations (mirrors Streamlit logic)
# ---------------------------------------------------------------------------

def _compute_bmi(height_cm: float, weight_kg: float) -> float:
    return round(weight_kg / ((height_cm / 100) ** 2), 2)


def _compute_recommendations(
    bmi: float,
    heart_rate: int,
    sleep_hours: int,
    exercise_days: int,
    stress_level: str,
    smoking: str,
    water_intake: int,
) -> list:
    recs = []
    if bmi >= 25:
        recs.append("🍎 Increase physical activity and maintain a balanced diet")
    if heart_rate > 100 or heart_rate < 60:
        recs.append("❤️ Consult a doctor about your heart rate")
    if sleep_hours < 7:
        recs.append("😴 Aim for 7-9 hours of sleep per night")
    if exercise_days < 3:
        recs.append("🏃 Try to exercise at least 3-4 days per week")
    if stress_level in ["High", "Very High"]:
        recs.append("🧘 Practice stress management techniques like meditation")
    if smoking == "Current":
        recs.append("🚭 Consider quitting smoking for better health")
    if water_intake < 8:
        recs.append("💧 Increase water intake to at least 8 glasses per day")
    if not recs:
        recs.append("✨ Great! Keep maintaining your healthy lifestyle!")
    return recs


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/api/register")
def register(body: RegisterRequest):
    """Register a new user."""
    password_hash = get_password_hash(body.password)
    ins = users.insert().values(
        username=body.username,
        email=body.email,
        password_hash=password_hash,
    )
    try:
        with engine.begin() as conn:
            conn.execute(ins)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Registration failed: {exc}") from exc
    return {"message": "User registered successfully"}


@app.post("/api/login")
def login(body: LoginRequest):
    """Authenticate a user. Returns user_id and username on success."""
    sel = users.select().where(
        (users.c.username == body.login_identifier)
        | (users.c.email == body.login_identifier)
    )
    with engine.connect() as conn:
        row = conn.execute(sel).fetchone()

    if row is None or not verify_password(body.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"user_id": row["id"], "username": row["username"]}


@app.post("/api/checkup")
def submit_checkup(body: CheckupRequest, x_user_id: Optional[str] = Header(None)):
    """Save a health checkup and return computed metrics."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    bmi = _compute_bmi(body.height_cm, body.weight_kg)
    recommendations = _compute_recommendations(
        bmi=bmi,
        heart_rate=body.heart_rate,
        sleep_hours=body.sleep_hours,
        exercise_days=body.exercise_days,
        stress_level=body.stress_level,
        smoking=body.smoking,
        water_intake=body.water_intake,
    )

    data = {
        "height_cm": body.height_cm,
        "weight_kg": body.weight_kg,
        "bmi": bmi,
        "blood_pressure": body.blood_pressure,
        "heart_rate": body.heart_rate,
        "temperature": body.temperature,
        "sleep_hours": body.sleep_hours,
        "exercise_days": body.exercise_days,
        "water_intake": body.water_intake,
        "smoking": body.smoking,
        "alcohol": body.alcohol,
        "stress_level": body.stress_level,
        "other_conditions": body.other_conditions,
        "diabetes": body.diabetes,
        "hypertension": body.hypertension,
        "asthma": body.asthma,
        "heart_disease": body.heart_disease,
        "thyroid": body.thyroid,
    }

    try:
        checkup_id = save_checkup(user_id, data)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to save checkup: {exc}") from exc

    return {"checkup_id": checkup_id, "bmi": bmi, "recommendations": recommendations}


@app.get("/api/dashboard")
def dashboard(x_user_id: Optional[str] = Header(None)):
    """Return all checkup records for the authenticated user."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    sel = checkups.select().where(checkups.c.user_id == user_id).order_by(checkups.c.date.desc())
    with engine.connect() as conn:
        rows = conn.execute(sel).fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row["id"],
            "date": row["date"].isoformat() if row["date"] else None,
            "bmi": row["bmi"],
            "heart_rate": row["heart_rate"],
            "temperature": row["temperature"],
            "blood_pressure": row["blood_pressure"],
            "sleep_hours": row["sleep_hours"],
            "exercise_days": row["exercise_days"],
            "water_intake": row["water_intake"],
        })
    return result


@app.get("/api/reports/latest")
def reports_latest(x_user_id: Optional[str] = Header(None)):
    """Return the id and date of the latest checkup for the user."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    sel = (
        checkups.select()
        .where(checkups.c.user_id == user_id)
        .order_by(checkups.c.date.desc())
        .limit(1)
    )
    with engine.connect() as conn:
        row = conn.execute(sel).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="No checkups found")

    return {"id": row["id"], "date": row["date"].isoformat() if row["date"] else None}


@app.get("/api/reports/pdf/{checkup_id}")
def download_pdf(checkup_id: int, x_user_id: Optional[str] = Header(None)):
    """Stream a PDF report for the specified checkup."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    try:
        pdf_bytes = generate_checkup_pdf(user_id, checkup_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {exc}") from exc

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=checkup_{checkup_id}.pdf"},
    )
