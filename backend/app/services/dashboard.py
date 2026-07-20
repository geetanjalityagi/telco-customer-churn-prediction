import pandas as pd
from app.schemas.dashboard_schema import KPIs, Charts, DashboardResponse
from app.core.model_loader import get_model_bundle
from app.services.prediction_service import BINARY_COLS

df = pd.read_csv("data/processed.csv")

try:
    bundle = get_model_bundle()
    df_encoded = df.copy()
    for col in BINARY_COLS:
        if col in df_encoded.columns and df_encoded[col].dtype == object:
            df_encoded[col] = df_encoded[col].replace({
                "Yes": 1, 
                "No": 0
            })
    df_encoded = df_encoded[bundle.feature_columns]
    predicted_probs = bundle.predict_proba_batch(df_encoded)
    df["PredictedChurn"] = predicted_probs >= bundle.chosen_threshold
except Exception as e:
    print(f"Warning: Failed to load model for dashboard predictions: {e}")
    df["PredictedChurn"] = (df["Churn"] == "Yes")

def data_info():
    Total_Customers = df.shape[0]
    Churn_Rate = round((df["Churn"] == "Yes").mean() * 100, 2)
    High_Risk_Customers = int(df["PredictedChurn"].sum())
    Average_Tenure = round(df["tenure"].mean(), 2)
    Average_Monthly_Charges = round(df["MonthlyCharges"].mean(), 2)
    Revenue_at_Risk = round(df.loc[df["PredictedChurn"], "MonthlyCharges"].sum(), 2)

    return KPIs(
        total_customers =  Total_Customers,
        churn_rate =  Churn_Rate,
        high_risk_customers =  High_Risk_Customers,
        average_tenure =  Average_Tenure,
        average_monthly_charges =  Average_Monthly_Charges,
        revenue_at_risk = Revenue_at_Risk
    )

def charts_info():
    churn_distribution = df['Churn'].value_counts().to_dict()
    contract_distribution = df['Contract'].value_counts().to_dict()
    customer_vs_churn = df.groupby("Contract")["Churn"].value_counts().unstack(fill_value=0).to_dict(orient="index")
    internet_vs_churn = df.groupby("InternetService")["Churn"].value_counts().unstack(fill_value=0).to_dict(orient="index")
    payment_vs_churn = df.groupby("PaymentMethod")["Churn"].value_counts().unstack(fill_value=0).to_dict(orient="index")
    tenure_bins = pd.cut(
                    df["tenure"],
                    bins=[0, 12, 24, 48, 72],
                    labels=["0-12", "13-24", "25-48", "49-72"],
                    include_lowest=True)
    tenure_distribution = tenure_bins.value_counts().sort_index().to_dict()
    monthly_charges = list(df['MonthlyCharges'])
    numeric_df = df.select_dtypes(include="number")
    correlation_matrix = (numeric_df.corr().round(2).to_dict())

    return Charts(
        churn_distribution =  churn_distribution,
        contract_distribution = contract_distribution,
        contract_vs_churn = customer_vs_churn,
        internet_vs_churn = internet_vs_churn,
        payment_vs_churn = payment_vs_churn,
        tenure_distribution = tenure_distribution,
        monthly_charges = monthly_charges,
        correlation_matrix = correlation_matrix
    )

def dashboard_data():
    return DashboardResponse(
        kpis = data_info(),
        charts = charts_info(),
        insights = [
                "Month-to-month customers have the highest churn rate.",
                "Customers with tenure below 12 months are more likely to churn.",
                "Electronic check is the most common payment method among churned customers.",
                "Fiber optic users show a higher churn percentage than DSL users."
            ]
    )