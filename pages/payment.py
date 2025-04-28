import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime
import time

# ---- Page Config ----
st.set_page_config(page_title="Payment | TheSpiceNSpirits", layout="centered")
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# # ---- Sidebar Navigation ----
# with st.sidebar:
#     st.markdown("### 🌶️ TheSpiceNSpirits")
#     nav = st.selectbox("☰ Navigate", [
#         "🏠 Home",
#         "👨‍💼 Admin Login",
#         "📋 Menu",
#         "🛒 Cart",
#         "📦 Order Summary",
#         "💳 Payment"
#     ])

#     if nav == "🏠 Home":
#         st.switch_page("streamlit_app.py")
#     elif nav == "👨‍💼 Admin Login":
#         st.switch_page("pages/admin_login.py")
#     elif nav == "📋 Menu":
#         st.switch_page("pages/menu.py")
#     elif nav == "🛒 Cart":
#         st.switch_page("pages/cart.py")
#     elif nav == "📦 Order Summary":
#         st.switch_page("pages/order_summary.py")
#     elif nav == "💳 Payment":
#         pass  # Already on Payment

# ---- Safety Check ----
if "customer_info" not in st.session_state or "final_cart" not in st.session_state:
    st.error("Missing cart or customer data.")
    st.stop()

customer = st.session_state.customer_info
cart = st.session_state.final_cart
total_price = st.session_state.total_cost

# ---- Title and Customer Details ----
st.title("💳 Payment Summary")

st.markdown("### 👤 Customer Details")
with st.container():
    st.markdown(f"""
        <div style="background-color:#222; padding:1rem; border-radius:10px; border:1px solid #444;">
            <p style="margin:0; font-weight:bold;">🧑 Name: <span style="font-weight:normal;">{customer['name']}</span></p>
            <p style="margin:0; font-weight:bold;">📞 Mobile: <span style="font-weight:normal;">{customer['mobile']}</span></p>
            <p style="margin:0; font-weight:bold;">✉️ Email: <span style="font-weight:normal;">{customer['email']}</span></p>
        </div>
    """, unsafe_allow_html=True)

# ---- Order Summary ----
st.markdown("#### 🧾 Order Summary")
df = pd.DataFrame(cart)
df["Total"] = df["price"] * df["qty"]
st.dataframe(df[["item_name", "qty", "price", "Total"]], use_container_width=True)

st.markdown(f"### 💰 Total: **${total_price:.2f}**")

# ---- Payment Method ----
st.markdown("### 🏦 Select Payment Method")
payment_method = st.radio("Payment Mode", ["Cash", "Credit Card", "Debit Card"], horizontal=True)

# ---- Database Connection ----
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Quant2ph4@",  # move later to dotenv
        host="db.ftpuapspmqjfblzhxkok.supabase.co",
        port="5432",
        sslmode="require"
    )

conn = get_connection()

# ---- Insert Order into Database ----
def insert_order(table_id, order_timestamp, total_price, order_status, employee_id, order_type, payment_method):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO orders (table_id, order_timestamp, total_price, order_status, employee_id, order_type, payment_method)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (table_id, order_timestamp, total_price, order_status, employee_id, order_type, payment_method))
        conn.commit()

# ---- Confirm Payment ----
if st.button("✅ Confirm Payment"):
    insert_order(
        table_id=1,                     # assuming dummy table 1
        order_timestamp=datetime.now(),
        total_price=total_price,
        order_status="Confirmed",
        employee_id=8,                  # assuming dummy employee_id 8
        order_type="Dine In",
        payment_method=payment_method
    )

    # Save into session
    st.session_state.order_summary = {
        "customer": customer,
        "cart": cart,
        "total": total_price,
        "payment_method": payment_method
    }

    st.success("💳 Please insert or tap your card in the machine to continue with the payment...")

    with st.empty():
        for i in range(10, 0, -1):
            st.warning(f"⏳ Waiting for card... {i} seconds remaining")
            time.sleep(1)
        st.success("✅ Payment successful and order confirmed!")
        st.balloons()

    st.switch_page("pages/order_summary.py")
