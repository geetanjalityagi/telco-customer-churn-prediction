import streamlit as st
import pandas as pd
import plotly.express as px

def insights_tab(df):
    col1, col2 = st.columns(2)

    with col1:
        # Churn Pie Chart
        df_churn = df["Churn"].value_counts().reset_index()
        df_churn.columns = ["Status", "Count"]
        df_churn["Status"] = df_churn["Status"].map({"Yes": "Churned", "No": "Retained"})
                        
        fig_pie = px.pie(
                df_churn,
                names="Status",
                values="Count",
                hole=0.4,
                title="Churn Status Distribution",
                color="Status",
                color_discrete_map={"Churned": "#ef5350", "Retained": "#66bb6a"}
            )
        fig_pie.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))

        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Contract Type vs Churn Stacked/Grouped Bar Chart
        df_contract = df.groupby(["Contract", "Churn"]).size().reset_index(name="Count")
        df_contract["Churn"] = df_contract["Churn"].map({"Yes": "Churned", "No": "Retained"})
                
        fig_contract = px.bar(
            df_contract,
            x="Contract",
            y="Count",
            color="Churn",
            barmode="group",
            title="Churn by Contract Type",
            color_discrete_map={"Churned": "#ef5350", "Retained": "#66bb6a"}
        )
        fig_contract.update_layout(
            height=350, 
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Contract Type",
            yaxis_title="Customer Count"
        )
        st.plotly_chart(fig_contract, use_container_width=True)

    st.write(" ")
    col3, col4 = st.columns(2)

    with col3:
        # Monthly Charges vs Churn Box Plot
        fig_box_charge = px.box(
            df,
            x="Churn",
            y="MonthlyCharges",
            color="Churn",
            title="Monthly Charges vs Churn Status",
            color_discrete_map={"Yes": "#ef5350", "No": "#66bb6a"},
            labels={"Churn": "Churned?"}
        )
        fig_box_charge.update_layout(
            height=350, 
            margin=dict(l=20, r=20, t=40, b=20),
            yaxis_title="Monthly Charges ($)"
        )
        st.plotly_chart(fig_box_charge, use_container_width=True)

    with col4:
         # Tenure vs Churn Box Plot
        fig_box_tenure = px.box(
            df,
            x="Churn",
            y="tenure",
            color="Churn",
            title="Tenure (Months) vs Churn Status",
            color_discrete_map={"Yes": "#ef5350", "No": "#66bb6a"},
            labels={"Churn": "Churned?"}
        )
        fig_box_tenure.update_layout(
            height=350, 
            margin=dict(l=20, r=20, t=40, b=20),
            yaxis_title="Tenure (Months)"
        )
        st.plotly_chart(fig_box_tenure, use_container_width=True)

    st.write("")
    col5, col6 = st.columns(2)

    with col5:
        df_payment = df.groupby(["PaymentMethod", "Churn"]).size().reset_index(name="Count")
        df_payment["Churn"] = df_payment["Churn"].map({"Yes": "Churned", "No": "Retained"})
                        
        fig_payment = px.bar(
            df_payment,
            x="PaymentMethod",
            y="Count",
            color="Churn",
            barmode="group",
            title="Churn by Payment Method",
            color_discrete_map={"Churned": "#ef5350", "Retained": "#66bb6a"}
        )
        fig_payment.update_layout(
            height=350, 
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Payment Method",
            yaxis_title="Customer Count"
        )
        st.plotly_chart(fig_payment, use_container_width=True)

    with col6:
        df_internet = df.groupby(["InternetService", "Churn"]).size().reset_index(name="Count")
        df_internet["Churn"] = df_internet["Churn"].map({"Yes": "Churned", "No": "Retained"})
                        
        fig_internet = px.bar(
            df_internet,
            x="InternetService",
            y="Count",
            color="Churn",
            barmode="group",
            title="Churn by Internet Service",
            # color_discrete_map={"Churned": "#ef5350", "Retained": "#66bb6a"}
        )
        fig_internet.update_layout(
            height=350, 
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Internet Service",
            yaxis_title="Customer Count"
        )
        st.plotly_chart(fig_internet, use_container_width=True)
                