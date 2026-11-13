from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ProductCreate(BaseModel):
    category_id: int = Field(gt=0)
    name: str = Field(min_length=2, max_length=150)
    description: str | None = None
    sku: str = Field(min_length=2, max_length=64)
    price: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    discount_price: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    stock_quantity: int = Field(default=0, ge=0)
    image_url: str | None = Field(default=None, max_length=500)
    brand: str | None = Field(default=None, max_length=100)
    is_active: bool = True

    @field_validator("name", "sku")
    @classmethod
    def clean_text(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty")
        return value

    @model_validator(mode="after")
    def validate_discount(self):
        if self.discount_price is not None and self.discount_price > self.price:
            raise ValueError("Discount price cannot exceed regular price")
        return self


class ProductUpdate(BaseModel):
    category_id: int | None = Field(default=None, gt=0)
    name: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    sku: str | None = Field(default=None, min_length=2, max_length=64)
    price: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    discount_price: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    stock_quantity: int | None = Field(default=None, ge=0)
    image_url: str | None = Field(default=None, max_length=500)
    brand: str | None = Field(default=None, max_length=100)
    is_active: bool | None = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    name: str
    description: str | None
    sku: str
    price: Decimal
    discount_price: Decimal | None
    stock_quantity: int
    image_url: str | None
    brand: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
