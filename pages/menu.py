import streamlit as st
import requests
import pandas as pd
import decimal

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

# ---- Helper Query Function ----
def run_query(table, params=None):
    """
    Execute SELECT queries against Supabase REST API
    table: table name
    params: dictionary of parameters for filtering, etc.
    """
    url = f"{supabase['url']}/rest/v1/{table}"
    
    response = requests.get(url, headers=supabase['headers'], params=params)
    
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error(f"Error executing query on table {table}: {response.status_code}, {response.text}")
        return pd.DataFrame()

# ---- Fetch Menu ----
def fetch_menu():
    try:
        # Query each table individually
        menu_items = run_query('menu_items', {
            'select': 'menu_item_id,item_name,description,price,spice_level,dietary_type,availability,subcategory_id',
            'availability': 'eq.true'
        })
        
        subcategories = run_query('menu_subcategories', {
            'select': 'subcategory_id,subcategory_name,section_id'
        })
        
        sections = run_query('menu_sections', {
            'select': 'section_id,section_name'
        })
        
        # Check if we have data from all tables
        if menu_items.empty or subcategories.empty or sections.empty:
            missing_tables = []
            if menu_items.empty: missing_tables.append("menu_items")
            if subcategories.empty: missing_tables.append("menu_subcategories")
            if sections.empty: missing_tables.append("menu_sections")
            
            st.error(f"Could not retrieve data from tables: {', '.join(missing_tables)}")
            return pd.DataFrame()
        
        # Step 1: Join menu_items with subcategories
        merged_df = pd.merge(
            menu_items, 
            subcategories, 
            on='subcategory_id', 
            how='inner'
        )
        
        # Step 2: Join with sections
        menu_df = pd.merge(
            merged_df, 
            sections, 
            on='section_id', 
            how='inner'
        )
        
        # Sort the result similar to the original SQL query
        menu_df = menu_df.sort_values(by=['section_name', 'subcategory_name', 'item_name'])
        
        # Check if we have the required columns for the UI
        required_columns = ['section_name', 'subcategory_name', 'menu_item_id', 
                           'item_name', 'description', 'price', 'spice_level', 'dietary_type']
        
        missing_columns = [col for col in required_columns if col not in menu_df.columns]
        if missing_columns:
            st.error(f"Missing required columns in query result: {', '.join(missing_columns)}")
            return pd.DataFrame()
        
        return menu_df
    
    except Exception as e:
        st.error(f"Error fetching menu: {str(e)}")
        return pd.DataFrame()

# Fetch menu data
menu_df = fetch_menu()

# Handle potential empty dataframe
if menu_df.empty:
    st.error("Could not retrieve menu data")
    st.stop()

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
