from typing import Annotated
from fastapi import APIRouter, Query, Response, status
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.services import product_service

router = APIRouter(prefix="/api/products", tags=["Product Management"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    return product_service.create_product(product)

@router.get("/", response_model=list[ProductResponse])
def get_products(
    category: Annotated[str | None, Query(min_length=1, max_length=50)] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10
):
    return product_service.get_all_products(category, skip, limit)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str):
    return product_service.get_product(product_id)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: str, product: ProductUpdate):
    return product_service.update_product(product_id, product)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str):
    product_service.delete_product(product_id)
    return Response(status_code=204)
