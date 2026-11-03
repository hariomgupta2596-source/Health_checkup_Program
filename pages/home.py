import streamlit as st

def render():
    """Home page for Health Checkup Program"""
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
