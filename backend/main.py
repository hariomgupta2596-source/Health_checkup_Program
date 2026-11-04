"""FastAPI backend for Health Checkup Program.

Exposes REST endpoints consumed by the Next.js frontend.
Includes: Authentication, Checkup assessments, Interactive dashboard,
PDF reports, Complete checkup history with search & compare, and User profile.
"""

import sys
import os

# Add project root to sys.path so existing modules are importable
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from typing import Optional
from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

from database.db_connection import engine
from database.db_setup import users, profiles, checkups, conditions, create_all
from authentication import get_password_hash, verify_password
from modules.health_checkup import save_checkup
from modules.health_analysis import get_comprehensive_analysis
from modules.bmi_calculator import calculate_bmi
from utils.pdf_generator import generate_checkup_pdf

# Ensure tables exist and schema is up to date
create_all()

app = FastAPI(title="Health Checkup API", version="1.1.0")

# ---------------------------------------------------------------------------
# CORS – allow all origins for web clients (including Vercel deployment)
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


class ProfileUpdateRequest(BaseModel):
    display_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str


class CheckupRequest(BaseModel):
    name: str
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    blood_pressure: Optional[str] = None
    systolic: Optional[int] = None
    diastolic: Optional[int] = None
    heart_rate: int
    temperature: float
    sleep_hours: int
    exercise_days: int
    water_intake: int
    smoking: str
    alcohol: str
    stress_level: str
    other_conditions: str = ""
    allergies: str = ""
    medications: str = ""
    family_history: str = ""
    diabetes: bool = False
    hypertension: bool = False
    asthma: bool = False
    heart_disease: bool = False
    thyroid: bool = False


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Health Checkup API is running", "version": "1.1.0"}


@app.post("/api/register")
def register(body: RegisterRequest):
    """Register a new user account."""
    sel = users.select().where(
        (users.c.username == body.username) | (users.c.email == body.email)
    )
    with engine.connect() as conn:
        existing = conn.execute(sel).mappings().fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Username or email is already registered")

    password_hash = get_password_hash(body.password)
    ins = users.insert().values(
        username=body.username,
        email=body.email,
        password_hash=password_hash,
    )
    try:
        with engine.begin() as conn:
            result = conn.execute(ins)
            user_id = result.inserted_primary_key[0]
            # Create matching blank profile
            conn.execute(profiles.insert().values(user_id=user_id, display_name=body.username))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Registration failed: {exc}") from exc
    return {"message": "User registered successfully"}


@app.post("/api/login")
def login(body: LoginRequest):
    """Authenticate a user."""
    sel = users.select().where(
        (users.c.username == body.login_identifier)
        | (users.c.email == body.login_identifier)
    )
    with engine.connect() as conn:
        row = conn.execute(sel).mappings().fetchone()

    if row is None or not verify_password(body.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"user_id": row["id"], "username": row["username"]}


# ---------------------------------------------------------------------------
# Profile Management
# ---------------------------------------------------------------------------

@app.get("/api/profile")
def get_profile(x_user_id: Optional[str] = Header(None)):
    """Fetch current user's profile information and statistics."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    with engine.connect() as conn:
        usr = conn.execute(users.select().where(users.c.id == user_id)).mappings().fetchone()
        if not usr:
            raise HTTPException(status_code=404, detail="User not found")

        prof = conn.execute(profiles.select().where(profiles.c.user_id == user_id)).mappings().fetchone()
        total_checkups = conn.execute(
            checkups.select().where(checkups.c.user_id == user_id)
        ).fetchall()

    return {
        "username": usr["username"],
        "email": usr["email"],
        "created_at": usr["created_at"].isoformat() if usr["created_at"] else None,
        "display_name": prof["display_name"] if prof and prof["display_name"] else usr["username"],
        "age": prof["age"] if prof else None,
        "gender": prof["gender"] if prof else None,
        "total_checkups": len(total_checkups),
    }


@app.put("/api/profile")
def update_profile(body: ProfileUpdateRequest, x_user_id: Optional[str] = Header(None)):
    """Update user profile preferences."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    with engine.begin() as conn:
        prof = conn.execute(profiles.select().where(profiles.c.user_id == user_id)).mappings().fetchone()
        if prof:
            conn.execute(
                profiles.update()
                .where(profiles.c.user_id == user_id)
                .values(
                    display_name=body.display_name,
                    age=body.age,
                    gender=body.gender,
                )
            )
        else:
            conn.execute(
                profiles.insert().values(
                    user_id=user_id,
                    display_name=body.display_name,
                    age=body.age,
                    gender=body.gender,
                )
            )

    return {"message": "Profile updated successfully"}


