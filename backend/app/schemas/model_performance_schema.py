from pydantic import BaseModel

class TestPerformance(BaseModel):
    accuracy: float
    macro_f1: float
    roc_auc: float
    precision: float
    recall: float

class ModelPerformanceResponse(BaseModel):
 
    model_type: str
    chosen_threshold: float
    target_recall_used_for_threshold: float
    test_performance: TestPerformance
    feature_columns: list[str]
    target_column: str
    saved_on: str