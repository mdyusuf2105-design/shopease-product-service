from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user_model import UserProfile
from app.models.address_model import UserAddress
from app.schemas.address_schema import AddressCreate, AddressUpdate


def get_owner_profile(auth_user_id: int, db: Session):
    profile = db.query(UserProfile).filter(
        UserProfile.auth_user_id == auth_user_id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Create your user profile before managing addresses"
        )

    if not profile.is_active:
        raise HTTPException(
            status_code=403,
            detail="User profile is inactive"
        )

    return profile


def get_owned_address(address_id: int, profile_id: int, db: Session):
    address = db.query(UserAddress).filter(
        UserAddress.id == address_id,
        UserAddress.user_id == profile_id
    ).first()

    if not address:
        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    return address


def clear_default_addresses(profile_id: int, db: Session):
    db.query(UserAddress).filter(
        UserAddress.user_id == profile_id,
        UserAddress.is_default.is_(True)
    ).update(
        {"is_default": False},
        synchronize_session=False
    )


def create_address(auth_user_id: int, data: AddressCreate, db: Session):
    profile = get_owner_profile(auth_user_id, db)

    values = data.model_dump()

    if values["is_default"]:
        clear_default_addresses(profile.id, db)

    address = UserAddress(
        user_id=profile.id,
        **values
    )

    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def list_addresses(auth_user_id: int, db: Session):
    profile = get_owner_profile(auth_user_id, db)

    return db.query(UserAddress).filter(
        UserAddress.user_id == profile.id
    ).order_by(UserAddress.created_at.desc()).all()


def get_address(auth_user_id: int, address_id: int, db: Session):
    profile = get_owner_profile(auth_user_id, db)
    return get_owned_address(address_id, profile.id, db)


def update_address(
    auth_user_id: int,
    address_id: int,
    data: AddressUpdate,
    db: Session
):
    profile = get_owner_profile(auth_user_id, db)
    address = get_owned_address(address_id, profile.id, db)

    updates = data.model_dump(exclude_unset=True)

    if updates.get("is_default") is True:
        clear_default_addresses(profile.id, db)

    for field, value in updates.items():
        setattr(address, field, value)

    db.commit()
    db.refresh(address)
    return address


def delete_address(auth_user_id: int, address_id: int, db: Session):
    profile = get_owner_profile(auth_user_id, db)
    address = get_owned_address(address_id, profile.id, db)

    db.delete(address)
    db.commit()

    return {"message": "Address deleted successfully"}


def set_default_address(auth_user_id: int, address_id: int, db: Session):
    profile = get_owner_profile(auth_user_id, db)
    address = get_owned_address(address_id, profile.id, db)

    clear_default_addresses(profile.id, db)
    address.is_default = True

    db.commit()
    db.refresh(address)
    return address
