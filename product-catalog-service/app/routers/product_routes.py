from decimal import Decimal
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.security import get_current_user, require_admin
from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
)
from app.services import product_service


router = APIRouter(
    prefix="/api/products",
    tags=["Products"],
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    return product_service.create_product(db, product_data)


@router.get("/", response_model=ProductListResponse)
def list_products(
    search: str | None = None,
    category_id: int | None = Query(default=None, gt=0),
    min_price: Decimal | None = Query(default=None, ge=0),
    max_price: Decimal | None = Query(default=None, ge=0),
    available: bool | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    sort_by: Literal[
        "name", "price", "created_at", "stock_quantity"
    ] = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if min_price is not None and max_price is not None:
        if min_price > max_price:
            raise HTTPException(
                status_code=422,
                detail="Minimum price cannot exceed maximum price.",
            )

    return product_service.list_products(
        db=db,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        available=available,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
        user_role=current_user["role"],
    )


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return product_service.get_product(
        db,
        product_id,
        current_user["role"],
    )


@router.put("/{product_id}", response_model=ProductResponse)
def replace_product(
    product_id: int,
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    update_data = ProductUpdate(**product_data.model_dump())

    return product_service.update_product(
        db,
        product_id,
        update_data,
    )


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    return product_service.update_product(
        db,
        product_id,
        product_data,
    )


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    product_service.delete_product(db, product_id)

    return {
        "message": "Product deactivated successfully.",
        "product_id": product_id,
    }
