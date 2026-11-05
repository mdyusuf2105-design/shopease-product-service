from fastapi import FastAPI
from app.core.config import settings
from app.routers.auth_routes import router as auth_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="ShopEase Authentication Microservice with JWT and MySQL"
)

app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "service": "ShopEase Authentication Service",
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "authentication-service"}
