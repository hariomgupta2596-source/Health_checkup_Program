import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(
    page_title="Health Checkup Program",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .health-good { color: #28a745; font-weight: bold; }
    .health-warning { color: #ffc107; font-weight: bold; }
    .health-danger { color: #dc3545; font-weight: bold; }
    </style>
""")

# Initialize session state
if 'checkups' not in st.session_state:
    st.session_state.checkups = []

# Title and description
st.title("🏥 Health Checkup Program")
st.markdown("### Comprehensive Health Assessment & Monitoring System")
st.divider()

# Sidebar navigation
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Health Checkup", "Health Dashboard", "Reports", "Guidelines"]
)

# ============================================================================
# HOME PAGE
# ============================================================================
if page == "Home":
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2912/2912033.png", 
                width=200, caption="Health Checkup")
    
    with col2:
        st.markdown("""
        ## Welcome to Health Checkup Program
        
        This comprehensive health assessment tool helps you:
        - ✅ Monitor your vital health metrics
        - ✅ Get personalized health recommendations
        - ✅ Track health progress over time
        - ✅ Understand BMI and health status
        - ✅ Access health guidelines and tips
        
        ### Quick Features:
        - **Health Assessment**: Complete health checkup questionnaire
        - **Dashboard**: Visual representation of your health metrics
        - **Reports**: Detailed health reports and history
        - **Guidelines**: Evidence-based health recommendations
        """)
    
    st.divider()
    
    # Key statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Checkups", len(st.session_state.checkups), "+1 checkup")
    with col2:
        st.metric("Status", "Active", "✓")
    with col3:
        st.metric("Last Updated", datetime.now().strftime("%Y-%m-%d"))

# ============================================================================
# HEALTH CHECKUP PAGE
# ============================================================================
elif page == "Health Checkup":
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
        
        # Submit button
        submitted = st.form_submit_button("Submit Checkup", use_container_width=True)
        
        if submitted and name:
            # Calculate BMI
            bmi = weight_kg / ((height_cm / 100) ** 2)
            
            # Create checkup record
            checkup = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": name,
                "age": age,
                "gender": gender,
                "height_cm": height_cm,
                "weight_kg": weight_kg,
                "bmi": round(bmi, 2),
                "blood_pressure": blood_pressure,
                "heart_rate": heart_rate,
                "temperature": temperature,
                "sleep_hours": sleep_hours,
                "exercise_days": exercise_days,
                "water_intake": water_intake,
                "conditions": [diabetes, hypertension, asthma, heart_disease, thyroid],
                "other_conditions": other_conditions,
                "smoking": smoking,
                "alcohol": alcohol,
                "stress_level": stress_level
            }
            
            st.session_state.checkups.append(checkup)
            st.success("✅ Health Checkup Submitted Successfully!")
            
            # Display results
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
            
            # Health recommendations
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
            
            if len(recommendations) == 0:
                st.info("✨ Great! Keep maintaining your healthy lifestyle!")
            else:
                for rec in recommendations:
                    st.info(rec)

# ============================================================================
# HEALTH DASHBOARD PAGE
# ============================================================================
elif page == "Health Dashboard":
    st.header("📊 Health Dashboard")
    
    if len(st.session_state.checkups) == 0:
        st.warning("No checkup data available. Please complete a health checkup first!")
    else:
        # Get latest checkup
        latest = st.session_state.checkups[-1]
        
        st.markdown(f"### Latest Checkup: {latest['date']}")
        st.markdown(f"**Patient**: {latest['name']} | **Age**: {latest['age']} | **Gender**: {latest['gender']}")
        
        st.divider()
        
        # Metrics overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            bmi_status = "Normal" if 18.5 <= latest['bmi'] < 25 else ("Underweight" if latest['bmi'] < 18.5 else ("Overweight" if latest['bmi'] < 30 else "Obese"))
            st.metric("BMI", f"{latest['bmi']}", bmi_status)
        
        with col2:
            st.metric("Heart Rate", f"{latest['heart_rate']} bpm", "Pulse")
        
        with col3:
            st.metric("Temperature", f"{latest['temperature']}°C", "Body Temp")
        
        with col4:
            st.metric("Blood Pressure", latest['blood_pressure'], "BP")
        
        st.divider()
        
        # Lifestyle metrics
        st.subheader("🏃 Lifestyle Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Sleep", f"{latest['sleep_hours']} hrs/day", "Recommended: 7-9 hrs")
        
        with col2:
            st.metric("Exercise", f"{latest['exercise_days']} days/week", "Recommended: 3-5 days")
        
        with col3:
            st.metric("Water Intake", f"{latest['water_intake']} glasses/day", "Recommended: 8 glasses")
        
        st.divider()
        
        # Health history
        st.subheader("📈 Checkup History")
        
        df_history = pd.DataFrame([
            {
                "Date": c["date"],
                "Name": c["name"],
                "BMI": c["bmi"],
                "Heart Rate": c["heart_rate"],
                "Weight (kg)": c["weight_kg"],
                "Sleep (hrs)": c["sleep_hours"],
                "Stress Level": c["stress_level"]
            }
            for c in st.session_state.checkups
        ])
        
        st.dataframe(df_history, use_container_width=True)

# ============================================================================
# REPORTS PAGE
# ============================================================================
elif page == "Reports":
    st.header("📄 Health Reports")
    
    if len(st.session_state.checkups) == 0:
        st.warning("No checkup data available. Please complete a health checkup first!")
    else:
        # Report selection
        report_type = st.selectbox("Select Report Type", ["Summary Report", "BMI Report", "Vitals Report", "Lifestyle Report"])
        
        latest = st.session_state.checkups[-1]
        
        st.divider()
        
        if report_type == "Summary Report":
            st.markdown(f"""
            ## Health Summary Report
            **Generated on**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            
            ### Patient Information
            - **Name**: {latest['name']}
            - **Age**: {latest['age']} years
            - **Gender**: {latest['gender']}
            
            ### Physical Measurements
            - **Height**: {latest['height_cm']} cm
            - **Weight**: {latest['weight_kg']} kg
            - **BMI**: {latest['bmi']} ({'Normal' if 18.5 <= latest['bmi'] < 25 else ('Underweight' if latest['bmi'] < 18.5 else ('Overweight' if latest['bmi'] < 30 else 'Obese'))})
            
            ### Vital Signs
            - **Blood Pressure**: {latest['blood_pressure']} mmHg
            - **Heart Rate**: {latest['heart_rate']} bpm
            - **Temperature**: {latest['temperature']} °C
            
            ### Lifestyle Information
            - **Sleep**: {latest['sleep_hours']} hours/day
            - **Exercise**: {latest['exercise_days']} days/week
            - **Water Intake**: {latest['water_intake']} glasses/day
            - **Smoking**: {latest['smoking']}
            - **Alcohol**: {latest['alcohol']}
            - **Stress Level**: {latest['stress_level']}
            """)
        
        elif report_type == "BMI Report":
            st.markdown(f"""
            ## BMI Analysis Report
            
            **BMI Score**: {latest['bmi']}
            
            ### Classification
            """)
            
            bmi = latest['bmi']
            if bmi < 18.5:
                st.markdown("**Status**: UNDERWEIGHT ⚠️")
                st.markdown("""
                **Recommendations**:
                - Consult a nutritionist to develop a healthy weight gain plan
                - Include nutrient-dense foods in your diet
                - Engage in strength training exercises
                """)
            elif 18.5 <= bmi < 25:
                st.markdown("**Status**: NORMAL WEIGHT ✅")
                st.markdown("Congratulations! Your BMI is in the healthy range. Maintain your current lifestyle!")
            elif 25 <= bmi < 30:
                st.markdown("**Status**: OVERWEIGHT ⚠️")
                st.markdown("""
                **Recommendations**:
                - Increase physical activity to 150 minutes per week
                - Adopt a balanced, low-calorie diet
                - Monitor portion sizes
                """)
            else:
                st.markdown("**Status**: OBESE 🚨")
                st.markdown("""
                **Recommendations**:
                - Consult with a healthcare provider
                - Develop a comprehensive weight loss plan
                - Increase physical activity gradually
                - Seek support from a dietitian
                """)
        
        elif report_type == "Vitals Report":
            st.markdown(f"""
            ## Vital Signs Report
            
            ### Blood Pressure: {latest['blood_pressure']} mmHg
            - Normal: < 120/80
            - Elevated: 120-129/<80
            - High BP Stage 1: 130-139/80-89
            - High BP Stage 2: ≥ 140/≥ 90
            
            ### Heart Rate: {latest['heart_rate']} bpm
            - Normal Resting: 60-100 bpm
            - Current Status: {'Normal ✅' if 60 <= latest['heart_rate'] <= 100 else 'Abnormal ⚠️'}
            
            ### Body Temperature: {latest['temperature']} °C
            - Normal Range: 36.5-37.5 °C
            - Current Status: {'Normal ✅' if 36.5 <= latest['temperature'] <= 37.5 else 'Abnormal ⚠️'}
            """)
        
        elif report_type == "Lifestyle Report":
            st.markdown(f"""
            ## Lifestyle Analysis Report
            
            ### Sleep Quality
            - Current: {latest['sleep_hours']} hours/day
            - Recommended: 7-9 hours/day
            - Status: {'✅ Good' if 7 <= latest['sleep_hours'] <= 9 else '⚠️ Needs Improvement'}
            
            ### Physical Activity
            - Current: {latest['exercise_days']} days/week
            - Recommended: 3-5 days/week (150+ minutes)
            - Status: {'✅ Good' if 3 <= latest['exercise_days'] <= 5 else '⚠️ Needs Improvement'}
            
            ### Hydration
            - Current: {latest['water_intake']} glasses/day
            - Recommended: 8-10 glasses/day
            - Status: {'✅ Good' if latest['water_intake'] >= 8 else '⚠️ Needs Improvement'}
            
            ### Stress Management
            - Current Level: {latest['stress_level']}
            - Recommended: Low to Moderate
            - Status: {'✅ Good' if latest['stress_level'] in ['Low', 'Moderate'] else '⚠️ Needs Attention'}
            
            ### Smoking Status: {latest['smoking']}
            - Recommended: Never Smoke
            
            ### Alcohol Consumption: {latest['alcohol']}
            - Recommended: Minimal or No Consumption
            """)
        
        st.divider()
        
        # Download option
        if st.button("📥 Download Report as Text"):
            report_text = f"Health Checkup Report\nGenerated: {datetime.now()}\n\nPatient: {latest['name']}\nAge: {latest['age']}\nBMI: {latest['bmi']}\n"
            st.download_button(
                label="Click to download",
                data=report_text,
                file_name=f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

# ============================================================================
# GUIDELINES PAGE
# ============================================================================
elif page == "Guidelines":
    st.header("📚 Health Guidelines & Tips")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Nutrition", "Exercise", "Sleep", "Stress", "Prevention"])
    
    with tab1:
        st.subheader("🍎 Nutrition Guidelines")
        st.markdown("""
        ### Balanced Diet Components:
        
        1. **Fruits & Vegetables** (5 servings/day)
           - Provide vitamins, minerals, and fiber
           - Aim for variety of colors
        
        2. **Whole Grains** (6 servings/day)
           - Brown rice, whole wheat bread, oats
           - Rich in fiber and nutrients
        
        3. **Protein** (1.6-2.2g per kg of body weight)
           - Lean meats, fish, eggs, legumes
           - Essential for muscle maintenance
        
        4. **Dairy** (2-3 servings/day)
           - Milk, yogurt, cheese
           - Important for bone health
        
        5. **Healthy Fats**
           - Olive oil, avocados, nuts
           - Limit saturated fats to <10% of calories
        
        ### Foods to Limit:
        - Sugary drinks and snacks
        - Processed meats
        - High-sodium foods
        - Excessive caffeine
        """)
    
    with tab2:
        st.subheader("🏃 Exercise Guidelines")
        st.markdown("""
        ### WHO Recommendations (for 18-65 years):
        
        1. **Aerobic Activity** (150-300 minutes/week)
           - Brisk walking, running, cycling, swimming
           - Choose activities you enjoy
        
        2. **Strength Training** (2 days/week)
           - Weight lifting, bodyweight exercises
           - Builds muscle and bone density
        
        3. **Flexibility** (Daily)
           - Stretching, yoga
           - Maintains range of motion
        
        ### Tips for Success:
        - Start slowly and gradually increase intensity
        - Exercise with a friend for motivation
        - Choose activities you enjoy
        - Rest 1-2 days per week
        - Warm up before and cool down after
        """)
    
    with tab3:
        st.subheader("😴 Sleep Guidelines")
        st.markdown("""
        ### Recommended Sleep Duration:
        - **Adults (18-64 years)**: 7-9 hours/night
        - **Older Adults (65+ years)**: 7-8 hours/night
        
        ### Tips for Better Sleep:
        1. **Consistent Schedule**
           - Go to bed and wake up at the same time daily
           - Even on weekends
        
        2. **Sleep Environment**
           - Keep bedroom dark, cool (16-19°C), and quiet
           - Use comfortable bedding
        
        3. **Pre-sleep Routine**
           - Avoid screens 1 hour before bed
           - Try relaxation techniques
           - Avoid caffeine after 2 PM
        
        4. **Lifestyle Habits**
           - Regular exercise (but not close to bedtime)
           - Limit naps to 20-30 minutes
           - Avoid alcohol and heavy meals before sleep
        
        ### Signs of Sleep Disorder:
        - Persistent insomnia
        - Excessive daytime sleepiness
        - Snoring or breathing interruptions
        - Consult a doctor if issues persist
        """)
    
    with tab4:
        st.subheader("🧘 Stress Management")
        st.markdown("""
        ### Stress Management Techniques:
        
        1. **Mindfulness & Meditation**
           - Practice 10-20 minutes daily
           - Helps reduce anxiety and improve focus
        
        2. **Physical Activity**
           - Releases endorphins (natural mood elevators)
           - Reduces cortisol (stress hormone)
        
        3. **Breathing Exercises**
           - Deep breathing: Inhale for 4, hold for 4, exhale for 4
           - Practice 5-10 minutes daily
        
        4. **Time Management**
           - Prioritize important tasks
           - Break large projects into smaller steps
           - Take regular breaks
        
        5. **Social Connection**
           - Spend time with friends and family
           - Join clubs or groups with shared interests
        
        6. **Professional Help**
           - Consult a therapist if stress is overwhelming
           - Don't hesitate to seek support
        """)
    
    with tab5:
        st.subheader("🛡️ Disease Prevention")
        st.markdown("""
        ### Prevention Strategies:
        
        1. **Cardiovascular Health**
           - Maintain healthy weight (BMI 18.5-24.9)
           - Control blood pressure and cholesterol
           - Limit salt intake to <5g/day
        
        2. **Diabetes Prevention**
           - Maintain healthy weight
           - Exercise regularly
           - Eat whole grains and reduce sugar
        
        3. **Cancer Prevention**
           - Avoid tobacco and excessive alcohol
           - Eat plenty of fruits and vegetables
           - Get regular screenings
        
        4. **Regular Checkups**
           - Annual health screening
           - Dental checkup every 6 months
           - Vision check as recommended
        
        5. **Vaccination**
           - Seasonal flu vaccine annually
           - Follow recommended vaccination schedule
        
        6. **Mental Health**
           - Regular exercise and sleep
           - Social connections
           - Seek professional help when needed
        """)

st.divider()
st.markdown("""
---
**Disclaimer**: This Health Checkup Program is for informational purposes only and should not replace professional medical advice. 
Always consult with a qualified healthcare provider for diagnosis and treatment.

**Last Updated**: 2024 | **Version**: 1.0
""")
