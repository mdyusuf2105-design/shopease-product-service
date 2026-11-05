from datetime import datetime
from uuid import UUID
from typing import Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)
    category: str = Field(..., min_length=1, max_length=50)
    status: Literal["Active", "Inactive"] = "Active"

    @field_validator("name", "category")
    @classmethod
    def validate_text(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty")
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        return value.strip() or None if value is not None else None

class ProductUpdate(ProductCreate):
    pass

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: UUID
    name: str
    description: str | None
    price: float
    stock_quantity: int
    category: str
    status: Literal["Active", "Inactive"]
    created_at: datetime
