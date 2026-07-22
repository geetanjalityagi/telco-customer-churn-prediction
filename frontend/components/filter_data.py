import streamlit as st

def filter_data(df):
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style="margin-top: 5px; margin-bottom: 10px; padding-left: 5px;">
            <span style="font-size: 0.85rem; font-weight: 700; color: #a3a8b4; text-transform: uppercase; letter-spacing: 1.5px;">
                🔍 Cohort Filtering
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    with st.sidebar.expander("🛠️ Active Filters", expanded=True):
        # Gender Filter
        gender = sorted(df['gender'].unique())
        selected_gender = st.multiselect("👤 Gender", gender, default=gender, key="gender_multiselect")
        df = df[df['gender'].isin(selected_gender)]

        # Contract Type Filter
        contracts = sorted(df['Contract'].unique())
        selected_contracts = st.multiselect("📄 Contract Type", contracts, default=contracts, key="contract_multiselect")
        df = df[df['Contract'].isin(selected_contracts)]

        # Payment Method Filter
        payment_methods = sorted(df['PaymentMethod'].unique())
        selected_payments = st.multiselect("💳 Payment Method", payment_methods, default=payment_methods, key="payment_multiselect")
        df = df[df['PaymentMethod'].isin(selected_payments)]
        
        # Internet Service Filter
        internet_services = sorted(df['InternetService'].unique())
        selected_internet = st.multiselect("🌐 Internet Service", internet_services, default=internet_services, key="internet_multiselect")
        df = df[df['InternetService'].isin(selected_internet)]
        
        # Partner Filter
        partner_options = sorted(df['Partner'].unique())
        selected_partner = st.multiselect("💑 Has Partner", partner_options, default=partner_options, key="partner_multiselect")
        df = df[df['Partner'].isin(selected_partner)]
        
        # Dependents Filter
        dependents_options = sorted(df['Dependents'].unique())
        selected_dependents = st.multiselect("👨‍👩‍👧 Has Dependents", dependents_options, default=dependents_options, key="dependents_multiselect")
        df = df[df['Dependents'].isin(selected_dependents)]

        # Tenure Slider
        min_tenure, max_tenure = int(df['tenure'].min()), int(df['tenure'].max())
        tenure_range = st.slider("⏳ Tenure (months)", min_value=min_tenure, max_value=max_tenure, value=(min_tenure, max_tenure), key="tenure_slider")
        df = df[(df['tenure'] >= tenure_range[0]) & (df['tenure'] <= tenure_range[1])]
    
    return df

    
    