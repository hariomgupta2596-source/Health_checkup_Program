"""Login page for Health Checkup Program.
Provides a simple login form. On success, stores user info in Streamlit session state.
"""
import streamlit as st
from authentication import verify_password
from database.db_connection import engine
from database.db_setup import users

def render():
    st.title("🔐 Login")
    login_identifier = st.text_input("Username or Email")
    password = st.text_input("Password", type="password")
    if st.button("Log In"):
        if not login_identifier or not password:
            st.error("Please fill in both fields.")
            return
        sel = users.select().where((users.c.username == login_identifier) | (users.c.email == login_identifier))
        with engine.connect() as conn:
            result = conn.execute(sel).fetchone()
        if result is None:
            st.error("User not found.")
            return
        if verify_password(password, result["password_hash"]):
            st.session_state.user_id = result["id"]
            st.session_state.username = result["username"]
            st.success(f"✅ Logged in as {result['username']}")
        else:
            st.error("Incorrect password.")
