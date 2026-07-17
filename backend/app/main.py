import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings
from app.core.model_loader import get_model_bundle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("churn_api")

app = FastAPI(
    title=settings.app_name,
    version="1.0.0"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model artifacts once, at startup, so the first real request
    # isn't slowed down and a missing/corrupt artifact fails fast (crashes
    # on boot) rather than surfacing as a 500 later.
    logger.info("Warming up model bundle...")
    get_model_bundle()
    logger.info("Model bundle ready.")
    yield
    logger.info("Shutting down.")



app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.api_prefix, tags=["churn"])


@app.get("/")
def root():
    return {"service": settings.app_name, "docs": "/docs"}