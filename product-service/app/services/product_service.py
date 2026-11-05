from datetime import datetime, timezone
from uuid import UUID, uuid4
from fastapi import HTTPException
from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate

products: dict[str, Product] = {}

def validate_id(product_id: str) -> str:
    try:
        return str(UUID(product_id))
    except (ValueError, TypeError, AttributeError):
        raise HTTPException(status_code=400, detail="Invalid product ID")

def create_product(data: ProductCreate):
    product_id = str(uuid4())
    product = Product(
        product_id=UUID(product_id),
        name=data.name,
        description=data.description,
        price=data.price,
        stock_quantity=data.stock_quantity,
        category=data.category,
        status=data.status,
        created_at=datetime.now(timezone.utc)
    )
    products[product_id] = product
    return product

def get_all_products(category=None, skip=0, limit=10):
    result = list(products.values())
    if category:
        result = [p for p in result if p.category.lower() == category.strip().lower()]
    return result[skip:skip + limit]

def get_product(product_id: str):
    product_id = validate_id(product_id)
    product = products.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def update_product(product_id: str, data: ProductUpdate):
    product_id = validate_id(product_id)
    existing = get_product(product_id)

    updated = Product(
        product_id=existing.product_id,
        name=data.name,
        description=data.description,
        price=data.price,
        stock_quantity=data.stock_quantity,
        category=data.category,
        status=data.status,
        created_at=existing.created_at
    )
    products[product_id] = updated
    return updated

def delete_product(product_id: str):
    product_id = validate_id(product_id)
    get_product(product_id)
    del products[product_id]
