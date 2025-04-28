import streamlit as st
import requests

# Supabase API URL and API Key
url = "https://ftpuapspmqjfblzhxkok.supabase.co/rest/v1/menu_items"
headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ0cHVhcHNwbXFqZmJsemh4a29rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU4MDMwMzEsImV4cCI6MjA2MTM3OTAzMX0.nm3UhSuArd46urs25uz5V7Lo4xnYEwnzqfpRUoP_Dcw",
    "Content-Type": "application/json"
}

# Function to fetch data from Supabase
def fetch_data_from_supabase():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Return JSON data if request is successful
    else:
        st.error(f"Failed to fetch data from Supabase. Status Code: {response.status_code}")
        return []

# Streamlit app layout
st.title("Supabase Menu Items")

# Fetch data when the app loads
menu_data = fetch_data_from_supabase()

# Display the fetched data
if menu_data:
    for item in menu_data:
        st.write(item)  # Display each menu item record
else:
    st.write("No menu items found.")
