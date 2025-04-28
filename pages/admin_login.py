import streamlit as st
import psycopg2
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

# ---- Database Connection (psycopg2) ----
@st.cache_resource
def get_connection():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Quant2ph4@",
        host="db.ftpuapspmqjfblzhxkok.supabase.co",
        port="5432",
        sslmode="require"  # <-- Force SSL here
    )
    return conn

# ---- Validate Admin Login ----
def validate_admin(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 1 FROM employee
        WHERE title = %s AND employee_name = %s
        LIMIT 1
    """, (username, password))
    
    result = cur.fetchone()

    cur.close()
    conn.close()

    return result is not None

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
