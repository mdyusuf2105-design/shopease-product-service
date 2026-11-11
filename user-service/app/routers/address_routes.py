from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.security import get_authenticated_user_id
from app.schemas.address_schema import (
    AddressCreate,
    AddressUpdate,
    AddressResponse
)
from app.services.address_service import (
    create_address,
    list_addresses,
    get_address,
    update_address,
    delete_address,
    set_default_address
)


router = APIRouter(
    prefix="/api/users/addresses",
    tags=["User Addresses"]
)


@router.post(
    "",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED
)
def add_address(
    data: AddressCreate,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return create_address(auth_user_id, data, db)


@router.get("", response_model=list[AddressResponse])
def get_all_addresses(
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return list_addresses(auth_user_id, db)


@router.get("/{address_id}", response_model=AddressResponse)
def get_single_address(
    address_id: int,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return get_address(auth_user_id, address_id, db)


@router.put("/{address_id}", response_model=AddressResponse)
def replace_address(
    address_id: int,
    data: AddressCreate,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return update_address(
        auth_user_id,
        address_id,
        AddressUpdate(**data.model_dump()),
        db
    )


@router.delete("/{address_id}")
def remove_address(
    address_id: int,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return delete_address(auth_user_id, address_id, db)


@router.patch("/{address_id}/default", response_model=AddressResponse)
def make_default_address(
    address_id: int,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return set_default_address(auth_user_id, address_id, db)


@router.patch("/{address_id}", response_model=AddressResponse)
def partially_update_address(
    address_id: int,
    data: AddressUpdate,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return update_address(auth_user_id, address_id, data, db)
