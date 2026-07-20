import pandas as pd

from app.core.model_loader import ModelBundle
from app.schemas.response import ChurnPredictionResponse, RiskFactor
from app.schemas.request import CustomerInput

BINARY_COLS = [
    "Partner", "Dependents", "PhoneService", "MultipleLines", "OnlineSecurity",
    "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
    "StreamingMovies", "PaperlessBilling",
]

FEATURE_LABELS = {
    "ordinal__Contract": "Month-to-Month Contract",
    "scaler__tenure": "Short Tenure",
    "scaler__MonthlyCharges": "High Monthly Charges",
    "scaler__TotalCharges": "Low Total Spend (New Customer)",
    "nominal__InternetService_Fiber optic": "Fiber Optic Internet",
    "nominal__PaymentMethod_Electronic check": "Electronic Check Payment",
    "remainder__OnlineSecurity": "No Online Security",
    "remainder__TechSupport": "No Tech Support",
    "remainder__PaperlessBilling": "Paperless Billing",
}

SUGGESTIONS = {
    "ordinal__Contract": "Offer a discount to switch from month-to-month to a 1-year or 2-year contract.",
    "nominal__InternetService_Fiber optic": "Review fiber pricing or bundle offers — fiber customers show higher churn.",
    "scaler__tenure": "New customer — enroll in an early-engagement or onboarding loyalty program.",
    "scaler__MonthlyCharges": "Consider a loyalty discount or bundle to reduce bill amount.",
    "scaler__TotalCharges": "Low lifetime spend — engage with a value-added service trial.",
    "nominal__PaymentMethod_Electronic check": "Encourage switching to auto-pay (credit card/bank debit) with a small incentive.",
    "remainder__OnlineSecurity": "Offer a free trial of Online Security add-on.",
    "remainder__TechSupport": "Offer a free trial of Tech Support add-on.",
    "remainder__PaperlessBilling": "No action needed — minor factor.",
}


def get_risk_level(proba: float) -> tuple[str, str]:
    if proba <= 0.20:
        return "Very Low", "🟢"
    elif proba <= 0.40:
        return "Low", "🟢"
    elif proba <= 0.60:
        return "Moderate", "🟡"
    elif proba <= 0.80:
        return "High", "🟠"
    else:
        return "Critical", "🔴"


def get_priority_stars(risk_level: str) -> str:
    mapping = {"Very Low": 1, "Low": 2, "Moderate": 3, "High": 4, "Critical": 5}
    n = mapping.get(risk_level, 1)
    return "⭐" * n


_PRIORITY_ACTION = {
    "Critical": "Immediate Action Required",
    "High": "Prompt Follow-up Recommended",
    "Moderate": "Monitor Periodically",
    "Low": "No Immediate Action Needed",
    "Very Low": "No Immediate Action Needed",
}


def _to_readable_factors(index, values, bundle_metadata_labels=FEATURE_LABELS, suggestions_map=None):
    factors = []
    for feat, val in zip(index, values):
        factors.append(
            RiskFactor(
                feature=feat,
                label=bundle_metadata_labels.get(feat, feat.split("__")[-1]),
                shap_value=float(val),
                suggestion=(suggestions_map or {}).get(feat) if suggestions_map is not None else None,
            )
        )
    return factors


def _join_readable(labels: list[str]) -> str:
    if not labels:
        return ""
    if len(labels) == 1:
        return labels[0]
    return ", ".join(labels[:-1]) + f", and {labels[-1]}"


def explain_prediction(customer: CustomerInput, bundle: ModelBundle) -> ChurnPredictionResponse:
    raw_customer_dict = customer.model_dump()
    customer_df = pd.DataFrame([raw_customer_dict])

    customer_df_encoded = customer_df.copy()
    for col in BINARY_COLS:
        if col in customer_df_encoded.columns and customer_df_encoded[col].dtype == object:
            customer_df_encoded[col] = customer_df_encoded[col].replace({
                "Yes": 1, 
                "No": 0,
                "No internet service": 0,
                "No phone service": 0
            })

    customer_df_encoded = customer_df_encoded[bundle.feature_columns]

    proba = float(bundle.predict_proba(customer_df_encoded))
    pred = int(proba >= bundle.chosen_threshold)
    risk_level, risk_emoji = get_risk_level(proba)

    feature_names, shap_vals = bundle.shap_values(customer_df_encoded)
    contrib = pd.Series(shap_vals, index=feature_names).sort_values(ascending=False)

    top_risk = contrib[contrib > 0].head(3)
    top_protective = contrib[contrib < 0].sort_values().head(3)

    top_risk_factors = _to_readable_factors(top_risk.index, top_risk.values, suggestions_map=SUGGESTIONS)
    top_protective_factors = _to_readable_factors(top_protective.index, top_protective.values)

    readable_risk_labels = [f.label for f in top_risk_factors]
    readable_protective_labels = [f.label for f in top_protective_factors]

    if readable_risk_labels:
        business_interpretation = (
            f"The customer has a {risk_level.lower()} probability of churning, "
            f"primarily driven by: {_join_readable(readable_risk_labels)}."
        )
    else:
        business_interpretation = (
            f"The customer has a {risk_level.lower()} probability of churning. "
            f"No churn-risk factors were identified — instead, the customer is strongly "
            f"retained by: {_join_readable(readable_protective_labels)}."
        )

    recommended_actions = [f.suggestion for f in top_risk_factors if f.suggestion] or [
        "No retention action needed — continue standard engagement and loyalty rewards."
    ]

    return ChurnPredictionResponse(
        prediction="Will Churn" if pred else "Will Stay",
        churn_probability=round(proba, 4),
        risk_level=risk_level,
        risk_emoji=risk_emoji,
        priority_stars=get_priority_stars(risk_level),
        priority_action=_PRIORITY_ACTION[risk_level],
        top_risk_factors=top_risk_factors,
        top_protective_factors=top_protective_factors,
        business_interpretation=business_interpretation,
        recommended_actions=recommended_actions,
    )
