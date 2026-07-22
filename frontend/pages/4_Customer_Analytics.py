import streamlit as st
import pandas as pd
import plotly.express as px
from utils.sidebar import render_sidebar
from components.filter_data import filter_data

st.set_page_config(page_title="Customer Analytics", page_icon="🔍", layout="wide")
render_sidebar("Customer Analytics")

# Load data
df = pd.read_csv("data/processed.csv")
total_records = len(df)

# Page header
st.title("🔍 Customer Cohort Analytics")
st.caption("Slice and dice customer groups. Use the filters on the left sidebar to isolate specific segments and analyze their behaviors.")

# Apply filters
filtered_df = filter_data(df)
filtered_records = len(filtered_df)

if filtered_records == 0:
    st.warning("⚠️ No customers match the current filter selection. Please adjust your filters in the sidebar.")
else:
    # ── KPIs Row ────────────────────────────────────────────────────────────
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate churn rate for the filtered group
    churn_yes_count = len(filtered_df[filtered_df["Churn"] == "Yes"])
    cohort_churn_rate = (churn_yes_count / filtered_records * 100) if filtered_records > 0 else 0.0
    
    # Calculate percentage of total database
    percent_of_total = (filtered_records / total_records * 100)
    
    with col1:
        st.metric(
            label="Cohort Size", 
            value=f"{filtered_records:,}", 
            delta=f"{percent_of_total:.1f}% of total base",
            delta_color="normal"
        )
    with col2:
        st.metric(
            label="Cohort Churn Rate", 
            value=f"{cohort_churn_rate:.2f}%", 
            delta=f"{churn_yes_count:,} churned customers",
            delta_color="inverse"
        )
    with col3:
        avg_monthly = filtered_df["MonthlyCharges"].mean()
        st.metric(
            label="Avg Monthly Charges", 
            value=f"${avg_monthly:.2f}"
        )
    with col4:
        avg_tenure = filtered_df["tenure"].mean()
        st.metric(
            label="Avg Tenure", 
            value=f"{avg_tenure:.1f} months"
        )
        
    # ── Visualizations ───────────────────────────────────────────────────────
    st.write(" ")
    st.markdown("### 📊 Cohort Distributions")
    
    c_col1, c_col2 = st.columns(2)
    
    with c_col1:
        # Churn Pie Chart
        df_churn = filtered_df["Churn"].value_counts().reset_index()
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
        
    with c_col2:
        # Contract Type vs Churn Stacked/Grouped Bar Chart
        df_contract = filtered_df.groupby(["Contract", "Churn"]).size().reset_index(name="Count")
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
    c_col3, c_col4 = st.columns(2)
    
    with c_col3:
        # Monthly Charges vs Churn Box Plot
        fig_box_charge = px.box(
            filtered_df,
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
        
    with c_col4:
        # Tenure vs Churn Box Plot
        fig_box_tenure = px.box(
            filtered_df,
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

    # ── Cohort Data Table and Download ───────────────────────────────────────
    st.divider()
    with st.expander(f"📋 Cohort Records ({filtered_records:,} Customers)", expanded=False):
        # Format table for cleaner display
        display_df = filtered_df.copy()
        
        # Display DataFrame
        st.dataframe(display_df, use_container_width=True)
        
        # CSV Export function
        csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cohort as CSV",
            data=csv,
            file_name="customer_cohort.csv",
            mime="text/csv",
            use_container_width=True
        )