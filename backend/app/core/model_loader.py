import json
import logging

import joblib
import shap

from app.core.config import settings

logger = logging.getLogger("churn_api.model_loader")


class ModelBundle:
    """Holds every fitted object needed to score + explain a customer."""

    def __init__(self) -> None:
        logger.info("Loading calibrated model from %s", settings.calibrated_model_path)
        self.calibrated_model = joblib.load(settings.calibrated_model_path)

        logger.info("Loading metadata from %s", settings.metadata_path)
        with open(settings.metadata_path) as f:
            self.metadata: dict = json.load(f)

        logger.info("Loading raw xgb pipeline (for SHAP) from %s", settings.xgb_pipeline_path)
        best_xgb_pipeline = joblib.load(settings.xgb_pipeline_path)
        self.preprocessor = best_xgb_pipeline.named_steps["preprocessor"]
        self.xgb_model = best_xgb_pipeline.named_steps["model"]

        logger.info("Building SHAP TreeExplainer")
        self.explainer = shap.TreeExplainer(self.xgb_model)

        self.feature_columns: list[str] = self.metadata["feature_columns"]
        self.chosen_threshold: float = self.metadata["chosen_threshold"]

    def predict_proba(self, X_encoded):
        """Calibrated churn probability, same call as the notebook."""
        return self.calibrated_model.predict_proba(X_encoded)[:, 1][0]

    def predict_proba_batch(self, X_encoded):
        """Calibrated churn probability for a batch of customers."""
        return self.calibrated_model.predict_proba(X_encoded)[:, 1]

    def shap_values(self, X_encoded):
        transformed = self.preprocessor.transform(X_encoded)
        feature_names = self.preprocessor.get_feature_names_out()
        values = self.explainer.shap_values(transformed)[0]
        return feature_names, values

_bundle: ModelBundle | None = None


def get_model_bundle() -> ModelBundle:
    global _bundle
    if _bundle is None:
        _bundle = ModelBundle()
    return _bundle
