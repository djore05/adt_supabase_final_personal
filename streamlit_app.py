import streamlit as st

st.set_page_config(page_title="Welcome | TheSpiceNSpirits", layout="centered", initial_sidebar_state="auto")
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Custom Hamburger Nav ----
with st.sidebar:
    st.markdown("### 🌶️ TheSpiceNSpirits")
    nav = st.selectbox("☰ Navigate", [
        "🏠 Home",
        "👨‍💼 Admin Login",
        "📋 Menu",
        "🛒 Cart",
        "📦 Order Summary",
        "💳 Payment"
    ])

    if nav == "👨‍💼 Admin Login":
        st.switch_page("pages/admin_login.py")
    elif nav == "📋 Menu":
        st.switch_page("pages/menu.py")
    elif nav == "🛒 Cart":
        st.switch_page("pages/cart.py")
    elif nav == "📦 Order Summary":
        st.switch_page("pages/order_summary.py")
    elif nav == "💳 Payment":
        st.switch_page("pages/payment.py")

# ---- Page Content ----
st.title("🌶️ Welcome to TheSpiceNSpirits")
st.markdown("""
Welcome to **TheSpiceNSpirits** – Where flavors meet finesse.  
Explore our curated dishes, seamless ordering, and restaurant management tools.
""")

st.image("https://images.unsplash.com/photo-1600891964599-f61ba0e24092")

