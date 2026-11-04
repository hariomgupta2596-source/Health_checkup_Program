"""Health analysis and recommendation logic.
Provides a rule-based educational awareness engine for vitals, lifestyle habits, and general wellness.

Notice: This engine provides informational guidelines only and does not diagnose disease
or prescribe medical treatment.
"""
from typing import List, Dict, Any, Optional
from modules.bmi_calculator import calculate_bmi, classify_bmi


def evaluate_blood_pressure(systolic: Optional[int], diastolic: Optional[int]) -> Dict[str, Any]:
    """Evaluate blood pressure according to AHA/ACC guidelines."""
    if systolic is None or diastolic is None or systolic <= 0 or diastolic <= 0:
        return {"category": "Not Recorded", "status": "Unknown", "color": "#64748b"}

    if systolic < 120 and diastolic < 80:
        return {
            "category": "Normal",
            "status": "Healthy Reference Range",
            "color": "#22c55e",
            "detail": "Systolic < 120 mmHg and diastolic < 80 mmHg.",
        }
    elif 120 <= systolic <= 129 and diastolic < 80:
        return {
            "category": "Elevated",
            "status": "Mildly Elevated",
            "color": "#eab308",
            "detail": "Systolic 120-129 mmHg and diastolic < 80 mmHg. Lifestyle and dietary sodium moderation recommended.",
        }
    elif (130 <= systolic <= 139) or (80 <= diastolic <= 89):
        return {
            "category": "Stage 1 Hypertension",
            "status": "Stage 1 (Reference)",
            "color": "#f97316",
            "detail": "Systolic 130-139 mmHg or diastolic 80-89 mmHg. Review with a medical doctor.",
        }
    else:
        return {
            "category": "Stage 2 Hypertension",
            "status": "Stage 2 (Reference)",
            "color": "#ef4444",
            "detail": "Systolic >= 140 mmHg or diastolic >= 90 mmHg. Clinical evaluation advised.",
        }


def evaluate_heart_rate(heart_rate: Optional[int]) -> Dict[str, Any]:
    """Evaluate resting heart rate in bpm."""
    if not heart_rate or heart_rate <= 0:
        return {"category": "Not Recorded", "status": "Unknown", "color": "#64748b"}

    if heart_rate < 60:
        return {
            "category": "Bradycardia (< 60 bpm)",
            "status": "Low Resting Pulse",
            "color": "#0284c7",
            "detail": "Common in endurance athletes; if accompanied by dizziness, check with a doctor.",
        }
    elif 60 <= heart_rate <= 100:
        return {
            "category": "Normal (60-100 bpm)",
            "status": "Normal Resting Pulse",
            "color": "#22c55e",
            "detail": "Standard adult resting pulse range.",
        }
    else:
        return {
            "category": "Tachycardia (> 100 bpm)",
            "status": "Elevated Pulse",
            "color": "#ef4444",
            "detail": "Higher than typical resting range; consider caffeine, hydration, or medical review.",
        }


def evaluate_temperature(temp_c: Optional[float]) -> Dict[str, Any]:
    """Evaluate body temperature in Celsius."""
    if not temp_c or temp_c <= 0:
        return {"category": "Not Recorded", "status": "Unknown", "color": "#64748b"}

    if temp_c < 36.0:
        return {"category": "Low (< 36.0°C)", "status": "Subnormal", "color": "#0284c7"}
    elif 36.0 <= temp_c <= 37.5:
        return {"category": "Normal (36.5 - 37.5°C)", "status": "Normal", "color": "#22c55e"}
    elif 37.5 < temp_c <= 38.3:
        return {"category": "Low-grade fever (37.6 - 38.3°C)", "status": "Elevated", "color": "#f97316"}
    else:
        return {"category": "Fever (> 38.3°C)", "status": "Fever", "color": "#ef4444"}


