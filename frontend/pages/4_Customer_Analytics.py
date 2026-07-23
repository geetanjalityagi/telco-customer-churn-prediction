import streamlit as st
import pandas as pd
import plotly.express as px
from utils.sidebar import render_sidebar
from components.filter_data import filter_data
from components.insights import insights_tab

st.set_page_config(page_title="Customer Analytics", page_icon="🔍", layout="wide")
render_sidebar("Customer Analytics")

df = pd.read_csv("data/processed.csv")
total_records = len(df)

st.title("🔍 Customer Cohort Analytics")
st.caption("Slice and dice customer groups. Use the filters on the left sidebar to isolate specific segments and analyze their behaviors.")

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
    
    insights_tab(filtered_df)

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