import streamlit as st
import psycopg2
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

# ---- Database Connection ----
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Quant2ph4@",
        host="db.ftpuapspmqjfblzhxkok.supabase.co",
        port="5432",
        sslmode="require"
    )

conn = get_connection()

# ---- Helper Query ----
def run_query(query, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params or ())
        colnames = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        return pd.DataFrame(rows, columns=colnames)

# ---- Fetch Menu ----
def fetch_menu():
    query = """
        SELECT ms.section_name, msc.subcategory_name, mi.menu_item_id, mi.item_name,
               mi.description, mi.price, mi.spice_level, mi.dietary_type
        FROM menu_items mi
        JOIN menu_subcategories msc ON mi.subcategory_id = msc.subcategory_id
        JOIN menu_sections ms ON msc.section_id = ms.section_id
        WHERE mi.availability = TRUE
        ORDER BY ms.section_name, msc.subcategory_name, mi.item_name
    """
    return run_query(query)

menu_df = fetch_menu()

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
