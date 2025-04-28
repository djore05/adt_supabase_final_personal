import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import decimal
from datetime import datetime

# ---- Streamlit Page Config ----
st.set_page_config(page_title="Admin Dashboard | TheSpiceNSpirits", layout="wide")
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Top Bar ----
col1, col2 = st.columns([8, 1])
with col1:
    st.title("📊 Admin Dashboard")
with col2:
    st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
    if st.button("🚪 Logout", key="logout_btn"):
        st.switch_page("streamlit_app.py")
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

# ---- Helper Query Functions ----
def run_query(table, params=None):
    url = f"{supabase['url']}/rest/v1/{table}"
    response = requests.get(url, headers=supabase['headers'], params=params)
    
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error(f"Query error: {response.status_code}, {response.text}")
        return pd.DataFrame()

def run_custom_query(query_name, params=None):
    """Run a stored function/procedure in Supabase/PostgreSQL"""
    url = f"{supabase['url']}/rest/v1/rpc/{query_name}"
    response = requests.post(url, headers=supabase['headers'], json=params or {})
    
    if response.status_code == 200:
        return pd.DataFrame(response.json() if isinstance(response.json(), list) else [response.json()])
    else:
        st.error(f"Query error: {response.status_code}, {response.text}")
        return pd.DataFrame()

def run_insert(table, data):
    url = f"{supabase['url']}/rest/v1/{table}"
    response = requests.post(url, headers=supabase['headers'], json=data)
    
    if response.status_code in [200, 201]:
        return True, response.json()
    else:
        return False, f"Insert error: {response.status_code}, {response.text}"

def run_update(table, data, match_column, match_value):
    url = f"{supabase['url']}/rest/v1/{table}"
    
    # Add the match condition to the headers
    headers = supabase['headers'].copy()
    headers["Prefer"] = "return=representation"
    
    params = {
        match_column: f"eq.{match_value}"
    }
    
    response = requests.patch(url, headers=headers, json=data, params=params)
    
    if response.status_code in [200, 204]:
        return True, response.json() if response.text else {}
    else:
        return False, f"Update error: {response.status_code}, {response.text}"

def run_delete(table, match_column, match_value):
    url = f"{supabase['url']}/rest/v1/{table}"
    
    params = {
        match_column: f"eq.{match_value}"
    }
    
    response = requests.delete(url, headers=supabase['headers'], params=params)
    
    if response.status_code in [200, 204]:
        return True, {}
    else:
        return False, f"Delete error: {response.status_code}, {response.text}"

# ---- Tabs ----
tabs = st.tabs(["👥 Employees", "📋 Menu Items", "📈 Graphs", "📅 Reservations"])

