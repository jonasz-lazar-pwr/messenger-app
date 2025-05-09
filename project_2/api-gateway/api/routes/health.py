# api/routes/health.py

from fastapi import APIRouter

router = APIRouter()

# Healthz endpoint (no auth)
@router.get(
    "/",
    summary="Health check",
    description="Basic health check endpoint",
    tags=["Health"]
)
def health_check():
    return {"status": "ok"}
