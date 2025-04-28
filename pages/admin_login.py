import streamlit as st
import requests
import pandas as pd

# ---- Page Config ----
st.set_page_config(page_title="Admin Login | TheSpiceNSpirits")
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Title ----
st.title("👨‍💼 Admin Login - TheSpiceNSpirits")

# ---- Supabase Configuration ----
@st.cache_resource
def get_supabase_client():
    supabase_url = "https://ftpuapspmqjfblzhxkok.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ0cHVhcHNwbXFqZmJsemh4a29rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU4MDMwMzEsImV4cCI6MjA2MTM3OTAzMX0.nm3UhSuArd46urs25uz5V7Lo4xnYEwnzqfpRUoP_Dcw"
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    return {
        "url": supabase_url,
        "headers": headers
    }

supabase = get_supabase_client()

# ---- Validate Admin Login ----
def validate_admin(username, password):
    url = f"{supabase['url']}/rest/v1/employee"
    
    # Query parameters to filter employees with the given title and name
    # Using "*" instead of "id" to select any column
    params = {
        "select": "*",  # Select all columns instead of just 'id'
        "title": f"eq.{username}",
        "employee_name": f"eq.{password}"
    }
    
    try:
        response = requests.get(
            url,
            headers=supabase['headers'],
            params=params
        )
        
        if response.status_code == 200:
            # If we got results, the admin exists
            return len(response.json()) > 0
        else:
            st.error(f"Database error: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to database: {str(e)}")
        return False

# ---- Login Form ----
with st.form("admin_login_form"):
    username = st.text_input("Enter your Username")
    password = st.text_input("Enter your Password", type="password")
    submitted = st.form_submit_button("Login")
    
    if submitted:
        if validate_admin(username, password):
            st.success("Login successful! Redirecting to admin dashboard...")
            st.session_state.admin_logged_in = True
            st.switch_page("pages/admin_dashboard.py")
        else:
            st.error("Invalid credentials. Please try again.")
