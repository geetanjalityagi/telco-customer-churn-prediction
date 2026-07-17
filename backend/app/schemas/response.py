from pydantic import BaseModel, Field
from typing import List

class RiskFactor(BaseModel):
    feature: str
    label: str
    shap_value: float
    suggestion: str | None = None

class ChurnPredictionResponse(BaseModel):
    """
    Field-for-field JSON equivalent of the printed report produced by
    `explain_prediction()` in 03_Customer_Churn_Prediction.ipynb.
    """

    prediction: Literal["Will Churn", "Will Stay"]
    churn_probability: float
    risk_level: Literal["Very Low", "Low", "Moderate", "High", "Critical"]
    priority_action: str

    top_risk_factors: list[RiskFactor]
    top_protective_factors: list[RiskFactor]

    business_interpretation: str
    recommended_actions: list[str]