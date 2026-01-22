from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title="Transport Backend Challenge",
    description="API Gateway for Transport Data Lake",
    version="1.0.0",
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "app_name": settings.PROJECT_NAME}


@app.get("/")
async def root():
    return {"message": "Welcome to Transport Backend Challenge API"}


from app.api.v1.api import api_router

app.include_router(api_router, prefix="/api/v1")
