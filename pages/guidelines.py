import streamlit as st

def render():
    """Health Guidelines & Tips page – static educational content."""
    st.header("📚 Health Guidelines & Tips")

    # Use Streamlit tabs for each category (same as original implementation)
    tab_nutrition, tab_exercise, tab_sleep, tab_stress, tab_prevention = st.tabs([
        "Nutrition",
        "Exercise",
        "Sleep",
        "Stress",
        "Prevention",
    ])

    with tab_nutrition:
        st.subheader("🍎 Nutrition Guidelines")
        st.markdown(
            """
            ### Balanced Diet Components:
            
            1. **Fruits & Vegetables** (5 servings/day) – vitamins, minerals, fiber.
            2. **Whole Grains** (6 servings/day) – brown rice, oats, whole‑wheat bread.
            3. **Protein** (1.6‑2.2 g per kg body weight) – lean meat, fish, eggs, legumes.
            4. **Dairy** (2‑3 servings/day) – milk, yogurt, cheese.
            5. **Healthy Fats** – olive oil, avocados, nuts (limit saturated fats < 10 % calories).
            
            ### Foods to Limit:
            - Sugary drinks & snacks
            - Processed meats
            - High‑sodium foods
            - Excessive caffeine
            """
        )

    with tab_exercise:
        st.subheader("🏃 Exercise Guidelines")
        st.markdown(
            """
            ### WHO Recommendations (18‑65 yrs):
            
            1. **Aerobic Activity** – 150‑300 min/week (brisk walking, running, cycling, swimming).
            2. **Strength Training** – 2 days/week (weight lifting, body‑weight exercises).
            3. **Flexibility** – daily (stretching, yoga).
            
            ### Tips for Success:
            - Start slowly, increase intensity gradually.
            - Exercise with a friend for motivation.
            - Choose activities you enjoy.
            - Rest 1‑2 days/week.
            - Warm‑up before & cool‑down after.
            """
        )

    with tab_sleep:
        st.subheader("😴 Sleep Guidelines")
        st.markdown(
            """
            ### Recommended Sleep Duration:
            - **Adults (18‑64 yrs)**: 7‑9 hrs/night
            - **Older Adults (65+ yrs)**: 7‑8 hrs/night
            
            ### Tips for Better Sleep:
            1. **Consistent Schedule** – same bedtime & wake‑time every day.
            2. **Sleep Environment** – dark, cool (16‑19 °C), quiet.
            3. **Pre‑sleep Routine** – avoid screens 1 hr before bed, relaxation, no caffeine after 2 PM.
            4. **Lifestyle Habits** – regular exercise (not too close to bedtime), limit naps to 20‑30 min, avoid alcohol/heavy meals.
            
            ### Signs of Sleep Disorder:
            - Persistent insomnia
            - Excessive daytime sleepiness
            - Snoring or breathing interruptions
            - Consult a doctor if issues persist
            """
        )

    with tab_stress:
        st.subheader("🧘 Stress Management")
        st.markdown(
            """
            ### Stress Management Techniques:
            
            1. **Mindfulness & Meditation** – 10‑20 min daily.
            2. **Physical Activity** – releases endorphins, reduces cortisol.
            3. **Breathing Exercises** – 4‑4‑4 pattern, 5‑10 min daily.
            4. **Time Management** – prioritize tasks, break projects into steps, take regular breaks.
            5. **Social Connection** – spend time with friends/family, join clubs.
            6. **Professional Help** – therapist if stress feels overwhelming.
            """
        )

    with tab_prevention:
        st.subheader("🛡️ Disease Prevention")
        st.markdown(
            """
            ### Prevention Strategies:
            
            1. **Cardiovascular Health** – maintain BMI 18.5‑24.9, control BP & cholesterol, limit salt < 5 g/day.
            2. **Diabetes Prevention** – healthy weight, regular exercise, whole grains, reduce sugar.
            3. **Cancer Prevention** – avoid tobacco & excess alcohol, plenty of fruits/veg, regular screenings.
            4. **Regular Check‑ups** – annual health screening, dental check‑up every 6 months, vision check as needed.
            5. **Vaccination** – seasonal flu vaccine annually; follow recommended schedule.
            6. **Mental Health** – regular exercise, good sleep, social connections, seek help when needed.
            """
        )

    st.divider()
    st.caption("Disclaimer: This information is for educational purposes only and does not replace professional medical advice.")
