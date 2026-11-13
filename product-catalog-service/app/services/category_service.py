from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.category_model import Category
from app.models.product_model import Product
from app.schemas.category_schema import CategoryCreate, CategoryUpdate


def create_category(data: CategoryCreate, db: Session):
    category = Category(**data.model_dump())
    db.add(category)

    try:
        db.commit()
        db.refresh(category)
        return category
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category name already exists",
        )


def list_categories(db: Session, include_inactive: bool = False):
    query = db.query(Category)

    if not include_inactive:
        query = query.filter(Category.is_active.is_(True))

    return query.order_by(Category.name.asc()).all()


def get_category(category_id: int, db: Session):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


def update_category(category_id: int, data: CategoryUpdate, db: Session):
    category = get_category(category_id, db)

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    try:
        db.commit()
        db.refresh(category)
        return category
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Category name already exists",
        )


def delete_category(category_id: int, db: Session):
    category = get_category(category_id, db)

    product_exists = (
        db.query(Product.id)
        .filter(Product.category_id == category_id)
        .first()
    )

    if product_exists:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a category containing products. Reassign or remove its products first.",
        )

    db.delete(category)
    db.commit()

    return {"message": "Category deleted successfully"}
