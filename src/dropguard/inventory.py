from __future__ import annotations

from dataclasses import replace
from typing import Dict, List

from .models import Product


DEFAULT_PRODUCTS: Dict[str, Product] = {
    "drop-001": Product(
        product_id="drop-001",
        name="DropGuard Hoodie",
        description="Limited run heavyweight hoodie.",
        price_cents=8500,
        inventory=48,
    ),
    "drop-002": Product(
        product_id="drop-002",
        name="DropGuard Tee",
        description="Relaxed fit tee with embroidered logo.",
        price_cents=4200,
        inventory=120,
    ),
    "drop-003": Product(
        product_id="drop-003",
        name="DropGuard Cap",
        description="Structured cap with tonal branding.",
        price_cents=3200,
        inventory=75,
    ),
}


def list_products() -> List[Product]:
    return list(DEFAULT_PRODUCTS.values())


def get_product(product_id: str) -> Product | None:
    return DEFAULT_PRODUCTS.get(product_id)


def update_inventory(product_id: str, new_inventory: int) -> Product | None:
    product = DEFAULT_PRODUCTS.get(product_id)
    if not product:
        return None
    updated = replace(product, inventory=new_inventory)
    DEFAULT_PRODUCTS[product_id] = updated
    return updated
