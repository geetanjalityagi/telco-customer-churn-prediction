import streamlit as st
import pandas as pd
from utils.sidebar import render_sidebar
from components.filter_data import filter_data
from components.insights import insights_tab

st.set_page_config(page_title="Customer Explorer", page_icon="🔍", layout="wide")
render_sidebar("Customer Explorer")

df = pd.read_csv("data/processed.csv")
total_records = len(df)

st.title("🔍 Customer Explorer")
st.caption(
    "Explore customer demographics, service usages, billing patterns, and cohort distributions. "
    "Use the filtering widgets in the left sidebar to isolate specific segments."
)

filtered_df = filter_data(df)
filtered_records = filtered_df.shape[0]

if filtered_records == 0:
    st.warning("⚠️ No customers match the current filter selection. Please adjust your filters in the sidebar.")
else:
    tab_overview, tab_table, tab_lookup = st.tabs([
        "📊 Cohort Overview & Stats",
        "📋 Cohort Data Table",
        "🔍 Individual Customer Lookup"
    ])
    
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
        st.markdown("### 📋 Records & Export")
        st.markdown(
            "Below is the complete tabular list of customers within the active filtered cohort. "
            "You can sort, filter, and search directly within the interactive table, or download it as a CSV."
        )
        st.info(
            f"📊 Showing **{filtered_records:,} customers** × {filtered_df.shape[1]} columns "
            f"({percent_of_total:.1f}% of the full {total_records:,}-customer base)"
        )
        st.dataframe(filtered_df, use_container_width=True)
        
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
        st.caption(
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
            cust_row = df[df["customerID"] == selected_id]

            if cust_row.empty:
                st.error(f"❌ Customer ID '{selected_id}' not found in the database. Check spelling or try selecting from the dropdown.")
            else:
                customer = cust_row.iloc[0]
                is_churned = customer["Churn"] == "Yes"

                st.divider()

                # ── Status Banner ──────────────────────────────────────────
                if is_churned:
                    st.error(f"👤 **Customer Profile: {selected_id}** — Historical Account Status: **CHURNED ❌**")
                else:
                    st.success(f"👤 **Customer Profile: {selected_id}** — Historical Account Status: **ACTIVE / RETAINED ✅**")

                st.write("")

                # ── Demographics & Billing | Services ─────────────────────
                info_col1, info_col2 = st.columns(2)

                with info_col1:
                    # --- Demographics ---
                    st.markdown("#### 👤 Demographics & Profile")
                    gender_icon = "👩" if customer["gender"] == "Female" else "👨"
                    senior_status = "Yes (Age 65+)" if customer["SeniorCitizen"] == 1 else "No"

                    demo_data = {
                        "Field": ["Gender", "Senior Citizen", "Has Partner", "Has Dependents"],
                        "Value": [
                            f"{gender_icon} {customer['gender']}",
                            senior_status,
                            "Yes 💑" if customer["Partner"] == "Yes" else "No",
                            "Yes 👨‍👩‍👧" if customer["Dependents"] == "Yes" else "No",
                        ],
                    }
                    st.dataframe(
                        demo_data,
                        use_container_width=True,
                        hide_index=True,
                    )

                    st.write("")

                    # --- Billing ---
                    st.markdown("#### 💳 Billing & Contract")
                    try:
                        total_ch_str = f"${float(customer['TotalCharges']):.2f}"
                    except Exception:
                        total_ch_str = str(customer["TotalCharges"])

                    billing_data = {
                        "Field": [
                            "Contract Duration",
                            "Tenure",
                            "Monthly Charges",
                            "Total Charges",
                            "Payment Method",
                            "Paperless Billing",
                        ],
                        "Value": [
                            str(customer["Contract"]),
                            f"{customer['tenure']} months",
                            f"${customer['MonthlyCharges']:.2f}",
                            total_ch_str,
                            str(customer["PaymentMethod"]),
                            "Yes 📄" if customer["PaperlessBilling"] == "Yes" else "No",
                        ],
                    }
                    st.dataframe(
                        billing_data,
                        use_container_width=True,
                        hide_index=True,
                    )

                with info_col2:
                    st.markdown("#### 📡 Subscribed Services")

                    SERVICE_ICONS = {
                        "Phone Service":    "📞",
                        "Multiple Lines":   "📲",
                        "Internet Service": "🌐",
                        "Online Security":  "🔒",
                        "Online Backup":    "☁️",
                        "Device Protection":"🛡️",
                        "Tech Support":     "🛠️",
                        "Streaming TV":     "📺",
                        "Streaming Movies": "🎬",
                    }
                    services_raw = {
                        "Phone Service":    customer.get("PhoneService", "No"),
                        "Multiple Lines":   customer.get("MultipleLines", "No"),
                        "Internet Service": customer.get("InternetService", "No"),
                        "Online Security":  customer.get("OnlineSecurity", "No"),
                        "Online Backup":    customer.get("OnlineBackup", "No"),
                        "Device Protection":customer.get("DeviceProtection", "No"),
                        "Tech Support":     customer.get("TechSupport", "No"),
                        "Streaming TV":     customer.get("StreamingTV", "No"),
                        "Streaming Movies": customer.get("StreamingMovies", "No"),
                    }

                    svc_names, svc_statuses = [], []
                    for svc, raw in services_raw.items():
                        icon = SERVICE_ICONS.get(svc, "")
                        label = f"{icon} {svc}"
                        if raw in ["No internet service", "No phone service"]:
                            status_display = "➖ N/A"
                        elif raw == "No":
                            status_display = "❌ Inactive"
                        elif svc == "Internet Service":
                            status_display = f"✅ {raw}"
                        else:
                            status_display = "✅ Active"
                        svc_names.append(label)
                        svc_statuses.append(status_display)

                    st.dataframe(
                        {"Service": svc_names, "Status": svc_statuses},
                        use_container_width=True,
                        hide_index=True,
                    )

                # ── Financial KPI Metrics ──────────────────────────────────
                st.divider()
                st.markdown("#### 💰 Account Financial Snapshot")
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("📅 Tenure", f"{customer['tenure']} months")
                with m2:
                    st.metric("💵 Monthly Charges", f"${customer['MonthlyCharges']:.2f}")
                with m3:
                    st.metric("🧾 Total Charges", total_ch_str)

                # ── Retention Insights ─────────────────────────────────────
                st.divider()
                st.markdown("#### 💡 Account Health & Retention Insights")

                if not is_churned:
                    insights_list = []
                    if customer["Contract"] == "Month-to-month":
                        insights_list.append("⚠️ **Contract Vulnerability:** On a month-to-month plan — consider shifting to a 1-year or 2-year contract to reduce churn risk.")
                    if customer["PaymentMethod"] == "Electronic check":
                        insights_list.append("⚠️ **Payment Risk:** Uses Electronic Check. Automated credit card or bank transfer is strongly recommended.")
                    if customer["InternetService"] == "Fiber optic":
                        insights_list.append("⚠️ **Fiber optic Churn Risk:** Premium fiber subscribers show elevated churn. Monitor service quality and pricing competitiveness.")
                    if customer["tenure"] < 12:
                        insights_list.append("⚠️ **Early Lifecycle:** First 12 months — early onboarding support and discounts can stabilize long-term retention.")

                    if not insights_list:
                        st.success("✅ **Robust Loyalty Profile:** Long-term contract, automatic payments, and high tenure — this customer aligns with the lowest churn-risk cohort.")
                    else:
                        for insight in insights_list:
                            st.warning(insight)
                else:
                    st.info(
                        "ℹ️ **Historical Study Note:** This customer has already churned. "
                        "Review their profile to identify overlapping risk factors (e.g. month-to-month contract, short tenure) "
                        "and apply targeted defences to similar active customers."
                    )
