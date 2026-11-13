from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.category_model import Category
from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate


def create_product(data: ProductCreate, db: Session):
    category = db.query(Category).filter(
        Category.id == data.category_id,
        Category.is_active.is_(True)
    ).first()

    if not category:
        raise HTTPException(status_code=400, detail="Active category not found")

    product = Product(**data.model_dump())
    db.add(product)

    try:
        db.commit()
        db.refresh(product)
        return product
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Product SKU already exists")


def list_products(
    db: Session,
    user_role: str,
    search: str | None = None,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    available: bool | None = None,
    page: int = 1,
    page_size: int = 10,
    sort_by: str = "created_at",
    sort_order: str = "desc",
):
    query = db.query(Product).join(Category)

    if user_role != "admin":
        query = query.filter(
            Product.is_active.is_(True),
            Category.is_active.is_(True)
        )

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Product.name.ilike(term),
                Product.sku.ilike(term)
            )
        )

    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if available is True:
        query = query.filter(Product.stock_quantity > 0)
    elif available is False:
        query = query.filter(Product.stock_quantity == 0)

    allowed_sort_fields = {
        "name": Product.name,
        "price": Product.price,
        "created_at": Product.created_at,
        "stock_quantity": Product.stock_quantity,
    }

    sort_column = allowed_sort_fields.get(sort_by)

    if sort_column is None:
        raise HTTPException(status_code=422, detail="Invalid sort_by field")

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


def get_product(product_id: int, user_role: str, db: Session):
    query = db.query(Product).join(Category).filter(Product.id == product_id)

    if user_role != "admin":
        query = query.filter(
            Product.is_active.is_(True),
            Category.is_active.is_(True)
        )

    product = query.first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


def update_product(product_id: int, data: ProductUpdate, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    updates = data.model_dump(exclude_unset=True)

    if "category_id" in updates:
        category = db.query(Category).filter(
            Category.id == updates["category_id"],
            Category.is_active.is_(True)
        ).first()

        if not category:
            raise HTTPException(status_code=400, detail="Active category not found")

    new_price = updates.get("price", product.price)
    new_discount = updates.get("discount_price", product.discount_price)

    if new_discount is not None and new_discount > new_price:
        raise HTTPException(
            status_code=422,
            detail="Discount price cannot exceed regular price"
        )

    for key, value in updates.items():
        setattr(product, key, value)

    try:
        db.commit()
        db.refresh(product)
        return product
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Product SKU already exists")


def delete_product(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.is_active = False
    db.commit()

    return {"message": "Product deactivated successfully"}
