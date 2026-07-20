import streamlit as st
import pandas as pd
import requests
import plotly.express as px


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

def churn_distribution_chart():
    churn_distribution = dashboard_data["charts"]["churn_distribution"]

    df_churn = pd.DataFrame({
    "Churn": list(churn_distribution.keys()),
    "Customers": list(churn_distribution.values())
    })

    fig = px.pie(
        df_churn,
        names="Churn",
        values="Customers",
        hole=0.5,
        title="Customer Churn Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

def contract_distribution_chart():
    contract_distribution = dashboard_data["charts"]["contract_distribution"]
    df_contract = pd.DataFrame({
    "Contract Type": list(contract_distribution.keys()),
    "Customers": list(contract_distribution.values())
    })

    fig = px.bar(
    df_contract,
    x="Contract Type",
    y="Customers",
    title="Customer Distribution by Contract Type",
    text="Customers"
)

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Contract Type",
        yaxis_title="Number of Customers"
    )

    st.plotly_chart(fig, use_container_width=True)

def contract_vs_churn_chart():
    contract_vs_churn = dashboard_data["charts"]["contract_vs_churn"]

    rows = []

    for contract, churn_data in contract_vs_churn.items():
        for churn_status, count in churn_data.items():
            rows.append({
                "Contract Type": contract,
                "Churn": churn_status,
                "Customers": count
            })

    df_contract_churn = pd.DataFrame(rows)

    fig = px.bar(
    df_contract_churn,
    x="Contract Type",
    y="Customers",
    color="Churn",
    barmode="group",
    text="Customers",
    title="Churn by Contract Type"
)

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Contract Type",
        yaxis_title="Number of Customers",
        legend_title="Churn"
    )

    st.plotly_chart(fig, use_container_width=True)

def internet_service_chart():
    internet_service = dashboard_data["charts"]["internet_service"]

    df_contract = pd.DataFrame({
    "Internet Service": list(internet_service.keys()),
    "Customers": list(internet_service.values())
    })

    fig = px.bar(
    df_contract,
    x="Customers",
    y="Internet Service",
    orientation="h",
    text="Customers",
    title="Customer Distribution by Internet Service"
)

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Number of Customers",
        yaxis_title="Internet Service"
    )

    st.plotly_chart(fig, use_container_width=True)

def payment_method_chart():
    payment_method = dashboard_data["charts"]["payment_method"]

    df_payment = pd.DataFrame({
        "Payment Method": list(payment_method.keys()),
        "Customers": list(payment_method.values())
    })

    fig = px.pie(
        df_payment,
        names="Payment Method",
        values="Customers",
        hole=0.5,
        title="Payment Method Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

def tenure_distribution_chart():
    tenure_distribution = dashboard_data["charts"]["tenure_distribution"]

    df_tenure = pd.DataFrame({
        "Tenure Range (Months)": list(tenure_distribution.keys()),
        "Customers": list(tenure_distribution.values())
    })

    fig = px.funnel(
        df_tenure,
        x="Customers",
        y="Tenure Range (Months)",
        title="Customer Tenure Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

def monthly_charges_chart():
    monthly_charges = pd.DataFrame({
        "MonthlyCharges": dashboard_data["charts"]["monthly_charges"]
    })

    fig = px.histogram(
        monthly_charges,
        x="MonthlyCharges",
        nbins=30,
        title="Monthly Charges Distribution",
        marginal="box"
    )

    fig.update_layout(
        xaxis_title="Monthly Charges ($)",
        yaxis_title="Number of Customers"
    )

    st.plotly_chart(fig, use_container_width=True)
