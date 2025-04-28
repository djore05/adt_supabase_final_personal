import streamlit as st
import psycopg2
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

# ---- Insert Customer Info Function ----
def insert_customer(name, mobile, email):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO customer (name, mobile, email)
            VALUES (%s, %s, %s)
        """, (name, mobile, email))
        conn.commit()

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
            # Save into database
            insert_customer(name, mobile, email)

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
