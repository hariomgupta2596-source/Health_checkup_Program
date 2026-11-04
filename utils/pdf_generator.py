"""PDF report generation utilities using ReportLab.
Creates clinical-style assessment summaries for the Health Checkup Program.
"""
import io
from datetime import datetime

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

from database.db_connection import engine
from database.db_setup import checkups, conditions, users, profiles


def _fetch_checkup(user_id: int, checkup_id: int = None):
    """Retrieve checkup record, condition flags, and user details from DB."""
    sel = checkups.select().where(checkups.c.user_id == user_id)
    if checkup_id is not None:
        sel = sel.where(checkups.c.id == checkup_id)
    else:
        sel = sel.order_by(checkups.c.date.desc()).limit(1)

    with engine.connect() as conn:
        chk = conn.execute(sel).mappings().fetchone()
        if not chk:
            return None, None, None

        cond_sel = conditions.select().where(conditions.c.checkup_id == chk["id"]).limit(1)
        cond = conn.execute(cond_sel).mappings().fetchone()

        user_sel = users.select().where(users.c.id == user_id).limit(1)
        usr = conn.execute(user_sel).mappings().fetchone()

    return chk, cond, usr


def generate_checkup_pdf(user_id: int, checkup_id: int = None) -> bytes:
    """Generate a PDF report for a user's health checkup."""
    chk, cond, usr = _fetch_checkup(user_id, checkup_id)
    if chk is None:
        raise ValueError("No checkup data found for the requested user.")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0077b6"),
        alignment=0,
    )
    h2_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1a1a2e"),
        spaceBefore=12,
        spaceAfter=6,
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#64748b"),
        fontName="Helvetica-Oblique",
    )

    elems = []

    # Title & Metadata
    elems.append(Paragraph("🏥 Health Checkup Assessment Report", title_style))
    elems.append(Spacer(1, 6))

    patient_name = usr["username"] if usr else f"User #{user_id}"
    date_str = chk["date"].strftime("%B %d, %Y - %I:%M %p") if chk["date"] else "-"

    meta_data = [
        ["Patient Account:", patient_name, "Report Date:", date_str],
        ["Assessment ID:", f"CHK-{chk['id']}", "Platform:", "Health Checkup Program"],
    ]
    meta_table = Table(meta_data, colWidths=[110, 150, 100, 170])
    meta_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#555555")),
        ("TEXTCOLOR", (2, 0), (2, -1), colors.HexColor("#555555")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elems.append(meta_table)
    elems.append(Spacer(1, 10))

    # 1. Physical Measurements & Vitals
    elems.append(Paragraph("1. Physical Measurements & Vitals", h2_style))
    bp_val = chk["blood_pressure"]
    if not bp_val and chk["systolic"] and chk["diastolic"]:
        bp_val = f"{chk['systolic']}/{chk['diastolic']} mmHg"

    vitals_data = [
        ["Metric", "Recorded Value", "Reference Range / Status"],
        ["Height", f"{chk['height_cm']} cm", "Standard"],
        ["Weight", f"{chk['weight_kg']} kg", "Standard"],
        ["Body Mass Index (BMI)", f"{chk['bmi']:.2f} kg/m²", "18.5 - 24.9 (Adult Normal)"],
        ["Blood Pressure", bp_val or "Not Recorded", "< 120/80 mmHg (Normal)"],
        ["Resting Heart Rate", f"{chk['heart_rate']} bpm" if chk['heart_rate'] else "Not Recorded", "60 - 100 bpm"],
        ["Body Temperature", f"{chk['temperature']} °C" if chk['temperature'] else "Not Recorded", "36.5 - 37.5 °C"],
    ]
    vitals_table = Table(vitals_data, colWidths=[160, 150, 220])
    vitals_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6f7ff")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0077b6")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elems.append(vitals_table)
    elems.append(Spacer(1, 10))

    # 2. Lifestyle Habits
    elems.append(Paragraph("2. Daily Lifestyle Indicators", h2_style))
    lifestyle_data = [
        ["Habit", "Reported Level", "Habit", "Reported Level"],
        ["Average Sleep", f"{chk['sleep_hours']} hrs/day", "Daily Water Intake", f"{chk['water_intake']} glasses/day"],
        ["Weekly Exercise", f"{chk['exercise_days']} days/week", "Perceived Stress", chk['stress_level'] or "Moderate"],
        ["Smoking Status", chk['smoking'] or "Never", "Alcohol Consumption", chk['alcohol'] or "Never"],
    ]
    lifestyle_table = Table(lifestyle_data, colWidths=[130, 135, 130, 135])
    lifestyle_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f8fafc")),
        ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#f8fafc")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elems.append(lifestyle_table)
    elems.append(Spacer(1, 10))

    # 3. Medical History & Documented Conditions
    elems.append(Paragraph("3. Medical Background", h2_style))
    cond_list = []
    if cond:
        if cond["diabetes"]: cond_list.append("Diabetes")
        if cond["hypertension"]: cond_list.append("Hypertension")
        if cond["asthma"]: cond_list.append("Asthma")
        if cond["heart_disease"]: cond_list.append("Heart Disease")
        if cond["thyroid"]: cond_list.append("Thyroid")
    cond_text = ", ".join(cond_list) if cond_list else "None Reported"

    allergies_text = chk.get("allergies") or "None Reported"
    meds_text = chk.get("medications") or "None Reported"
    fam_text = chk.get("family_history") or "None Reported"

    history_data = [
        ["Chronic Conditions", cond_text],
        ["Known Allergies", allergies_text],
        ["Current Medications", meds_text],
        ["Family Medical History", fam_text],
    ]
    history_table = Table(history_data, colWidths=[160, 370])
    history_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elems.append(history_table)
    elems.append(Spacer(1, 14))

    # 4. Medical Disclaimer
    elems.append(Paragraph("Important Medical Notice & Educational Disclaimer", h2_style))
    disclaimer_text = (
        "This Health Checkup Assessment is generated automatically for educational and general wellness awareness only. "
        "It is NOT a medical diagnosis, clinical prognosis, or prescription for treatment. "
        "Adult BMI calculations do not apply to minors (< 18 years). "
        "Always seek the direct guidance of a licensed physician or healthcare professional for any health-related questions."
    )
    elems.append(Paragraph(disclaimer_text, disclaimer_style))

    doc.build(elems)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
