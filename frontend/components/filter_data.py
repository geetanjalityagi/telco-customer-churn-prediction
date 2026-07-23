import streamlit as st

# Keys for all filter widgets
_FILTER_KEYS = [
    "gender_multiselect",
    "contract_multiselect",
    "payment_multiselect",
    "internet_multiselect",
    "partner_multiselect",
    "dependents_multiselect",
    "tenure_slider",
]

def filter_data(df):
    original_df = df.copy()

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

    # ── Seed session state defaults only on very first load ──────────────────
    # This ensures Streamlit never resets a user's selection on re-run.
    if "gender_multiselect" not in st.session_state:
        st.session_state["gender_multiselect"]     = sorted(original_df["gender"].unique().tolist())
        st.session_state["contract_multiselect"]   = sorted(original_df["Contract"].unique().tolist())
        st.session_state["payment_multiselect"]    = sorted(original_df["PaymentMethod"].unique().tolist())
        st.session_state["internet_multiselect"]   = sorted(original_df["InternetService"].unique().tolist())
        st.session_state["partner_multiselect"]    = sorted(original_df["Partner"].unique().tolist())
        st.session_state["dependents_multiselect"] = sorted(original_df["Dependents"].unique().tolist())
        st.session_state["tenure_slider"]          = (
            int(original_df["tenure"].min()),
            int(original_df["tenure"].max()),
        )

    # ── Reset Filters button ─────────────────────────────────────────────────
    if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
        for key in _FILTER_KEYS:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    with st.sidebar.expander("🛠️ Active Filters", expanded=True):
        # Gender Filter
        gender = sorted(original_df["gender"].unique().tolist())
        selected_gender = st.multiselect(
            "👤 Gender", gender, key="gender_multiselect"
        )
        df = df[df["gender"].isin(selected_gender)]

        # Contract Type Filter
        contracts = sorted(original_df["Contract"].unique().tolist())
        selected_contracts = st.multiselect(
            "📄 Contract Type", contracts, key="contract_multiselect"
        )
        df = df[df["Contract"].isin(selected_contracts)]

        # Payment Method Filter
        payment_methods = sorted(original_df["PaymentMethod"].unique().tolist())
        selected_payments = st.multiselect(
            "💳 Payment Method", payment_methods, key="payment_multiselect"
        )
        df = df[df["PaymentMethod"].isin(selected_payments)]

        # Internet Service Filter
        internet_services = sorted(original_df["InternetService"].unique().tolist())
        selected_internet = st.multiselect(
            "🌐 Internet Service", internet_services, key="internet_multiselect"
        )
        df = df[df["InternetService"].isin(selected_internet)]

        # Partner Filter
        partner_options = sorted(original_df["Partner"].unique().tolist())
        selected_partner = st.multiselect(
            "💑 Has Partner", partner_options, key="partner_multiselect"
        )
        df = df[df["Partner"].isin(selected_partner)]

        # Dependents Filter
        dependents_options = sorted(original_df["Dependents"].unique().tolist())
        selected_dependents = st.multiselect(
            "👨‍👩‍👧 Has Dependents", dependents_options, key="dependents_multiselect"
        )
        df = df[df["Dependents"].isin(selected_dependents)]

        # Tenure Slider
        min_tenure = int(original_df["tenure"].min())
        max_tenure = int(original_df["tenure"].max())
        tenure_range = st.slider(
            "⏳ Tenure (months)",
            min_value=min_tenure,
            max_value=max_tenure,
            key="tenure_slider",
        )
        df = df[(df["tenure"] >= tenure_range[0]) & (df["tenure"] <= tenure_range[1])]

    return df