# ---- Employees Tab ----
with tabs[0]:
    st.subheader("Manage Employees")

    emp_df = run_query("employee")
    st.dataframe(emp_df, use_container_width=True)

    with st.expander("➕ Add New Employee"):
        with st.form("add_emp_form"):
            emp_name = st.text_input("Name")
            title = st.text_input("Title")
            contact = st.text_input("Contact Number")
            age = st.number_input("Age", min_value=18, max_value=100, value=18)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            salary = st.number_input("Salary", min_value=0.0)
            joining_date = st.date_input("Joining Date")
            submit = st.form_submit_button("Add Employee")
            if submit:
                employee_data = {
                    "employee_name": emp_name,
                    "title": title,
                    "contact_number": contact,
                    "age": age,
                    "gender": gender,
                    "salary": salary,
                    "joining_date": joining_date.strftime("%Y-%m-%d")
                }
                success, result = run_insert("employee", employee_data)
                if success:
                    st.success("Employee added successfully!")
                    st.rerun()
                else:
                    st.error(result)

    with st.expander("❌ Remove Employee"):
        if not emp_df.empty:
            emp_choices = [f"{row['employee_id']} - {row['employee_name']}" for _, row in emp_df.iterrows()]
            selected_emp = st.selectbox("Select Employee to Remove", options=emp_choices)
            if st.button("Remove Selected Employee"):
                emp_id = int(selected_emp.split(" - ")[0])
                success, result = run_delete("employee", "employee_id", emp_id)
                if success:
                    st.success("Employee removed successfully!")
                    st.rerun()
                else:
                    st.error(result)
        else:
            st.warning("No employees to display.")

    with st.expander("📝 Edit Employee"):
        if not emp_df.empty:
            emp_choices = [f"{row['employee_id']} - {row['employee_name']}" for _, row in emp_df.iterrows()]
            selected_edit = st.selectbox("Select Employee to Edit", options=emp_choices, key="edit_emp_select")
            if selected_edit:
                emp_id = int(selected_edit.split(" - ")[0])
                selected_row = emp_df[emp_df['employee_id'] == emp_id].iloc[0]
                with st.form("edit_emp_form"):
                    emp_name = st.text_input("Name", value=selected_row['employee_name'])
                    title = st.text_input("Title", value=selected_row['title'])
                    contact = st.text_input("Contact Number", value=selected_row['contact_number'])
                    age = st.number_input("Age", min_value=18, max_value=100, value=selected_row['age'])
                    gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(selected_row['gender']))
                    salary = st.number_input("Salary", min_value=0.0, value=float(selected_row['salary']) if isinstance(selected_row['salary'], (decimal.Decimal, float, int)) else 0.0)
                    joining_date = st.date_input("Joining Date", value=pd.to_datetime(selected_row['joining_date']))
                    submit_edit = st.form_submit_button("Update Employee")
                    if submit_edit:
                        employee_data = {
                            "employee_name": emp_name,
                            "title": title,
                            "contact_number": contact,
                            "age": age,
                            "gender": gender,
                            "salary": salary,
                            "joining_date": joining_date.strftime("%Y-%m-%d")
                        }
                        success, result = run_update("employee", employee_data, "employee_id", emp_id)
                        if success:
                            st.success("Employee updated successfully!")
                            st.rerun()
                        else:
                            st.error(result)
        else:
            st.warning("No employees to display.")

# ---- Menu Items Tab ----
with tabs[1]:
    st.subheader("Manage Menu Items")

    menu_df = run_query("menu_items")
    st.dataframe(menu_df, use_container_width=True)

    with st.expander("➕ Add Menu Item"):
        with st.form("add_menu_form"):
            item_name = st.text_input("Item Name")
            description = st.text_area("Description")
            price = st.number_input("Price", min_value=0.0)
            spice_level = st.selectbox("Spice Level", ["Low", "Medium", "High"])
            dietary_type = st.selectbox("Dietary Type", ["VEG", "NON-VEG", "VEGAN", "EGG"])
            availability = st.checkbox("Available", value=True)
            subcategory_id = st.number_input("Subcategory ID", step=1)
            submit = st.form_submit_button("Add Item")
            if submit:
                menu_data = {
                    "item_name": item_name,
                    "description": description,
                    "price": price,
                    "spice_level": spice_level,
                    "dietary_type": dietary_type,
                    "availability": availability,
                    "subcategory_id": subcategory_id
                }
                success, result = run_insert("menu_items", menu_data)
                if success:
                    st.success("Menu item added successfully!")
                    st.rerun()
                else:
                    st.error(result)

    with st.expander("❌ Remove Menu Item"):
        if not menu_df.empty:
            menu_choices = [f"{row['menu_item_id']} - {row['item_name']}" for _, row in menu_df.iterrows()]
            selected_menu = st.selectbox("Select Item to Remove", options=menu_choices)
            if st.button("Remove Menu Item"):
                item_id = int(selected_menu.split(" - ")[0])
                success, result = run_delete("menu_items", "menu_item_id", item_id)
                if success:
                    st.success("Menu item removed.")
                    st.rerun()
                else:
                    st.error(result)
        else:
            st.warning("No menu items to display.")

