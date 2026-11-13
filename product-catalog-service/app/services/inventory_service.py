from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.inventory_model import InventoryTransaction
from app.models.product_model import Product
from app.schemas.inventory_schema import StockChange


def get_inventory(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "product_id": product.id,
        "stock_quantity": product.stock_quantity,
    }


def change_stock(
    product_id: int,
    data: StockChange,
    transaction_type: str,
    db: Session
):
    try:
        product = (
            db.query(Product)
            .filter(Product.id == product_id)
            .with_for_update()
            .first()
        )

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        previous_stock = product.stock_quantity

        if transaction_type == "IN":
            updated_stock = previous_stock + data.quantity
        else:
            if data.quantity > previous_stock:
                raise HTTPException(
                    status_code=409,
                    detail="Insufficient stock. Stock cannot become negative."
                )
            updated_stock = previous_stock - data.quantity

        product.stock_quantity = updated_stock

        transaction = InventoryTransaction(
            product_id=product_id,
            transaction_type=transaction_type,
            quantity=data.quantity,
            previous_stock=previous_stock,
            updated_stock=updated_stock,
            remarks=data.remarks,
        )

        db.add(transaction)
        db.commit()
        db.refresh(product)
        db.refresh(transaction)

        return transaction

    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise


def stock_in(product_id: int, data: StockChange, db: Session):
    return change_stock(product_id, data, "IN", db)


def stock_out(product_id: int, data: StockChange, db: Session):
    return change_stock(product_id, data, "OUT", db)


def inventory_history(product_id: int, db: Session):
    product = db.query(Product.id).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return (
        db.query(InventoryTransaction)
        .filter(InventoryTransaction.product_id == product_id)
        .order_by(InventoryTransaction.created_at.desc())
        .all()
    )


def low_stock_products(db: Session):
    return (
        db.query(Product)
        .filter(
            Product.is_active.is_(True),
            Product.stock_quantity <= settings.LOW_STOCK_THRESHOLD
        )
        .order_by(Product.stock_quantity.asc())
        .all()
    )
