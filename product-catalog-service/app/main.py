from fastapi import FastAPI

from app.core.config import settings

from app.routers.product_routes import router as product_router
from app.routers.category_routes import router as category_router
from app.routers.inventory_routes import router as inventory_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "ShopEase Product Catalog Microservice for product, category "
        "and inventory management with JWT role-based authorization."
    ),
)

app.include_router(product_router)
app.include_router(category_router)
app.include_router(inventory_router)


@app.get("/", tags=["General"])
def home():
    return {
        "service": "ShopEase Product Catalog Service",
        "status": "running",
        "version": settings.APP_VERSION,
    }


@app.get("/health", tags=["General"])
def health():
    return {
        "status": "healthy",
        "service": "product-catalog-service",
    }
