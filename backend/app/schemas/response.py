from pydantic import BaseModel
from typing import Literal

class TestPerformance(BaseModel):
    accuracy: float
    macro_f1: float
    roc_auc: float

class ModelPerformanceResponse(BaseModel):
 
    model_type: str
    chosen_threshold: float
    target_recall_used_for_threshold: float
    test_performance: TestPerformance
    feature_columns: list[str]
    target_column: str
    saved_on: str

class RiskFactor(BaseModel):
    feature: str
    label: str
    shap_value: float
    suggestion: str | None = None

class ChurnPredictionResponse(BaseModel):

    prediction: Literal["Will Churn", "Will Stay"]
    churn_probability: float
    risk_level: Literal["Very Low", "Low", "Moderate", "High", "Critical"]
    risk_emoji: str
    priority_stars: str
    priority_action: str

    top_risk_factors: list[RiskFactor]
    top_protective_factors: list[RiskFactor]

    business_interpretation: str
    recommended_actions: list[str]

class BatchChurnPredictionResponse(BaseModel):
    total_customers: int
    predicted_churn_count: int
    churn_rate: float
    predictions: list[ChurnPredictionResponse]