# ---- Reservations Tab ----
with tabs[3]:
    st.subheader("Manage Reservations")

    res_df = run_query("reservations")
    st.dataframe(res_df, use_container_width=True)

    with st.expander("➕ Add Reservation"):
        with st.form("add_res_form"):
            customer_id = st.number_input("Customer ID", step=1)
            table_id = st.number_input("Table ID", step=1)
            reservation_time = st.text_input("Reservation Time (YYYY-MM-DD HH:MM:SS)")
            guests = st.number_input("Number of People", min_value=1)
            submit = st.form_submit_button("Add Reservation")
            if submit:
                reservation_data = {
                    "customer_id": customer_id,
                    "table_id": table_id,
                    "reservation_time": reservation_time,
                    "number_of_guests": guests
                }
                success, result = run_insert("reservations", reservation_data)
                if success:
                    st.success("Reservation added successfully!")
                    st.rerun()
                else:
                    st.error(result)

# ---- Analytics Tab ----
with tabs[2]:
    st.subheader("📊 Analytics Dashboard")

    # For complex queries, we need to create stored procedures/functions in Supabase
    # Here we'll use the run_custom_query function which calls these procedures
    
    st.markdown("### 🍽 Menu Distribution by Dietary Type")
    diet_df = run_custom_query("get_menu_by_dietary_type")
    if not diet_df.empty:
        st.bar_chart(diet_df.set_index("dietary_type"))
    else:
        # Fallback using basic query
        diet_data = run_query("menu_items", {"select": "dietary_type,count"})
        diet_df = diet_data.groupby("dietary_type").size().reset_index(name="count")
        st.bar_chart(diet_df.set_index("dietary_type"))

    st.markdown("### 📅 Monthly Reservations Count")
    res_trend = run_custom_query("get_monthly_reservations")
    if not res_trend.empty:
        st.line_chart(res_trend.set_index("month"))
    else:
        st.info("No reservation trend data available. Create a stored procedure in Supabase or implement the query directly.")

    st.markdown("### 👤 Employees by Gender")
    emp_gender = run_custom_query("get_employees_by_gender")
    if not emp_gender.empty:
        st.bar_chart(emp_gender.set_index("gender"))
    else:
        # Fallback using basic query
        gender_data = run_query("employee", {"select": "gender,count"})
        emp_gender = gender_data.groupby("gender").size().reset_index(name="count")
        st.bar_chart(emp_gender.set_index("gender"))

    st.markdown("### 🔝 Top 10 Most Ordered Menu Items")
    top_items = run_custom_query("get_top_menu_items")
    if not top_items.empty:
        st.bar_chart(top_items.set_index("item_name"))
    else:
        st.info("No top items data available. Create a stored procedure in Supabase or implement the query directly.")

    st.markdown("### 💳 Payment Method Distribution")
    payment_data = run_custom_query("get_payment_methods")
    if not payment_data.empty:
        st.plotly_chart(
            px.pie(payment_data, values="total", names="payment_method", title="Payment Method Usage"),
            use_container_width=True
        )
    else:
        st.info("No payment method data available. Create a stored procedure in Supabase or implement the query directly.")

    st.markdown("### 📈 Monthly Revenue Trend")
    revenue_df = run_custom_query("get_monthly_revenue")
    if not revenue_df.empty:
        st.line_chart(revenue_df.set_index("month"))
    else:
        st.info("No monthly revenue data available. Create a stored procedure in Supabase or implement the query directly.")

    st.markdown("### 📅 Daily Revenue Trend")
    daily_revenue = run_custom_query("get_daily_revenue")
    if not daily_revenue.empty:
        st.line_chart(daily_revenue.set_index("day"))
    else:
        st.info("No daily revenue data available. Create a stored procedure in Supabase or implement the query directly.")
