from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user_model import UserProfile
from app.schemas.user_schema import UserProfileCreate, UserProfileUpdate


def create_profile(auth_user_id: int, data: UserProfileCreate, db: Session):
    existing = db.query(UserProfile).filter(
        UserProfile.auth_user_id == auth_user_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="User profile already exists"
        )

    profile = UserProfile(
        auth_user_id=auth_user_id,
        **data.model_dump()
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def get_profile(auth_user_id: int, db: Session):
    profile = db.query(UserProfile).filter(
        UserProfile.auth_user_id == auth_user_id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    return profile


def update_profile(
    auth_user_id: int,
    data: UserProfileUpdate,
    db: Session,
    partial: bool = False
):
    profile = get_profile(auth_user_id, db)

    updates = data.model_dump(exclude_unset=True)

    if partial and not updates:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    for field, value in updates.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile


def delete_profile(auth_user_id: int, db: Session):
    profile = get_profile(auth_user_id, db)

    db.delete(profile)
    db.commit()

    return {"message": "User profile deleted successfully"}


def deactivate_profile(auth_user_id: int, db: Session):
    profile = get_profile(auth_user_id, db)

    profile.is_active = False
    db.commit()
    db.refresh(profile)

    return profile
