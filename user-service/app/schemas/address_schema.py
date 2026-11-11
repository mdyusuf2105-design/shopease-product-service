import re

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class AddressCreate(BaseModel):
    address_type: str = Field(default="Home", max_length=30)
    full_name: str = Field(min_length=2, max_length=150)
    phone_number: str = Field(min_length=7, max_length=20)
    address_line_1: str = Field(min_length=3, max_length=255)
    address_line_2: str | None = Field(default=None, max_length=255)
    city: str = Field(min_length=2, max_length=100)
    state: str = Field(min_length=2, max_length=100)
    country: str = Field(min_length=2, max_length=100)
    postal_code: str = Field(min_length=3, max_length=20)
    is_default: bool = False

    @field_validator("address_type")
    @classmethod
    def validate_address_type(cls, value):
        if value not in ["Home", "Office", "Other"]:
            raise ValueError("Address type must be Home, Office or Other")
        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, value):
        if not re.fullmatch(r"\+?[0-9]{7,15}", value.strip()):
            raise ValueError("Invalid phone number")
        return value.strip()


class AddressUpdate(BaseModel):
    address_type: str | None = Field(default=None, max_length=30)
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    phone_number: str | None = Field(default=None, max_length=20)
    address_line_1: str | None = Field(default=None, max_length=255)
    address_line_2: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    country: str | None = Field(default=None, max_length=100)
    postal_code: str | None = Field(default=None, max_length=20)
    is_default: bool | None = None

    @field_validator("address_type")
    @classmethod
    def validate_address_type(cls, value):
        if value is not None and value not in ["Home", "Office", "Other"]:
            raise ValueError("Address type must be Home, Office or Other")
        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, value):
        if value is not None and not re.fullmatch(
            r"\+?[0-9]{7,15}", value.strip()
        ):
            raise ValueError("Invalid phone number")
        return value.strip() if value is not None else value


class AddressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    address_type: str
    full_name: str
    phone_number: str
    address_line_1: str
    address_line_2: str | None
    city: str
    state: str
    country: str
    postal_code: str
    is_default: bool
    created_at: datetime
