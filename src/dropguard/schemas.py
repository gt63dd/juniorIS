from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class ProductResponse(BaseModel):
    product_id: str
    name: str
    description: str
    price_cents: int
    inventory: int


class ProductListResponse(BaseModel):
    drop_start: datetime
    products: List[ProductResponse]


class CartItemRequest(BaseModel):
    product_id: str
    quantity: int = Field(..., ge=1, le=10)


class CartItemResponse(BaseModel):
    product_id: str
    quantity: int


class CartResponse(BaseModel):
    session_id: str
    updated_at: datetime
    items: List[CartItemResponse]
