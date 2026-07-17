import logging

from fastapi import APIRouter, HTTPException

from app.core.model_loader import get_model_bundle
from app.schemas.request import CustomerInput
from app.schemas.response import ChurnPredictionResponse, RiskFactor
from app.services.prediction_service import explain_prediction

logger = logging.getLogger("churn_api.routes")
router = APIRouter()


@router.get("/health")
def health():
    bundle = get_model_bundle()
    return {
        "status": "ok",
        "model_type": bundle.metadata.get("model_type"),
        "chosen_threshold": bundle.chosen_threshold,
        "test_performance": bundle.metadata.get("test_performance"),
    }


@router.post("/predict", response_model=ChurnPredictionResponse)
def predict(customer: CustomerInput):
    try:
        bundle = get_model_bundle()
        return explain_prediction(customer, bundle)
    except Exception:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Prediction failed. Check server logs.")
