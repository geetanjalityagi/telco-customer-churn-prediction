import streamlit as st
import pandas as pd
import plotly.express as px
from utils.sidebar import render_sidebar
from components.filter_data import filter_data
from components.insights import insights_tab

# Set up page configurations
st.set_page_config(page_title="Customer Explorer", page_icon="🔍", layout="wide")
render_sidebar("Customer Explorer")

# Load and prepare processed customer dataset
df = pd.read_csv("data/processed.csv")
total_records = len(df)

# Header Section
st.title("🔍 Customer Explorer")
st.caption(
    "Explore customer demographics, service usages, billing patterns, and cohort distributions. "
    "Use the filtering widgets in the left sidebar to isolate specific segments."
)

# Apply filters from the sidebar component
filtered_df = filter_data(df)
filtered_records = len(filtered_df)

if filtered_records == 0:
    st.warning("⚠️ No customers match the current filter selection. Please adjust your filters in the sidebar.")
else:
    # ── Organize Interface with Tabs ──────────────────────────────────────────
    tab_overview, tab_table, tab_lookup = st.tabs([
        "📊 Cohort Overview & Stats",
        "📋 Cohort Data Table",
        "🔍 Individual Customer Lookup"
    ])
    
    # Calculate cohort key figures
    churn_yes_count = len(filtered_df[filtered_df["Churn"] == "Yes"])
    cohort_churn_rate = (churn_yes_count / filtered_records * 100) if filtered_records > 0 else 0.0
    percent_of_total = (filtered_records / total_records * 100)
    avg_monthly = filtered_df["MonthlyCharges"].mean()
    avg_tenure = filtered_df["tenure"].mean()
    
    # ── TAB 1: COHORT OVERVIEW & STATS ────────────────────────────────────────
    with tab_overview:
        st.markdown("### 📈 Cohort Key Performance Indicators")
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        with kpi_col1:
            st.metric(
                label="Cohort Size", 
                value=f"{filtered_records:,}", 
                delta=f"{percent_of_total:.1f}% of total base",
                delta_color="blue"
            )
        with kpi_col2:
            st.metric(
                label="Cohort Churn Rate", 
                value=f"{cohort_churn_rate:.2f}%", 
                delta=f"{churn_yes_count:,} churned customers",
                delta_color="inverse"
            )
        with kpi_col3:
            st.metric(
                label="Avg Monthly Charges", 
                value=f"${avg_monthly:.2f}"
            )
        with kpi_col4:
            st.metric(
                label="Avg Tenure", 
                value=f"{avg_tenure:.1f} months"
            )
            
        st.divider()
        st.markdown("### 📊 Cohort Distributions")
        insights_tab(filtered_df)
        
    # ── TAB 2: COHORT DATA TABLE ──────────────────────────────────────────────
    with tab_table:
        st.markdown("### 📋 Cohort Records & Export")
        st.markdown(
            "Below is the complete tabular list of customers within the active filtered cohort. "
            "You can sort, filter, and search directly within the interactive table, or download it as a CSV."
        )
        
        # Display formatted cohort table
        st.dataframe(filtered_df, use_container_width=True)
        
        # CSV Export functionality
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cohort as CSV",
            data=csv,
            file_name="customer_cohort.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    # ── TAB 3: INDIVIDUAL CUSTOMER LOOKUP ─────────────────────────────────────
    with tab_lookup:
        st.markdown("### 🔍 Individual Customer Profile Deep-Dive")
        st.markdown(
            "Select or search for a customer ID from the active cohort to explore their details, "
            "demographic characteristics, contract billing options, and service subscriptions."
        )
        
        cohort_cust_ids = sorted(filtered_df["customerID"].tolist())
        
        lookup_col1, lookup_col2 = st.columns([2, 1])
        with lookup_col1:
            input_mode = st.radio(
                "Search Method",
                options=["Select from Active Cohort Dropdown", "Type Customer ID Manually"],
                horizontal=True,
                label_visibility="collapsed"
            )
            
            if input_mode == "Select from Active Cohort Dropdown":
                max_list = 500
                list_ids = cohort_cust_ids[:max_list]
                selected_id = st.selectbox(
                    f"Choose Customer ID (showing first {min(len(cohort_cust_ids), max_list)} of {len(cohort_cust_ids)} in current cohort)",
                    options=list_ids,
                    index=0 if list_ids else None,
                    key="customer_select_dropdown"
                )
            else:
                selected_id = st.text_input(
                    "Enter Customer ID Manually", 
                    placeholder="e.g., 7590-VHVEG",
                    key="customer_text_input"
                ).strip()
        
        if not selected_id:
            st.info("💡 Please select or enter a Customer ID to view their profile.")
        else:
            # Query customer record from the full database
            cust_row = df[df["customerID"] == selected_id]
            
            if cust_row.empty:
                st.error(f"❌ Customer ID '{selected_id}' not found in database. Check spelling or try selecting from the dropdown.")
            else:
                customer = cust_row.iloc[0]
                
                # Check historic churn status
                is_churned = customer["Churn"] == "Yes"
                status_color = "#ef5350" if is_churned else "#66bb6a"
                status_label = "CHURNED ❌" if is_churned else "ACTIVE / RETAINED ✅"
                
                st.markdown("---")
                
                # Header Badge for Customer ID
                st.markdown(
                    f"""
                    <div style="background-color: {status_color}12; padding: 15px; border-radius: 8px; border-left: 6px solid {status_color}; margin-bottom: 20px;">
                        <h3 style="margin: 0; padding: 0; color: #1e293b;">👤 Customer Profile: {selected_id}</h3>
                        <p style="margin: 5px 0 0 0; font-size: 1.05rem; color: #334155;">
                            Historical Account Status: <strong style="color: {status_color};">{status_label}</strong>
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Divide attributes into structured columns
                info_col1, info_col2 = st.columns(2)
                
                with info_col1:
                    # Demographics Section
                    st.markdown("#### 👤 Demographics & Profile")
                    gender_icon = "👩" if customer["gender"] == "Female" else "👨"
                    senior_status = "Yes (Age 65+)" if customer["SeniorCitizen"] == 1 else "No"
                    
                    st.markdown(f"**Gender:** {gender_icon} {customer['gender']}")
                    st.markdown(f"**Senior Citizen:** {senior_status}")
                    st.markdown(f"**Has Partner:** {'Yes 💑' if customer['Partner'] == 'Yes' else 'No'}")
                    st.markdown(f"**Has Dependents:** {'Yes 👨‍👩‍👧' if customer['Dependents'] == 'Yes' else 'No'}")
                    
                    st.markdown("")
                    
                    # Billing Section
                    st.markdown("#### 💳 Billing & Contract Settings")
                    st.markdown(f"**Contract Duration:** `{customer['Contract']}`")
                    st.markdown(f"**Tenure:** `{customer['tenure']} months`")
                    st.markdown(f"**Monthly Charges:** `${customer['MonthlyCharges']:.2f}`")
                    
                    # Gracefully handle total charges formatting
                    try:
                        total_ch = float(customer['TotalCharges'])
                        total_ch_str = f"${total_ch:.2f}"
                    except Exception:
                        total_ch_str = f"{customer['TotalCharges']}"
                        
                    st.markdown(f"**Total Charges:** `{total_ch_str}`")
                    st.markdown(f"**Payment Method:** `{customer['PaymentMethod']}`")
                    st.markdown(f"**Paperless Billing:** {'Yes 📄' if customer['PaperlessBilling'] == 'Yes' else 'No'}")

                with info_col2:
                    # Services Section
                    st.markdown("#### 📡 Subscribed Services")
                    
                    services = {
                        "Phone Service": customer.get("PhoneService", "No"),
                        "Multiple Lines": customer.get("MultipleLines", "No"),
                        "Internet Service": customer.get("InternetService", "No"),
                        "Online Security": customer.get("OnlineSecurity", "No"),
                        "Online Backup": customer.get("OnlineBackup", "No"),
                        "Device Protection": customer.get("DeviceProtection", "No"),
                        "Tech Support": customer.get("TechSupport", "No"),
                        "Streaming TV": customer.get("StreamingTV", "No"),
                        "Streaming Movies": customer.get("StreamingMovies", "No")
                    }
                    
                    for svc, status in services.items():
                        if status == "Yes" or (svc == "InternetService" and status != "No") or (svc == "MultipleLines" and status == "Yes"):
                            # Active Service Badge
                            badge_style = "background-color: #e8f5e9; color: #1b5e20;" if svc == "InternetService" else "background-color: #e3f2fd; color: #0d47a1;"
                            status_text = status if svc == "InternetService" else "Active"
                            badge_html = f"<span style='{badge_style} padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 0.85rem; margin-right: 8px;'>{status_text}</span>"
                            label_html = f"<strong style='color: #1e293b;'>{svc}</strong>"
                        elif status in ["No internet service", "No phone service"]:
                            # Non-Applicable Badge
                            badge_html = f"<span style='background-color: #f1f5f9; color: #64748b; padding: 2px 8px; border-radius: 4px; font-size: 0.85rem; margin-right: 8px;'>N/A</span>"
                            label_html = f"<span style='color: #64748b;'>{svc}</span>"
                        else:
                            # Inactive Service Badge
                            badge_html = f"<span style='background-color: #fef2f2; color: #991b1b; padding: 2px 8px; border-radius: 4px; font-size: 0.85rem; margin-right: 8px;'>Inactive</span>"
                            label_html = f"<span style='color: #475569;'>{svc}</span>"
                        
                        st.markdown(f"<div style='margin-bottom: 6px;'>{badge_html} {label_html}</div>", unsafe_allow_html=True)
                
                # Rule-based localized account insights
                st.markdown("---")
                st.markdown("#### 💡 Customer Account Health & Retention Insights")
                
                if not is_churned:
                    insights_list = []
                    if customer["Contract"] == "Month-to-month":
                        insights_list.append("⚠️ **Contract Vulnerability:** This customer is on a month-to-month subscription. Consider shifting them to a 1-year or 2-year contract to lower churn risk.")
                    if customer["PaymentMethod"] == "Electronic check":
                        insights_list.append("⚠️ **Payment Method Attrition:** Customer uses Electronic Check. Transitioning them to automated credit card/bank transfer options is highly recommended.")
                    if customer["InternetService"] == "Fiber optic":
                        insights_list.append("⚠️ **High Churn Fiber optic segment:** Premium fiber subscriptions exhibit high churn rates. Keep pricing competitive and monitor service performance.")
                    if customer["tenure"] < 12:
                        insights_list.append("⚠️ **Early Lifecycle Phase:** Customer is in their first 12 months. Early onboarding support and custom discounts could stabilize long-term retention.")
                    
                    if not insights_list:
                        st.success("✅ **Robust Loyalty Profile:** The customer's account settings (long-term contract, automatic payments, and high tenure) align with the lowest historic risk cohorts.")
                    else:
                        for insight in insights_list:
                            st.markdown(insight)
                else:
                    st.info(
                        "ℹ️ **Historical Study Note:** This customer has already churned. "
                        "Examine their profile details to understand overlapping risk factor patterns (e.g. Month-to-month contract, short tenure, etc.) "
                        "and configure predictive defenses for similar active profiles."
                    )