"""Registration page for Health Checkup Program.
Creates a new user with hashed password.
"""
import streamlit as st
from authentication import get_password_hash
from database.db_connection import engine
from database.db_setup import users
from datetime import datetime

def render():
    st.title("📝 Register")
    new_username = st.text_input("Choose a username", key="reg_user")
    new_email = st.text_input("Email", key="reg_email")
    pwd1 = st.text_input("Password", type="password", key="reg_pwd1")
    pwd2 = st.text_input("Confirm Password", type="password", key="reg_pwd2")
    if st.button("Create Account"):
        # Basic validation
        if not new_username or not new_email or not pwd1 or not pwd2:
            st.error("All fields are required.")
        elif pwd1 != pwd2:
            st.error("Passwords do not match.")
        else:
            # Check if username or email already exists
            sel = users.select().where((users.c.username == new_username) | (users.c.email == new_email))
            with engine.connect() as conn:
                exists = conn.execute(sel).first()
            if exists:
                st.error("Username or email already taken.")
            else:
                pwd_hash = get_password_hash(pwd1)
                ins = users.insert().values(username=new_username, email=new_email, password_hash=pwd_hash, created_at=datetime.utcnow())
                with engine.begin() as conn:
                    conn.execute(ins)
                st.success("✅ Registration successful! You can now log in.")
