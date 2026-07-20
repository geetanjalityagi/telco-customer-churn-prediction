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

def internet_vs_churn_chart():
    internet_vs_churn = dashboard_data["charts"]["internet_vs_churn"]

    rows = []

    for internet, churn_data in internet_vs_churn.items():
        for churn_status, count in churn_data.items():
            rows.append({
                "Internet Service": internet,
                "Churn": churn_status,
                "Customers": count
            })

    df_internet_churn = pd.DataFrame(rows)

    fig = px.bar(
    df_internet_churn,
    x="Internet Service",
    y="Customers",
    color="Churn",
    barmode="group",
    text="Customers",
    title="Which Internet Services are risky?"
)

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Internet Service",
        yaxis_title="Number of Customers",
        legend_title="Churn"
    )

    st.plotly_chart(fig, use_container_width=True)

def payment_vs_churn_chart():
    payment_vs_churn = dashboard_data["charts"]["payment_vs_churn"]

    rows = []

    for payment, churn_data in payment_vs_churn.items():
        for churn_status, count in churn_data.items():
            rows.append({
                "Payment Method": payment,
                "Churn": churn_status,
                "Customers": count
            })

    df_payment_churn = pd.DataFrame(rows)

    fig = px.bar(
    df_payment_churn,
    x="Payment Method",
    y="Customers",
    color="Churn",
    barmode="group",
    text="Customers",
    title="Churn by Payment Method"
)

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Internet Service",
        yaxis_title="Number of Customers",
        legend_title="Churn"
    )

    st.plotly_chart(fig, use_container_width=True)


def tenure_distribution_chart():
    tenure_distribution = dashboard_data["charts"]["tenure_distribution"]

    rows = []
    for churn_status, tenures in tenure_distribution.items():
        for t in tenures:
            rows.append({"Churn": churn_status, "Tenure (Months)": t})

    df_tenure = pd.DataFrame(rows)

    fig = px.box(
        df_tenure,
        x="Churn",
        y="Tenure (Months)",
        color="Churn",
        title="Tenure Distribution by Churn"
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


def correlation_chart():
    correlation = dashboard_data["charts"]["correlation_matrix"]

    corr_df = pd.DataFrame(correlation)

    fig = px.imshow(
    corr_df,
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale="RdBu_r",
    title="Feature Correlation Heatmap"
)

    fig.update_layout(
        xaxis_title="Features",
        yaxis_title="Features"
    )

    st.plotly_chart(fig, use_container_width=True)