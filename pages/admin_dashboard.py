import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import decimal

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

# ---- Database Connection ----
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Quant2ph4@",  # ⚠️ move to .env later
        host="db.ftpuapspmqjfblzhxkok.supabase.co",
        port="5432",
        sslmode="require"
    )

conn = get_connection()

# ---- Helper Query Functions ----
def run_query(query, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params or ())
        try:
            colnames = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            return pd.DataFrame(rows, columns=colnames)
        except:
            conn.commit()
            return None

def run_update(query, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params or ())
        conn.commit()

# ---- Tabs ----
tabs = st.tabs(["👥 Employees", "📋 Menu Items", "📈 Graphs", "📅 Reservations"])

# ---- Employees Tab ----
with tabs[0]:
    st.subheader("Manage Employees")

    emp_df = run_query("SELECT * FROM employee")
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
                run_update("""
                    INSERT INTO employee (employee_name, title, contact_number, age, gender, salary, joining_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (emp_name, title, contact, age, gender, salary, joining_date))
                st.success("Employee added successfully!")
                st.rerun()

    with st.expander("❌ Remove Employee"):
        emp_choices = emp_df[['employee_id', 'employee_name']].apply(lambda x: f"{x['employee_id']} - {x['employee_name']}", axis=1).tolist()
        selected_emp = st.selectbox("Select Employee to Remove", options=emp_choices)
        if st.button("Remove Selected Employee"):
            emp_id = int(selected_emp.split(" - ")[0])
            run_update("DELETE FROM employee WHERE employee_id = %s", (emp_id,))
            st.success("Employee removed successfully!")
            st.rerun()

    with st.expander("📝 Edit Employee"):
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
                salary = st.number_input("Salary", min_value=0.0, value=float(selected_row['salary']) if isinstance(selected_row['salary'], decimal.Decimal) else selected_row['salary'])
                joining_date = st.date_input("Joining Date", value=pd.to_datetime(selected_row['joining_date']))
                submit_edit = st.form_submit_button("Update Employee")
                if submit_edit:
                    run_update("""
                        UPDATE employee
                        SET employee_name = %s, title = %s, contact_number = %s,
                            age = %s, gender = %s, salary = %s, joining_date = %s
                        WHERE employee_id = %s
                    """, (emp_name, title, contact, age, gender, salary, joining_date, emp_id))
                    st.success("Employee updated successfully!")
                    st.rerun()

# ---- Menu Items Tab ----
with tabs[1]:
    st.subheader("Manage Menu Items")

    menu_df = run_query("SELECT * FROM menu_items")
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
                run_update("""
                    INSERT INTO menu_items (item_name, description, price, spice_level, dietary_type, availability, subcategory_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (item_name, description, price, spice_level, dietary_type, availability, subcategory_id))
                st.success("Menu item added successfully!")
                st.rerun()

    with st.expander("❌ Remove Menu Item"):
        menu_choices = menu_df[['menu_item_id', 'item_name']].apply(lambda x: f"{x['menu_item_id']} - {x['item_name']}", axis=1).tolist()
        selected_menu = st.selectbox("Select Item to Remove", options=menu_choices)
        if st.button("Remove Menu Item"):
            item_id = int(selected_menu.split(" - ")[0])
            run_update("DELETE FROM menu_items WHERE menu_item_id = %s", (item_id,))
            st.success("Menu item removed.")
            st.rerun()

# ---- Reservations Tab ----
with tabs[3]:
    st.subheader("Manage Reservations")

    res_df = run_query("SELECT * FROM reservations")
    st.dataframe(res_df, use_container_width=True)

    with st.expander("➕ Add Reservation"):
        with st.form("add_res_form"):
            customer_id = st.number_input("Customer ID", step=1)
            table_id = st.number_input("Table ID", step=1)
            reservation_time = st.text_input("Reservation Time (YYYY-MM-DD HH:MM:SS)")
            guests = st.number_input("Number of People", min_value=1)
            submit = st.form_submit_button("Add Reservation")
            if submit:
                run_update("""
                    INSERT INTO reservations (customer_id, table_id, reservation_time, number_of_guests)
                    VALUES (%s, %s, %s, %s)
                """, (customer_id, table_id, reservation_time, guests))
                st.success("Reservation added successfully!")
                st.rerun()

# ---- Analytics Tab ----
with tabs[2]:
    st.subheader("📊 Analytics Dashboard")

    st.markdown("### 🍽 Menu Distribution by Dietary Type")
    diet_df = run_query("""
        SELECT dietary_type, COUNT(*) as count
        FROM menu_items
        GROUP BY dietary_type
    """)
    st.bar_chart(diet_df.set_index("dietary_type"))

    st.markdown("### 📅 Monthly Reservations Count")
    res_trend = run_query("""
        SELECT TO_CHAR(reservation_time, 'YYYY-MM') AS month, COUNT(*) as total
        FROM reservations
        GROUP BY month
        ORDER BY month
    """)
    st.line_chart(res_trend.set_index("month"))

    st.markdown("### 👤 Employees by Gender")
    emp_gender = run_query("""
        SELECT gender, COUNT(*) as count
        FROM employee
        GROUP BY gender
    """)
    st.bar_chart(emp_gender.set_index("gender"))

    st.markdown("### 🔝 Top 10 Most Ordered Menu Items")
    top_items = run_query("""
        SELECT mi.item_name, COUNT(oi.order_id) AS frequency
        FROM order_items oi
        JOIN menu_items mi ON oi.menu_item_id = mi.menu_item_id
        GROUP BY mi.item_name
        ORDER BY frequency DESC
        LIMIT 10
    """)
    st.bar_chart(top_items.set_index("item_name"))

    st.markdown("### 💳 Payment Method Distribution")
    payment_data = run_query("""
        SELECT payment_method, COUNT(*) as total
        FROM orders
        GROUP BY payment_method
    """)
    st.plotly_chart(
        px.pie(payment_data, values="total", names="payment_method", title="Payment Method Usage"),
        use_container_width=True
    )

    st.markdown("### 📈 Monthly Revenue Trend")
    revenue_df = run_query("""
        SELECT TO_CHAR(order_timestamp, 'YYYY-MM') AS month, SUM(total_price) AS revenue
        FROM orders
        GROUP BY month
        ORDER BY month
    """)
    st.line_chart(revenue_df.set_index("month"))

    st.markdown("### 📅 Daily Revenue Trend")
    daily_revenue = run_query("""
        SELECT DATE(order_timestamp) AS day, SUM(total_price) AS revenue
        FROM orders
        GROUP BY day
        ORDER BY day
    """)
    st.line_chart(daily_revenue.set_index("day"))
