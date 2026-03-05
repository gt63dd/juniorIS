from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass(frozen=True)
class Product:
    product_id: str
    name: str
    description: str
    price_cents: int
    inventory: int


@dataclass
class CartItem:
    product_id: str
    quantity: int


@dataclass
class Cart:
    items: Dict[str, CartItem] = field(default_factory=dict)
    updated_at: datetime | None = None

    def to_list(self) -> List[CartItem]:
        return list(self.items.values())
