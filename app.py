import streamlit as st
import dashboard_sleep
import dashboard_steps

# Sidebar Navigation
st.sidebar.title("Navigation")
selected_dashboard = st.sidebar.radio("Go to:", ["Steps Dashboard", "Sleep Dashboard"])

# Load selected dashboard
if selected_dashboard == "Steps Dashboard":
    dashboard_steps.main()
elif selected_dashboard == "Sleep Dashboard":
    dashboard_sleep.main()