from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.security import get_current_user, require_admin
from app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)
from app.services import category_service


router = APIRouter(
    prefix="/api/categories",
    tags=["Categories"],
)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    return category_service.create_category(db, category_data)


@router.get("/", response_model=list[CategoryResponse])
def list_categories(
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    is_admin = current_user["role"] == "admin"

    return category_service.list_categories(
        db,
        include_inactive=include_inactive if is_admin else False,
    )


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    category = category_service.get_category(db, category_id)

    if not category.is_active and current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def replace_category(
    category_id: int,
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    update_data = CategoryUpdate(**category_data.model_dump())

    return category_service.update_category(
        db,
        category_id,
        update_data,
    )


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    return category_service.update_category(
        db,
        category_id,
        category_data,
    )


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    category_service.delete_category(db, category_id)

    return {
        "message": "Category deleted successfully.",
        "category_id": category_id,
    }
