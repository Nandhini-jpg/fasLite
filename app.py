import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Import database setup
from db_setup import initialize_sample_data
from auth import authenticate_user, register_user, logout, get_current_user, is_authenticated
from data_manager import initialize_data
from dashboards.faculty import faculty_dashboard
from dashboards.dean import dean_dashboard
from dashboards.student import student_dashboard

# Set page config
st.set_page_config(
    page_title="Faculty Appraisal System",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "Login"

# Initialize database and sample data
initialize_sample_data()

# Initialize other data (like current semester)
initialize_data()

# App header
st.title("Faculty Appraisal System")

# Side navigation
if is_authenticated():
    user = get_current_user()
    with st.sidebar:
        st.write(f"Welcome, {user['name']} ({user['role']})")
        st.button("Logout", on_click=logout)

# Main content area
if not is_authenticated():
    # Authentication page (Login/Register)
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        login_role = st.selectbox("Role", ["Faculty", "Dean", "Student"], key="login_role")
        
        if st.button("Login", key="login_btn"):
            if authenticate_user(login_username, login_password, login_role.lower()):
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
    
    with tab2:
        st.subheader("Register")
        register_name = st.text_input("Full Name", key="register_name")
        register_username = st.text_input("Username", key="register_username")
        register_password = st.text_input("Password", type="password", key="register_password")
        register_role = st.selectbox("Role", ["Faculty", "Dean", "Student"], key="register_role")
        
        if st.button("Register", key="register_btn"):
            if register_name and register_username and register_password:
                if register_user(register_username, register_password, register_name, register_role.lower()):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists. Please choose another.")
            else:
                st.error("All fields are required.")
else:
    # Display dashboard based on user role
    if st.session_state.user_role == "faculty":
        faculty_dashboard()
    elif st.session_state.user_role == "dean":
        dean_dashboard()
    elif st.session_state.user_role == "student":
        student_dashboard()
