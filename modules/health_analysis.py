"""Health analysis and recommendation logic.
Provides a simple rule‑based engine that receives a dict of health data and
returns a list of human‑readable recommendations.
"""
from typing import List, Dict, Any

def get_recommendations(data: Dict[str, Any]) -> List[str]:
    """Generate wellness recommendations based on the health data.

    Parameters
    ----------
    data: dict
        Keys expected: ``bmi``, ``heart_rate``, ``sleep_hours``, ``exercise_days``,
        ``stress_level``, ``smoking``, ``water_intake``.
    Returns
    -------
    List[str]
        Recommendation strings.
    """
    recommendations: List[str] = []
    bmi = data.get("bmi")
    if bmi is not None and bmi >= 25:
        recommendations.append("🍎 Increase physical activity and maintain a balanced diet")
    heart_rate = data.get("heart_rate")
    if heart_rate is not None and (heart_rate > 100 or heart_rate < 60):
        recommendations.append("❤️ Consult a doctor about your heart rate")
    sleep = data.get("sleep_hours")
    if sleep is not None and sleep < 7:
        recommendations.append("😴 Aim for 7-9 hours of sleep per night")
    exercise = data.get("exercise_days")
    if exercise is not None and exercise < 3:
        recommendations.append("🏃 Try to exercise at least 3-4 days per week")
    stress = data.get("stress_level")
    if stress in ("High", "Very High"):
        recommendations.append("🧘 Practice stress management techniques like meditation")
    smoking = data.get("smoking")
    if smoking == "Current":
        recommendations.append("🚭 Consider quitting smoking for better health")
    water = data.get("water_intake")
    if water is not None and water < 8:
        recommendations.append("💧 Increase water intake to at least 8 glasses per day")
    return recommendations
