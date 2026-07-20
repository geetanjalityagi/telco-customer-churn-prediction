import requests
import streamlit as st
from utils.sidebar import render_sidebar
from components.charts import churn_distribution_chart, contract_distribution_chart, contract_vs_churn_chart, internet_vs_churn_chart, payment_vs_churn_chart, tenure_distribution_chart, monthly_charges_chart, correlation_chart

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

st.title("🧭 Dashboard Overview")
st.divider()

if dashboard_data and "kpis" in dashboard_data:
    kpis = dashboard_data["kpis"]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Customers", value=kpis.get("total_customers", "N/A"))
    with col2:
        st.metric(label="Churn Rate", value=kpis.get("churn_rate", "N/A"))
    with col3:
        st.metric(label="High Risk Customers", value=kpis.get("high_risk_customers", "N/A"))

    st.write("")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric(label="Average Tenure", value=kpis.get("average_tenure", "N/A"))
    with col5:
        st.metric(label="Average Monthly Charges", value=kpis.get("average_monthly_charges", "N/A"))
    with col6:
        st.metric(label="Revenue at Risk", value=kpis.get("revenue_at_risk", "N/A"))
else:
    st.info("No dashboard data available to display.")

st.divider()

st.markdown("### 📈 Key Insights & Trends")
st.write("")

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    churn_distribution_chart()
with chart_col2:
    contract_distribution_chart()

st.write("  ")

chart_col3, chart_col4 = st.columns(2)
with chart_col3:
    contract_vs_churn_chart()
    with st.expander("Insights"):
        st.write(
            """
            - Customers with Month-to-Month contracts have the highest churn rate.
            - Customers with One-Year and Two-Year contracts are much more likely to stay.
            - Longer contracts improve customer retention.
            """
        )
with chart_col4:
    internet_vs_churn_chart()
    with st.expander("Insights"):
        st.write(
            """
            - Fiber Optic customers have the highest churn rate.
            - Customers without internet service have the lowest churn.
            - Fiber Optic customers should be prioritized for retention strategies.
            """
        )

st.write("  ") 

chart_col5, chart_col6 = st.columns(2)
with chart_col5:
    payment_vs_churn_chart()
    with st.expander("Insights"):
        st.write(
            """
            - Customers using Electronic Check have the highest churn rate.
            - Automatic payment methods are associated with lower churn.
            - Promoting automatic payments may help reduce churn.
            """
        )
with chart_col6:
    tenure_distribution_chart()
    with st.expander("Insights"):
        st.write(
            """
            - Customers with shorter tenure are more likely to churn.
            - Churn decreases as customer tenure increases.
            - The first year is the most critical period for retention.
            """
        )

monthly_charges_chart()
correlation_chart()