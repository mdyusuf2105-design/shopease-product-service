from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.security import require_admin
from app.schemas.inventory_schema import (
    StockChange,
    InventoryResponse,
    InventoryTransactionResponse,
)
from app.services import inventory_service


router = APIRouter(
    prefix="/api/inventory",
    tags=["Inventory"],
)


@router.get("/low-stock")
def get_low_stock_products(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    return inventory_service.low_stock_products(db)


@router.get("/{product_id}", response_model=InventoryResponse)
def get_inventory(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    return inventory_service.get_inventory(db, product_id)


@router.post(
    "/stock-in/{product_id}",
    response_model=InventoryTransactionResponse,
)
def stock_in(
    product_id: int,
    stock_data: StockChange,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    return inventory_service.stock_in(
        db,
        product_id,
        stock_data,
    )


@router.post(
    "/stock-out/{product_id}",
    response_model=InventoryTransactionResponse,
)
def stock_out(
    product_id: int,
    stock_data: StockChange,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    return inventory_service.stock_out(
        db,
        product_id,
        stock_data,
    )


@router.get(
    "/{product_id}/history",
    response_model=list[InventoryTransactionResponse],
)
def get_inventory_history(
    product_id: int,
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    return inventory_service.inventory_history(
        db,
        product_id,
        limit,
    )
