import streamlit as st
import requests
import pandas as pd
import decimal

# ---- Supabase API Configuration ----
SUPABASE_URL = "https://db.ftpuapspmqjfblzhxkok.supabase.co"  # Your Supabase URL
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ0cHVhcHNwbXFqZmJsemh4a29rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU4MDMwMzEsImV4cCI6MjA2MTM3OTAzMX0.nm3UhSuArd46urs25uz5V7Lo4xnYEwnzqfpRUoP_Dcw"  # Replace with your Supabase anon API key

# ---- Page Config ----
st.set_page_config(page_title="TheSpiceNSpirits - Menu", layout="wide")
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Title and Go to Cart ----
col1, col2 = st.columns([8, 2])
with col1:
    st.title("🍽️ TheSpiceNSpirits - Menu")
with col2:
    st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
    if st.button("🛒 Go to Cart"):
        st.switch_page("pages/cart.py")
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Function to Fetch Data from Supabase ----
def fetch_menu_from_supabase():
    # Define the endpoint for the menu items table
    endpoint = f"{SUPABASE_URL}/rest/v1/menu_items"
    
    # Set up headers, including the authorization token
    headers = {
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json",
    }

    # Add query parameters (if needed)
    params = {
        "select": "section_name, subcategory_name, menu_item_id, item_name, description, price, spice_level, dietary_type",
        "availability": "eq.true",  # Filter for available items
        "order": "section_name, subcategory_name, item_name"  # Sorting by section, subcategory, item name
    }

    # Send GET request to Supabase API
    response = requests.get(endpoint, headers=headers, params=params)

    if response.status_code == 200:
        return pd.DataFrame(response.json())  # Return as a DataFrame
    else:
        st.error(f"Failed to fetch data from Supabase. Status Code: {response.status_code}")
        return pd.DataFrame()  # Return empty DataFrame in case of error

# ---- Fetch Menu from Supabase ----
menu_df = fetch_menu_from_supabase()

# ---- Sidebar Filters ----
st.sidebar.markdown("### 🥗 Filter by Dietary Type")
dietary_types = sorted(menu_df['dietary_type'].dropna().unique())
selected_types = [dtype for dtype in dietary_types if st.sidebar.checkbox(dtype, value=True, key=dtype)]

if selected_types:
    menu_df = menu_df[menu_df['dietary_type'].isin(selected_types)]
else:
    st.warning("Please select at least one dietary type to view the menu.")
    st.stop()

# ---- Initialize Cart ----
if 'cart' not in st.session_state:
    st.session_state.cart = []

# ---- Display Menu ----
sections = menu_df['section_name'].unique()
for section in sections:
    st.header(f"🍴 {section}")
    section_df = menu_df[menu_df['section_name'] == section]
    subcategories = section_df['subcategory_name'].unique()

    for sub in subcategories:
        with st.expander(sub):
            sub_df = section_df[section_df['subcategory_name'] == sub]

            for _, row in sub_df.iterrows():
                cart_item = next((item for item in st.session_state.cart if item['item_id'] == row['menu_item_id']), None)
                current_qty = cart_item['qty'] if cart_item else 0

                cols = st.columns([3, 3, 1, 1, 1])

                with cols[0]:
                    st.markdown(f"**{row['item_name']}**  \n{row['description']}")

                with cols[1]:
                    st.markdown(f"💲{float(row['price']) if isinstance(row['price'], decimal.Decimal) else row['price']}  \n{row['dietary_type']} | 🌶️ {row['spice_level']}")

                with cols[2]:
                    st.markdown(f"**Qty in Cart: {current_qty}**")

                with cols[3]:
                    if st.button("➕", key=f"add_{row['menu_item_id']}"):
                        if cart_item:
                            cart_item['qty'] += 1
                        else:
                            st.session_state.cart.append({
                                'item_id': row['menu_item_id'],
                                'item_name': row['item_name'],
                                'price': float(row['price']) if isinstance(row['price'], decimal.Decimal) else row['price'],
                                'qty': 1
                            })
                        st.rerun()

                with cols[4]:
                    if st.button("➖", key=f"remove_{row['menu_item_id']}"):
                        if cart_item:
                            cart_item['qty'] -= 1
                            if cart_item['qty'] <= 0:
                                st.session_state.cart.remove(cart_item)
                                st.warning(f"{row['item_name']} removed from cart!")
                            st.rerun()
