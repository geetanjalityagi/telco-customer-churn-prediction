import requests
import streamlit as st
from utils.sidebar import render_sidebar
from components.charts import churn_distribution_chart, contract_distribution_chart, contract_vs_churn_chart, internet_vs_churn_chart, payment_vs_churn_chart, tenure_distribution_chart, monthly_charges_chart, correlation_chart,contract_payment_heatmap

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

st.title("📊 Dashboard Overview")
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
    with st.expander("Insights"):
        st.write(
            """
            - Around 26.5% of the customer base has churned, indicating a moderately imbalanced dataset.
            - Because the majority (~73.5%) remain, standard accuracy can be misleading; evaluation metrics like F1-score and ROC-AUC are more suitable.
            - Addressing this class imbalance is critical during model training and validation.
            """
        )
with chart_col2:
    contract_distribution_chart()
    with st.expander("Insights"):
        st.write(
            """
            - Month-to-Month contracts are the most common, accounting for 54.9% of the customer base.
            - Long-term contracts (One-Year and Two-Year) make up the remaining 45.1% of customers.
            - The high volume of short-term contracts exposes the business to higher revenue volatility.
            """
        )

st.write("  ")

chart_col3, chart_col4 = st.columns(2)
with chart_col3:
    contract_vs_churn_chart()
    with st.expander("Insights"):
        st.write(
            """
            - Month-to-Month contracts have an exceptionally high churn rate of 42.6%.
            - Customers with One-Year (11.3%) and Two-Year (2.8%) contracts have significantly lower churn.
            - Transitioning Month-to-Month customers to longer-term commitments should be a top priority.
            """
        )
with chart_col4:
    internet_vs_churn_chart()
    with st.expander("Insights"):
        st.write(
            """
            - Fiber Optic customers have the highest churn rate at 41.8%, compared to DSL users at 18.9%.
            - Customers with no internet service have the lowest churn rate (7.2%).
            - High Fiber Optic churn could point to issues with premium pricing, service expectations, or competitor options.
            """
        )

st.write("  ") 

chart_col5, chart_col6 = st.columns(2)
with chart_col5:
    payment_vs_churn_chart()
    with st.expander("Insights"):
        st.write(
            """
            - Electronic Check users experience the highest churn rate by far at 45.1%.
            - Automatic payment methods (Credit Card and Bank Transfer) have significantly lower churn rates (~15% to 17%).
            - Encouraging Electronic Check users to enroll in automatic payments is a viable churn reduction strategy.
            """
        )
with chart_col6:
    tenure_distribution_chart()
    with st.expander("Insights"):
        st.write(
            """
            - The median tenure for churned customers is just 10 months, compared to 38 months for retained customers.
            - Churn risk is heavily concentrated in the first year of the customer lifecycle.
            - Retention efforts should focus heavily on onboarding and the early months of service.
            """
        )

monthly_charges_chart()
with st.expander("Insights"):
    st.write(
        """
        - Churned customers have a higher median monthly charge ($79.70) than retained customers ($64.50).
        - High monthly charges, particularly in the $70–$100 range, correspond to a higher concentration of churn.
        - Price sensitivity plays a major role; customer retention may improve with discount incentives or bundle optimization.
        """
    )

correlation_chart()
with st.expander("Insights"):
    st.write(
        """
        - **Tenure** has the strongest negative correlation with churn (-0.35), reinforcing that customer longevity is the key driver of retention.
        - **Monthly Charges** show a positive correlation with churn (0.19), confirming that higher billing amounts increase the likelihood of churn.
        - **Total Charges** have a negative correlation with churn (-0.20) because higher total charges accumulate over long, stable tenures.
        """
    )

contract_payment_heatmap()
with st.expander("Insights"):
    st.write(
        """
        Month-to-Month + Electronic Check has the highest churn rate.
        Two-Year + Automatic Payment shows the strongest customer retention.
        Combining these features may improve predictive performance.
        """
    )

# ── Overall Summary ─────────────────────────────────────────────────────────
st.write("")
st.divider()
st.markdown("### 🧾 Overall Summary")
st.caption("Key findings distilled from all charts above.")
st.write("")

sum_col1, sum_col2 = st.columns(2)

with sum_col1:
    st.metric(label="📋 Month-to-Month Churn Rate", value="42.6%", delta="vs 2.8% on Two-Year contracts", delta_color="inverse")
    st.write("Migrating high-risk customers to annual plans is the single highest-impact retention lever.")
    st.write("")

    st.metric(label="💳 Electronic Check Churn Rate", value="45.1%", delta="vs ~15–17% for auto payments", delta_color="inverse")
    st.write("Encouraging customers to switch to automatic payments could yield an immediate drop in attrition.")

with sum_col2:
    st.metric(label="📡 Fiber Optic Churn Rate", value="41.8%", delta="vs 18.9% for DSL users", delta_color="inverse")
    st.write("Premium-tier users have high expectations. Pricing and service quality need close monitoring.")
    st.write("")

    st.metric(label="📅 Median Tenure — Churned Customers", value="10 months", delta="vs 38 months for retained", delta_color="inverse")
    st.write("Churn is heavily front-loaded. Early onboarding and engagement are essential to long-term loyalty.")

st.write("")
st.info(
    "💡 **Strategic Recommendation:** Focus retention programs on customers who are on Month-to-Month contracts, "
    "use Fiber Optic internet, pay via Electronic Check, and have been with the company for less than 12 months. "
    "These four overlapping risk factors consistently predict the highest churn probability across all charts."
)
