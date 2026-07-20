from typing import Dict, List
from pydantic import BaseModel

class KPIs(BaseModel):
    total_customers: int
    churn_rate: float
    high_risk_customers: int
    average_tenure: float
    average_monthly_charges: float
    revenue_at_risk: float


class Charts(BaseModel):
    churn_distribution: Dict[str, int]
    contract_distribution: Dict[str, int]
    contract_vs_churn: Dict[str, Dict[str, int]]
    internet_vs_churn: Dict[str, Dict[str, int]]
    payment_vs_churn: Dict[str, Dict[str, int]]
    tenure_distribution: Dict[str, List[int]]
    monthly_charges: List[float]
    correlation_matrix: Dict[str, Dict[str, float]]

class DashboardResponse(BaseModel):
    kpis: KPIs
    charts: Charts
    insights: List[str]