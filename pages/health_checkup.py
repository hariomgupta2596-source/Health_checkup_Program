import streamlit as st
from datetime import datetime

def render():
    """Health Checkup form page"""
    st.header("📋 Health Checkup Form")
    st.markdown("Complete your comprehensive health assessment")

    with st.form("health_checkup_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Personal Information")
            name = st.text_input("Full Name", placeholder="John Doe")
            age = st.number_input("Age", min_value=1, max_value=120, value=30)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with col2:
            st.subheader("Physical Measurements")
            height_cm = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
            weight_kg = st.number_input("Weight (kg)", min_value=20, max_value=200, value=70)
            blood_pressure = st.text_input("Blood Pressure (e.g., 120/80)", value="120/80")
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Health Metrics")
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=72)
            temperature = st.number_input("Body Temperature (°C)", min_value=35.0, max_value=42.0, value=37.0, step=0.1)
        with col2:
            st.subheader("Lifestyle Habits")
            sleep_hours = st.slider("Average Sleep (hours/day)", 0, 12, 7)
            exercise_days = st.slider("Exercise Days (per week)", 0, 7, 3)
            water_intake = st.slider("Water Intake (glasses/day)", 0, 15, 8)
        st.divider()
        st.subheader("Health Conditions")
        col1, col2, col3 = st.columns(3)
        with col1:
            diabetes = st.checkbox("Diabetes")
            hypertension = st.checkbox("Hypertension")
        with col2:
            asthma = st.checkbox("Asthma")
            heart_disease = st.checkbox("Heart Disease")
        with col3:
            thyroid = st.checkbox("Thyroid")
            other_conditions = st.text_input("Other Conditions", placeholder="If any")
        st.divider()
        st.subheader("Lifestyle Factors")
        smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
        alcohol = st.selectbox("Alcohol Consumption", ["Never", "Rarely", "Occasionally", "Regularly"])
        stress_level = st.select_slider("Stress Level", options=["Low", "Moderate", "High", "Very High"])
        st.divider()
        submitted = st.form_submit_button("Submit Checkup", use_container_width=True)

        if not st.session_state.get("user_id"):
        st.warning("🔒 Please log in to submit a health checkup.")
        st.stop()
    if submitted and name:
        bmi = weight_kg / ((height_cm / 100) ** 2)
        # Prepare data dict for persistence
        data = {
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "bmi": round(bmi, 2),
            "blood_pressure": blood_pressure,
            "heart_rate": heart_rate,
            "temperature": temperature,
            "sleep_hours": sleep_hours,
            "exercise_days": exercise_days,
            "water_intake": water_intake,
            "smoking": smoking,
            "alcohol": alcohol,
            "stress_level": stress_level,
            "other_conditions": other_conditions,
            "diabetes": diabetes,
            "hypertension": hypertension,
            "asthma": asthma,
            "heart_disease": heart_disease,
            "thyroid": thyroid,
        }
        # Save to DB
        from modules.health_checkup import save_checkup
        checkup_id = save_checkup(st.session_state.user_id, data)
        st.success("✅ Health Checkup Submitted Successfully!")
        st.divider()
        st.subheader("📊 Your Health Assessment Results")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            bmi_status = "Normal" if 18.5 <= bmi < 25 else ("Underweight" if bmi < 18.5 else ("Overweight" if bmi < 30 else "Obese"))
            st.metric("BMI", f"{bmi}", bmi_status)
        with col2:
            hr_status = "Normal" if 60 <= heart_rate <= 100 else "Check with Doctor"
            st.metric("Heart Rate", f"{heart_rate} bpm", hr_status)
        with col3:
            temp_status = "Normal" if 36.5 <= temperature <= 37.5 else "Abnormal"
            st.metric("Temperature", f"{temperature}°C", temp_status)
        with col4:
            st.metric("Blood Pressure", blood_pressure, "Monitor")
        st.divider()
        st.subheader("💡 Personalized Recommendations")
        recommendations = []
        if bmi >= 25:
            recommendations.append("🍎 Increase physical activity and maintain a balanced diet")
        if heart_rate > 100 or heart_rate < 60:
            recommendations.append("❤️ Consult a doctor about your heart rate")
        if sleep_hours < 7:
            recommendations.append("😴 Aim for 7-9 hours of sleep per night")
        if exercise_days < 3:
            recommendations.append("🏃 Try to exercise at least 3-4 days per week")
        if stress_level in ["High", "Very High"]:
            recommendations.append("🧘 Practice stress management techniques like meditation")
        if smoking == "Current":
            recommendations.append("🚭 Consider quitting smoking for better health")
        if water_intake < 8:
            recommendations.append("💧 Increase water intake to at least 8 glasses per day")
        if not recommendations:
            st.info("✨ Great! Keep maintaining your healthy lifestyle!")
        else:
            for rec in recommendations:
                st.info(rec)
