"""PDF report generation utilities using ReportLab.

The main function `generate_checkup_pdf(user_id, checkup_id=None)` creates a PDF
containing the most recent checkup (or a specific one if `checkup_id` is
provided). It returns the PDF as a `bytes` object that can be fed directly to
`st.download_button`.
"""
import io
from datetime import datetime

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

from database.db_connection import engine
from database.db_setup import checkups, conditions

def _fetch_checkup(user_id: int, checkup_id: int = None):
    """Retrieve a checkup record (and its conditions) from the DB.

    If ``checkup_id`` is ``None`` the latest checkup for the user is returned.
    Returns ``(checkup_row, condition_row)`` where each is a SQLAlchemy RowMapping.
    """
    # Base select for checkup
    sel = checkups.select().where(checkups.c.user_id == user_id)
    if checkup_id is not None:
        sel = sel.where(checkups.c.id == checkup_id)
    else:
        sel = sel.order_by(checkups.c.date.desc()).limit(1)
    with engine.connect() as conn:
        chk = conn.execute(sel).fetchone()
        if not chk:
            return None, None
        # Fetch conditions for this checkup
        cond_sel = conditions.select().where(conditions.c.checkup_id == chk["id"]).limit(1)
        cond = conn.execute(cond_sel).fetchone()
    return chk, cond

def generate_checkup_pdf(user_id: int, checkup_id: int = None) -> bytes:
    """Generate a PDF report for a user's health checkup.

    Parameters
    ----------
    user_id: int
        Authenticated user ID.
    checkup_id: int, optional
        Specific checkup to print. If omitted, the latest checkup is used.
    Returns
    -------
    bytes
        PDF data ready for download.
    """
    chk, cond = _fetch_checkup(user_id, checkup_id)
    if chk is None:
        raise ValueError("No checkup data found for the requested user.")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=LETTER)
    styles = getSampleStyleSheet()
    elems = []

    # Title & metadata
    elems.append(Paragraph("Health Checkup Report", styles["Title"]))
    elems.append(Spacer(1, 12))
    elems.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    elems.append(Spacer(1, 12))

    # Basic info table
    data = [
        ["Date", chk["date"].strftime("%Y-%m-%d %H:%M")],
        ["Height (cm)", f"{chk["height_cm"]:.1f}"],
        ["Weight (kg)", f"{chk["weight_kg"]:.1f}"],
        ["BMI", f"{chk["bmi"]:.2f}"],
        ["Blood Pressure", chk["blood_pressure"] or "-"],
        ["Heart Rate (bpm)", chk["heart_rate"] or "-"],
        ["Temperature (°C)", chk["temperature"] or "-"],
        ["Sleep (hrs/day)", chk["sleep_hours"] or "-"],
        ["Exercise (days/week)", chk["exercise_days"] or "-"],
        ["Water Intake (glasses/day)", chk["water_intake"] or "-"],
        ["Smoking", chk["smoking"] or "-"],
        ["Alcohol", chk["alcohol"] or "-"],
        ["Stress Level", chk["stress_level"] or "-"],
        ["Other Conditions", chk["other_conditions"] or "-"],
    ]
    tbl = Table(data, hAlign="LEFT", colWidths=[150, 250])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
    ]))
    elems.append(tbl)
    elems.append(Spacer(1, 12))

    # Condition flags, if present
    if cond:
        elems.append(Paragraph("Medical Conditions", styles["Heading2"]))
        cond_data = [
            ["Diabetes", "Yes" if cond["diabetes"] else "No"],
            ["Hypertension", "Yes" if cond["hypertension"] else "No"],
            ["Asthma", "Yes" if cond["asthma"] else "No"],
            ["Heart Disease", "Yes" if cond["heart_disease"] else "No"],
            ["Thyroid", "Yes" if cond["thyroid"] else "No"],
        ]
        cond_tbl = Table(cond_data, hAlign="LEFT", colWidths=[150, 250])
        cond_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elems.append(cond_tbl)
        elems.append(Spacer(1, 12))

    # Disclaimer
    elems.append(Paragraph(
        "This report is for educational purposes only and does not replace professional medical advice.",
        styles["Italic"],
    ))

    doc.build(elems)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
