import streamlit as st
from utils.sidebar import render_sidebar
import requests

st.set_page_config(page_title="Single Prediction", layout="wide")
render_sidebar("Single Prediction")
# st.title("Single Prediction")

API_BASE_URL = "http://localhost:8000/api/v1"
PREDICT_URL = f"{API_BASE_URL}/predict"

RISK_COLOR = {
    "Very Low": "#2e7d32",
    "Low": "#2e7d32",
    "Moderate": "#f9a825",
    "High": "#ef6c00",
    "Critical": "#c62828",
}

st.title("📊 Customer Churn Prediction")
st.caption("Enter a customer's profile to score their churn risk and see what's driving it.")

with st.form("customer_form"):
    st.subheader("Customer Profile")

    col1, col2, col3 = st.columns(3)
    with col1:
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner = st.selectbox("Has Partner", ["No", "Yes"])
        dependents = st.selectbox("Has Dependents", ["No", "Yes"])
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
    with col2:
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
        internet_service = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    with col3:
        paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment_method = st.selectbox(
            "Payment Method",
            ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
        )
        monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=70.0, step=0.5)
        total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=840.0, step=1.0)

    st.markdown("**Add-on Services**")
    addon_options = ["No", "Yes", "No internet service"]
    a1, a2, a3 = st.columns(3)
    with a1:
        online_security = st.selectbox("Online Security", addon_options)
        online_backup = st.selectbox("Online Backup", addon_options)
    with a2:
        device_protection = st.selectbox("Device Protection", addon_options)
        tech_support = st.selectbox("Tech Support", addon_options)
    with a3:
        streaming_tv = st.selectbox("Streaming TV", addon_options)
        streaming_movies = st.selectbox("Streaming Movies", addon_options)

    submitted = st.form_submit_button("Predict Churn", use_container_width=True)

if submitted:
    payload = {
        "SeniorCitizen": 1 if senior_citizen == "Yes" else 0,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
    }

    try:
        with st.spinner("Scoring customer..."):
            response = requests.post(PREDICT_URL, json=payload, timeout=15)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"Couldn't reach the API at {PREDICT_URL}. Is the FastAPI backend running?")
        st.stop()
    except requests.exceptions.HTTPError:
        st.error(f"API returned an error: {response.status_code} — {response.text}")
        st.stop()

    st.divider()
    st.markdown("## 🧾 Customer Churn Prediction Report")

    c1, c2, c3 = st.columns(3)
    with c1:
        emoji = "⚠️" if result["prediction"] == "Will Churn" else "✅"
        st.markdown("Prediction")
        st.markdown(f"#### {emoji} {result['prediction']}")
    with c2:
        st.markdown("Churn Probability")
        st.markdown(f"#### {result['churn_probability']:.1%}")
    with c3:
        st.markdown("Risk Level")
        st.markdown(f"#### {result['risk_emoji']} {result['risk_level']}")


    st.progress(min(result["churn_probability"], 1.0))

    color = RISK_COLOR.get(result["risk_level"], "#616161")
    st.markdown(
        f"<div style='padding:10px;border-radius:8px;background-color:{color}20;"
        f"border-left:6px solid {color};'>"
        f"<b>Priority:</b> {result['priority_stars']} — {result['priority_action']}"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("")

    col_risk, col_protect = st.columns(2)
    with col_risk:
        st.markdown("#### 🔺 Top Risk Factors")
        if result["top_risk_factors"]:
            for i, f in enumerate(result["top_risk_factors"], 1):
                st.markdown(f"**{i}. {f['label']}**  \n`SHAP: +{f['shap_value']:.3f}`")
        else:
            st.markdown("_None — no significant churn-driving factors found._")

    with col_protect:
        st.markdown("#### 🔻 Factors Keeping This Customer Loyal")
        if result["top_protective_factors"]:
            for i, f in enumerate(result["top_protective_factors"], 1):
                st.markdown(f"**{i}. {f['label']}**  \n`SHAP: {f['shap_value']:.3f}`")
        else:
            st.markdown("_None identified._")

    # --- business interpretation -------------------------------------------
    st.markdown("### 📝 Business Interpretation")
    st.info(result["business_interpretation"])

    # --- recommended actions ------------------------------------------------
    st.markdown("### ✅ Recommended Actions")
    for action in result["recommended_actions"]:
        st.markdown(f"- {action}")

    with st.expander("Raw API response (JSON)"):
        st.json(result)
