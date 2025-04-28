import streamlit as st
import requests
import pandas as pd
import decimal

# ---- Page Config ----
st.set_page_config(page_title="🛒 Your Cart")
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Title ----
st.title("🛒 TheSpiceNSpirits - Cart")

# ---- Check Cart ----
if 'cart' not in st.session_state or not st.session_state.cart:
    st.warning("🛒 Your cart is empty. Go to the Menu and add some items!")
    st.stop()

# ---- Display Cart ----
cart_items = st.session_state.cart
cart_df = pd.DataFrame(cart_items)
cart_df['Total'] = cart_df['qty'] * cart_df['price']

st.subheader("Your Selected Items")
for i, item in enumerate(cart_items):
    cols = st.columns([4, 2, 2, 2, 1])
    with cols[0]:
        st.write(f"**{item['item_name']}**")
    with cols[1]:
        st.write(f"Qty: {item['qty']}")
    with cols[2]:
        st.write(f"Price: ${item['price']:.2f}")
    with cols[3]:
        st.write(f"Total: ${item['qty'] * item['price']:.2f}")
    with cols[4]:
        if st.button("❌", key=f"remove_{i}"):
            st.session_state.cart.pop(i)
            st.success(f"Removed {item['item_name']} from cart.")
            st.rerun()

# ---- Show Total ----
total = cart_df['Total'].sum()
st.markdown(f"### 💵 Total: ${total:.2f}")

# ---- Clear Cart ----
if st.button("🗑️ Clear Entire Cart"):
    st.session_state.cart = []
    st.success("Cart cleared.")
    st.rerun()

# ---- Customer Information Form ----
st.markdown("---")
st.markdown("### 🧾 Enter your Details")

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

# ---- Insert Customer Info Function ----
def insert_customer(name, mobile, email):
    url = f"{supabase['url']}/rest/v1/customer"
    customer_data = {
        "name": name,
        "mobile": mobile,
        "email": email
    }
    
    response = requests.post(
        url, 
        json=customer_data, 
        headers=supabase['headers']
    )
    
    if response.status_code in [200, 201]:
        return True, response.json()
    else:
        return False, f"Error: {response.status_code}, {response.text}"

# ---- Form to Save Customer and Proceed to Payment ----
with st.form("customer_form"):
    name = st.text_input("Name")
    mobile = st.text_input("Mobile Number")
    email = st.text_input("Email Address")
    submit_customer = st.form_submit_button("💳 Proceed to Payment")
    
    if submit_customer:
        if not name or not mobile:
            st.error("Please provide at least a name and mobile number.")
        else:
            # Save into database using Supabase
            success, result = insert_customer(name, mobile, email)
            
            if success:
                # Save into session for next page
                st.session_state.customer_info = {
                    "name": name,
                    "mobile": mobile,
                    "email": email
                }
                st.session_state.final_cart = st.session_state.cart.copy()
                st.session_state.total_cost = float(total)  # Make sure total is float not Decimal
                st.success("✅ Customer information saved!")
                st.switch_page("pages/payment.py")
            else:
                st.error(f"Failed to save customer information: {result}")
