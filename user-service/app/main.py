from fastapi import FastAPI

from app.core.config import settings
from app.routers.user_routes import router as user_router
from app.routers.address_routes import router as address_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "ShopEase User Management Microservice "
        "with JWT authentication, user profiles and addresses."
    )
)

app.include_router(user_router)
app.include_router(address_router)


@app.get("/")
def home():
    return {
        "service": "ShopEase User Management Service",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "user-management-service"
    }
