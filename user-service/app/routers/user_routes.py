from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.security import get_authenticated_user_id
from app.schemas.user_schema import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse
)
from app.services.user_service import (
    create_profile,
    get_profile,
    update_profile,
    delete_profile,
    deactivate_profile
)


router = APIRouter(
    prefix="/api/users/profile",
    tags=["User Profile"]
)


@router.post(
    "",
    response_model=UserProfileResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user_profile(
    data: UserProfileCreate,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return create_profile(auth_user_id, data, db)


@router.get("", response_model=UserProfileResponse)
def read_user_profile(
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return get_profile(auth_user_id, db)


@router.put("", response_model=UserProfileResponse)
def replace_user_profile(
    data: UserProfileCreate,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return update_profile(
        auth_user_id,
        UserProfileUpdate(**data.model_dump()),
        db
    )


@router.patch("", response_model=UserProfileResponse)
def partially_update_user_profile(
    data: UserProfileUpdate,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return update_profile(auth_user_id, data, db, partial=True)


@router.delete("")
def remove_user_profile(
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return delete_profile(auth_user_id, db)


@router.patch("/deactivate", response_model=UserProfileResponse)
def deactivate_user_profile(
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return deactivate_profile(auth_user_id, db)
