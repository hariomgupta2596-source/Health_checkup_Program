import pytest
from modules.bmi_calculator import calculate_bmi, classify_bmi, get_healthy_weight_range
from modules.health_analysis import (
    evaluate_blood_pressure,
    evaluate_heart_rate,
    evaluate_temperature,
    get_comprehensive_analysis,
)


def test_calculate_bmi():
    # 70 kg at 170 cm -> 70 / (1.7^2) = 24.22
    bmi = calculate_bmi(170, 70)
    assert bmi == 24.22
    assert calculate_bmi(0, 70) == 0.0


def test_pediatric_bmi_awareness():
    # Minors under 18 must receive pediatric notice, not adult WHO categories
    eval_child = classify_bmi(22.0, age=12)
    assert eval_child["is_pediatric"] is True
    assert "Pediatric" in eval_child["status"]
    assert "Pediatric" in eval_child["note"]


def test_adult_bmi_categories():
    assert classify_bmi(17.5, age=25)["category"] == "Underweight"
    assert classify_bmi(22.5, age=25)["category"] == "Normal Weight"
    assert classify_bmi(27.5, age=25)["category"] == "Overweight"
    assert classify_bmi(32.5, age=25)["category"] == "Obesity (Class I)"


def test_healthy_weight_range():
    range_data = get_healthy_weight_range(170)
    assert range_data["min_kg"] == 53.5
    assert range_data["max_kg"] == 72.0


def test_blood_pressure_evaluation():
    norm = evaluate_blood_pressure(115, 75)
    assert norm["category"] == "Normal"

    elev = evaluate_blood_pressure(125, 75)
    assert elev["category"] == "Elevated"

    stg1 = evaluate_blood_pressure(135, 85)
    assert stg1["category"] == "Stage 1 Hypertension"

    stg2 = evaluate_blood_pressure(145, 95)
    assert stg2["category"] == "Stage 2 Hypertension"


def test_comprehensive_analysis_output():
    data = {
        "age": 32,
        "height_cm": 175,
        "weight_kg": 85,
        "systolic": 135,
        "diastolic": 85,
        "heart_rate": 75,
        "temperature": 36.8,
        "sleep_hours": 6,
        "exercise_days": 2,
        "water_intake": 6,
        "smoking": "Never",
        "alcohol": "Never",
        "stress_level": "Moderate",
        "allergies": "Penicillin",
    }
    analysis = get_comprehensive_analysis(data)
    assert "bmi" in analysis
    assert "recommendations" in analysis
    assert len(analysis["recommendations"]) > 0
    assert "educational" in analysis["disclaimer"].lower()
