"""BMI calculation and classification module.
Provides age-aware calculations, healthy weight range guidelines, and WHO classifications.
"""
from typing import Dict, Any


def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """Calculate Body Mass Index (kg/m²)."""
    if height_cm <= 0 or weight_kg <= 0:
        return 0.0
    height_m = height_cm / 100.0
    return round(weight_kg / (height_m ** 2), 2)


def get_healthy_weight_range(height_cm: float) -> Dict[str, float]:
    """Calculate the healthy weight range (BMI 18.5 - 24.9) for a given height in cm."""
    if height_cm <= 0:
        return {"min_kg": 0.0, "max_kg": 0.0}
    height_m = height_cm / 100.0
    min_weight = round(18.5 * (height_m ** 2), 1)
    max_weight = round(24.9 * (height_m ** 2), 1)
    return {"min_kg": min_weight, "max_kg": max_weight}


def classify_bmi(bmi: float, age: int = 30) -> Dict[str, Any]:
    """Classify BMI with age-appropriate awareness.
    
    Important: Adult BMI cutoff categories do NOT apply to children and teenagers (< 18).
    For minors, pediatric growth percentiles should be used by a pediatrician.
    """
    if age < 18:
        return {
            "status": "Pediatric Assessment Required",
            "category": "Minor (< 18 years)",
            "is_pediatric": True,
            "color": "#0284c7",
            "note": "Standard adult BMI categories do not apply to children or adolescents under 18. Pediatric growth charts and age/sex percentiles should be consulted with a pediatrician.",
        }

    if bmi < 18.5:
        category = "Underweight"
        color = "#eab308"
        note = "Below standard range. Consider speaking with a healthcare professional or nutritionist regarding balanced nutrient-dense meal plans."
    elif 18.5 <= bmi < 25.0:
        category = "Normal Weight"
        color = "#22c55e"
        note = "Within healthy WHO reference range. Continue balanced nutrition and regular physical activity."
    elif 25.0 <= bmi < 30.0:
        category = "Overweight"
        color = "#f97316"
        note = "Above standard reference range. Regular cardiovascular activity and portion-controlled nutrition are recommended."
    elif 30.0 <= bmi < 35.0:
        category = "Obesity (Class I)"
        color = "#ef4444"
        note = "Consult a physician or registered dietitian for a comprehensive personal wellness plan."
    else:
        category = "Obesity (Class II/III)"
        color = "#b91c1c"
        note = "Consult with a medical provider for structured guidance and cardiometabolic monitoring."

    return {
        "status": category,
        "category": category,
        "is_pediatric": False,
        "color": color,
        "note": note,
    }