def get_comprehensive_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate comprehensive educational analysis across vitals, BMI, and lifestyle."""
    age = data.get("age", 30)
    height_cm = data.get("height_cm", 0.0)
    weight_kg = data.get("weight_kg", 0.0)
    bmi = data.get("bmi") or calculate_bmi(height_cm, weight_kg)

    bmi_eval = classify_bmi(bmi, age)
    bp_eval = evaluate_blood_pressure(data.get("systolic"), data.get("diastolic"))
    hr_eval = evaluate_heart_rate(data.get("heart_rate"))
    temp_eval = evaluate_temperature(data.get("temperature"))

    recommendations: List[str] = []

    # BMI recommendations
    if not bmi_eval.get("is_pediatric"):
        if bmi >= 25.0:
            recommendations.append("🍎 Maintain a balanced, nutrient-rich diet and aim for at least 150 minutes of moderate aerobic activity weekly.")
        elif bmi < 18.5:
            recommendations.append("🥑 Consider consulting a registered dietitian to develop a healthy, nutrient-dense caloric intake plan.")

    # Blood Pressure
    if bp_eval.get("category") in ("Stage 1 Hypertension", "Stage 2 Hypertension"):
        recommendations.append("🩺 Monitor blood pressure regularly at the same time each day and schedule a routine checkup with a physician.")

    # Heart Rate
    if hr_eval.get("category") and "Tachycardia" in hr_eval["category"]:
        recommendations.append("❤️ Your resting pulse was elevated; ensure adequate rest, moderate caffeine, and consult a doctor if persistent.")

    # Sleep
    sleep = data.get("sleep_hours")
    if sleep is not None:
        if sleep < 7:
            recommendations.append("😴 Aim for 7-9 hours of consistent sleep per night; prioritize a screen-free winding down routine.")
        elif sleep > 10:
            recommendations.append("🛌 Excessive daytime sleepiness or 10+ hours regularly may warrant discussing sleep quality with a healthcare provider.")

    # Physical Activity
    exercise = data.get("exercise_days")
    if exercise is not None and exercise < 3:
        recommendations.append("🏃 Incorporate regular physical movement—even a brisk 20-30 minute walk 3-5 days per week provides cardiovascular benefits.")

    # Hydration
    water = data.get("water_intake")
    if water is not None and water < 8:
        recommendations.append("💧 Increase hydration toward 8 glasses (approx. 2 liters) of water daily, especially when physically active.")

    # Stress
    stress = data.get("stress_level")
    if stress in ("High", "Very High"):
        recommendations.append("🧘 Practice stress management techniques such as box breathing, mindfulness, and taking structured breaks during work.")

    # Smoking / Alcohol
    if data.get("smoking") == "Current":
        recommendations.append("🚭 Quitting tobacco significantly reduces cardiovascular and respiratory risks; consult your clinician for cessation resources.")
    if data.get("alcohol") in ("Frequently", "Regularly"):
        recommendations.append("🍷 Limiting alcohol intake promotes restorative sleep, optimal liver function, and healthy blood pressure levels.")

    # Medical history observations
    allergies = data.get("allergies")
    if allergies and allergies.strip():
        recommendations.append(f"⚠️ Documented allergies: {allergies.strip()}. Always confirm medication safety with pharmacists and doctors.")

    if not recommendations:
        recommendations.append("✨ Great habits recorded! Keep up your balanced lifestyle, hydration, and regular checkups.")

    return {
        "bmi": bmi,
        "bmi_eval": bmi_eval,
        "bp_eval": bp_eval,
        "hr_eval": hr_eval,
        "temp_eval": temp_eval,
        "recommendations": recommendations,
        "disclaimer": "This health assessment is for educational and wellness awareness only. It does not provide medical diagnosis or replace a professional clinical evaluation.",
    }


def get_recommendations(data: Dict[str, Any]) -> List[str]:
    """Compatibility wrapper returning list of recommendations."""
    return get_comprehensive_analysis(data)["recommendations"]
