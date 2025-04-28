import streamlit as st
import pandas as pd

# ---- Page Config ----
st.set_page_config(page_title="Order Summary | TheSpiceNSpirits", layout="centered")
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
#         pass  # Already on this page
#     elif nav == "💳 Payment":
#         st.switch_page("pages/payment.py")

# # ---- Safety Check ----
if "order_summary" not in st.session_state:
    st.error("No order found. Please go to the cart first.")
    st.stop()

summary = st.session_state.order_summary
customer = summary["customer"]
cart = summary["cart"]
total = summary["total"]
payment = summary["payment_method"]

# ---- Styled Summary ----
st.title("✅ Order Summary")

st.markdown(f"""
    <div style="background-color:#202020; padding:1rem; border-radius:10px; border:1px solid #444;">
        <h4>🧑 Customer: {customer['name']}</h4>
        <p>📞 {customer['mobile']} &nbsp;&nbsp; ✉️ {customer['email']}</p>
        <p>💳 Payment Method: <b>{payment}</b></p>
    </div>
""", unsafe_allow_html=True)

# ---- Cart Details ----
df = pd.DataFrame(cart)
df["Total"] = df["price"] * df["qty"]

st.markdown("### 🧾 Items Ordered")
st.dataframe(df[["item_name", "qty", "price", "Total"]], use_container_width=True)

st.markdown(f"### 💰 Grand Total: **${total:.2f}**")

st.success("🎉 Hurray! Your order has been successfully placed and will be served within 20 minutes. Sit back and relax!")
st.success("Thank you for choosing TheSpiceNSpirits!")

# ---- Send Receipt (Dummy) ----
st.markdown("---")
st.markdown("📧 Want a receipt?")
if st.button("📤 Send Receipt to Email"):
    # (Here you can actually integrate SMTP email if needed)
    st.success(f"✅ Receipt sent to {customer['email']}")
