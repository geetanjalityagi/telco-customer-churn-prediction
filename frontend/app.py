import requests
import streamlit as st
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="Customer Churn Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()

API_BASE_URL = "http://localhost:8000/api/v1"
DASHBOARD_URL = f"{API_BASE_URL}/dashboard"

@st.cache_data(ttl=300)
def load_dashboard_data():
    try:
        response = requests.get(DASHBOARD_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching dashboard data: {e}")
        return None

dashboard_data = load_dashboard_data()

st.markdown("# Dashboard Overview")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown("Total Customers")
    st.markdown(f"#### {dashboard_data["kpis"]["total_customers"]}")

with col2:
    st.markdown("Churn Rate")
    st.markdown(f"### {dashboard_data["kpis"]["churn_rate"]}")

with col3:
    st.markdown("High Risk Customers")
    st.markdown(f"#### {dashboard_data["kpis"]["high_risk_customers"]}")

with col4:
    st.markdown("Avergae Tenure")
    st.markdown(f"#### {dashboard_data["kpis"]["average_tenure"]}")

with col5:
    st.markdown("Average Monthly Charges")
    st.markdown(f"#### {dashboard_data["kpis"]["average_monthly_charges"]}")

with col6:
    st.markdown("Revenure at risk")
    st.markdown(f"#### {dashboard_data["kpis"]["revenue_at_risk"]}")