@app.put("/api/profile/password")
def change_password(body: PasswordChangeRequest, x_user_id: Optional[str] = Header(None)):
    """Change account password with verification of current password."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    with engine.connect() as conn:
        usr = conn.execute(users.select().where(users.c.id == user_id)).mappings().fetchone()
        if not usr:
            raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(body.current_password, usr["password_hash"]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    new_hash = get_password_hash(body.new_password)
    with engine.begin() as conn:
        conn.execute(
            users.update().where(users.c.id == user_id).values(password_hash=new_hash)
        )

    return {"message": "Password changed successfully"}


# ---------------------------------------------------------------------------
# Assessment & Checkups
# ---------------------------------------------------------------------------

@app.post("/api/checkup")
def submit_checkup(body: CheckupRequest, x_user_id: Optional[str] = Header(None)):
    """Save a health checkup and return age-aware analysis and wellness recommendations."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    bmi = calculate_bmi(body.height_cm, body.weight_kg)
    bp_string = body.blood_pressure
    if not bp_string and body.systolic and body.diastolic:
        bp_string = f"{body.systolic}/{body.diastolic}"

    analysis_input = {
        "age": body.age,
        "height_cm": body.height_cm,
        "weight_kg": body.weight_kg,
        "bmi": bmi,
        "systolic": body.systolic,
        "diastolic": body.diastolic,
        "heart_rate": body.heart_rate,
        "temperature": body.temperature,
        "sleep_hours": body.sleep_hours,
        "exercise_days": body.exercise_days,
        "water_intake": body.water_intake,
        "smoking": body.smoking,
        "alcohol": body.alcohol,
        "stress_level": body.stress_level,
        "allergies": body.allergies,
    }
    analysis = get_comprehensive_analysis(analysis_input)

    data = {
        "height_cm": body.height_cm,
        "weight_kg": body.weight_kg,
        "bmi": bmi,
        "blood_pressure": bp_string,
        "systolic": body.systolic,
        "diastolic": body.diastolic,
        "heart_rate": body.heart_rate,
        "temperature": body.temperature,
        "sleep_hours": body.sleep_hours,
        "exercise_days": body.exercise_days,
        "water_intake": body.water_intake,
        "smoking": body.smoking,
        "alcohol": body.alcohol,
        "stress_level": body.stress_level,
        "other_conditions": body.other_conditions,
        "allergies": body.allergies,
        "medications": body.medications,
        "family_history": body.family_history,
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

    return {
        "checkup_id": checkup_id,
        "bmi": bmi,
        "bmi_eval": analysis["bmi_eval"],
        "bp_eval": analysis["bp_eval"],
        "hr_eval": analysis["hr_eval"],
        "temp_eval": analysis["temp_eval"],
        "recommendations": analysis["recommendations"],
        "disclaimer": analysis["disclaimer"],
    }


@app.get("/api/dashboard")
def dashboard(x_user_id: Optional[str] = Header(None)):
    """Return assessment records for trend visualisations."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    sel = checkups.select().where(checkups.c.user_id == user_id).order_by(checkups.c.date.asc())
    with engine.connect() as conn:
        rows = conn.execute(sel).mappings().fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row["id"],
            "date": row["date"].isoformat() if row["date"] else None,
            "bmi": row["bmi"],
            "heart_rate": row["heart_rate"],
            "temperature": row["temperature"],
            "blood_pressure": row["blood_pressure"],
            "systolic": row.get("systolic"),
            "diastolic": row.get("diastolic"),
            "sleep_hours": row["sleep_hours"],
            "exercise_days": row["exercise_days"],
            "water_intake": row["water_intake"],
            "stress_level": row.get("stress_level"),
        })
    return result


@app.get("/api/history")
def checkup_history(
    q: Optional[str] = Query(None),
    x_user_id: Optional[str] = Header(None),
):
    """Return all checkup assessments for the authenticated user, supporting optional search."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    sel = checkups.select().where(checkups.c.user_id == user_id).order_by(checkups.c.date.desc())
    with engine.connect() as conn:
        rows = conn.execute(sel).mappings().fetchall()

    result = []
    for row in rows:
        cond_row = conn.execute(
            conditions.select().where(conditions.c.checkup_id == row["id"])
        ).mappings().fetchone()

        cond_list = []
        if cond_row:
            if cond_row["diabetes"]: cond_list.append("Diabetes")
            if cond_row["hypertension"]: cond_list.append("Hypertension")
            if cond_row["asthma"]: cond_list.append("Asthma")
            if cond_row["heart_disease"]: cond_list.append("Heart Disease")
            if cond_row["thyroid"]: cond_list.append("Thyroid")

        item = {
            "id": row["id"],
            "date": row["date"].isoformat() if row["date"] else None,
            "height_cm": row["height_cm"],
            "weight_kg": row["weight_kg"],
            "bmi": row["bmi"],
            "blood_pressure": row["blood_pressure"] or (f"{row.get('systolic')}/{row.get('diastolic')}" if row.get("systolic") else "Not Recorded"),
            "systolic": row.get("systolic"),
            "diastolic": row.get("diastolic"),
            "heart_rate": row["heart_rate"],
            "temperature": row["temperature"],
            "sleep_hours": row["sleep_hours"],
            "exercise_days": row["exercise_days"],
            "water_intake": row["water_intake"],
            "smoking": row["smoking"],
            "alcohol": row["alcohol"],
            "stress_level": row["stress_level"],
            "other_conditions": row["other_conditions"],
            "allergies": row.get("allergies") or "",
            "medications": row.get("medications") or "",
            "family_history": row.get("family_history") or "",
            "conditions": cond_list,
        }

        # Apply search filter if query string provided
        if q:
            q_lower = q.lower()
            text_corpus = f"{item['date']} {item['blood_pressure']} {item['bmi']} {item['allergies']} {item['medications']} {' '.join(cond_list)}".lower()
            if q_lower not in text_corpus:
                continue

        result.append(item)

    return result


@app.get("/api/checkup/{checkup_id}")
def get_single_checkup(checkup_id: int, x_user_id: Optional[str] = Header(None)):
    """Fetch complete details of a single checkup assessment."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    sel = checkups.select().where((checkups.c.id == checkup_id) & (checkups.c.user_id == user_id))
    with engine.connect() as conn:
        chk = conn.execute(sel).mappings().fetchone()
        if not chk:
            raise HTTPException(status_code=404, detail="Checkup assessment not found")

        cond = conn.execute(
            conditions.select().where(conditions.c.checkup_id == checkup_id)
        ).mappings().fetchone()

    cond_dict = {
        "diabetes": cond["diabetes"] if cond else False,
        "hypertension": cond["hypertension"] if cond else False,
        "asthma": cond["asthma"] if cond else False,
        "heart_disease": cond["heart_disease"] if cond else False,
        "thyroid": cond["thyroid"] if cond else False,
    }

    return {
        "id": chk["id"],
        "date": chk["date"].isoformat() if chk["date"] else None,
        "height_cm": chk["height_cm"],
        "weight_kg": chk["weight_kg"],
        "bmi": chk["bmi"],
        "blood_pressure": chk["blood_pressure"],
        "systolic": chk.get("systolic"),
        "diastolic": chk.get("diastolic"),
        "heart_rate": chk["heart_rate"],
        "temperature": chk["temperature"],
        "sleep_hours": chk["sleep_hours"],
        "exercise_days": chk["exercise_days"],
        "water_intake": chk["water_intake"],
        "smoking": chk["smoking"],
        "alcohol": chk["alcohol"],
        "stress_level": chk["stress_level"],
        "other_conditions": chk["other_conditions"],
        "allergies": chk.get("allergies") or "",
        "medications": chk.get("medications") or "",
        "family_history": chk.get("family_history") or "",
        "conditions": cond_dict,
    }


@app.delete("/api/checkup/{checkup_id}")
def delete_checkup(checkup_id: int, x_user_id: Optional[str] = Header(None)):
    """Delete a past assessment record with user authorization."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        user_id = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    with engine.begin() as conn:
        chk = conn.execute(
            checkups.select().where((checkups.c.id == checkup_id) & (checkups.c.user_id == user_id))
        ).mappings().fetchone()

        if not chk:
            raise HTTPException(status_code=404, detail="Checkup assessment not found or unauthorized")

        conn.execute(conditions.delete().where(conditions.c.checkup_id == checkup_id))
        conn.execute(checkups.delete().where(checkups.c.id == checkup_id))

    return {"message": "Assessment record deleted successfully"}


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
        row = conn.execute(sel).mappings().fetchone()

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
