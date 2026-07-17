from pydantic import BaseModel
from typing import Literal

class RiskFactor(BaseModel):
    feature: str
    label: str
    shap_value: float
    suggestion: str | None = None

class ChurnPredictionResponse(BaseModel):

    prediction: Literal["Will Churn", "Will Stay"]
    churn_probability: float
    risk_level: Literal["Very Low", "Low", "Moderate", "High", "Critical"]
    priority_action: str

    top_risk_factors: list[RiskFactor]
    top_protective_factors: list[RiskFactor]

    business_interpretation: str
    recommended_actions: list[str]