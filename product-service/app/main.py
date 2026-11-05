from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.config.settings import settings
from app.routers.product_routes import router as product_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="ShopEase Product Management Microservice"
)

app.include_router(product_router)

@app.get("/", tags=["General"])
def home():
    return {
        "message": "Welcome to ShopEase Product Service",
        "version": settings.APP_VERSION,
        "documentation": "/docs"
    }

@app.get("/health", tags=["General"])
def health():
    return {"status": "healthy", "service": "product-service"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Unexpected internal server error"
        }
    )
