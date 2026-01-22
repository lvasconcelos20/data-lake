from fastapi import APIRouter

from app.api.v1.routers import health, refueling

api_router = APIRouter()
api_router.include_router(refueling.router, tags=["abastecimentos"])
api_router.include_router(health.router, tags=["health"])
