from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ARTIFACT_DIR = BASE_DIR / "models_artifacts"


class Settings(BaseSettings):
    app_name: str = "Customer Churn Prediction API"
    api_prefix: str = "/api/v1"

    calibrated_model_path: Path = ARTIFACT_DIR / "churn_model_xgb_calibrated.pkl"
    xgb_pipeline_path: Path = ARTIFACT_DIR / "xgb_pipeline.pkl"
    metadata_path: Path = ARTIFACT_DIR / "churn_model_metadata.json"

    allowed_origins: list[str] = ["*"]

    class Config:
        env_prefix = "CHURN_" 


settings = Settings()
