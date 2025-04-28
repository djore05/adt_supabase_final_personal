import streamlit as st
import pandas as pd
import requests
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

# ---- Insert Order into Database ----
def insert_order(table_id, order_timestamp, total_price, order_status, employee_id, order_type, payment_method):
    url = f"{supabase['url']}/rest/v1/orders"
    
    order_data = {
        "table_id": table_id,
        "order_timestamp": order_timestamp.isoformat(),
        "total_price": total_price,
        "order_status": order_status,
        "employee_id": employee_id,
        "order_type": order_type,
        "payment_method": payment_method
    }
    
    response = requests.post(
        url, 
        json=order_data, 
        headers=supabase['headers']
    )
    
    if response.status_code in [200, 201]:
        return True, response.json()
    else:
        return False, f"Error: {response.status_code}, {response.text}"

# ---- Confirm Payment ----
if st.button("✅ Confirm Payment"):
    success, result = insert_order(
        table_id=1,                     # assuming dummy table 1
        order_timestamp=datetime.now(),
        total_price=total_price,
        order_status="Confirmed",
        employee_id=8,                  # assuming dummy employee_id 8
        order_type="Dine In",
        payment_method=payment_method
    )
    
    if success:
        # Save into session
        st.session_state.order_summary = {
            "customer": customer,
            "cart": cart,
            "total": total_price,
            "payment_method": payment_method,
            "order_id": result[0]["id"] if isinstance(result, list) and len(result) > 0 else None
        }

        st.success("💳 Please insert or tap your card in the machine to continue with the payment...")

        with st.empty():
            for i in range(10, 0, -1):
                st.warning(f"⏳ Waiting for card... {i} seconds remaining")
                time.sleep(1)
            st.success("✅ Payment successful and order confirmed!")
            st.balloons()

        st.switch_page("pages/order_summary.py")
    else:
        st.error(f"Failed to process order: {result}")
        st.info("Please try again or contact support.")
