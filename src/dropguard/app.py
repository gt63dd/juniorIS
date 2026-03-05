from __future__ import annotations

from datetime import datetime, timezone

from fastapi import Cookie, FastAPI, HTTPException, Response

from .config import DEFAULT_CONFIG
from .inventory import get_product, list_products
from .models import CartItem
from .schemas import (
    CartItemRequest,
    CartItemResponse,
    CartResponse,
    ProductListResponse,
    ProductResponse,
)
from .session import SESSION_COOKIE_NAME, SessionStore

app = FastAPI(title="DropGuard Lite")
store = SessionStore()


def _ensure_drop_started() -> None:
    now = datetime.now(timezone.utc)
    if now < DEFAULT_CONFIG.drop_start:
        raise HTTPException(
            status_code=403,
            detail="Drop has not started yet.",
        )


@app.get("/products", response_model=ProductListResponse)
async def products() -> ProductListResponse:
    _ensure_drop_started()
    product_payload = [ProductResponse(**product.__dict__) for product in list_products()]
    return ProductListResponse(drop_start=DEFAULT_CONFIG.drop_start, products=product_payload)


@app.get("/products/{product_id}", response_model=ProductResponse)
async def product_detail(product_id: str) -> ProductResponse:
    _ensure_drop_started()
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(**product.__dict__)


@app.get("/cart", response_model=CartResponse)
async def get_cart(response: Response, session_id: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME)) -> CartResponse:
    session_key = store.get_or_create_session(session_id)
    cart = store.get_cart(session_key)
    store.update_cart_timestamp(session_key)
    response.set_cookie(key=SESSION_COOKIE_NAME, value=session_key, httponly=True, samesite="lax")
    return CartResponse(
        session_id=session_key,
        updated_at=cart.updated_at or datetime.now(timezone.utc),
        items=[CartItemResponse(**item.__dict__) for item in cart.to_list()],
    )


@app.post("/cart/items", response_model=CartResponse)
async def add_cart_item(
    item: CartItemRequest,
    response: Response,
    session_id: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
) -> CartResponse:
    _ensure_drop_started()
    product = get_product(item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.inventory <= 0:
        raise HTTPException(status_code=409, detail="Product out of stock")

    session_key = store.get_or_create_session(session_id)
    cart = store.get_cart(session_key)
    cart.items[item.product_id] = CartItem(product_id=item.product_id, quantity=item.quantity)
    store.update_cart_timestamp(session_key)
    response.set_cookie(key=SESSION_COOKIE_NAME, value=session_key, httponly=True, samesite="lax")

    return CartResponse(
        session_id=session_key,
        updated_at=cart.updated_at or datetime.now(timezone.utc),
        items=[CartItemResponse(**cart_item.__dict__) for cart_item in cart.to_list()],
    )


@app.patch("/cart/items/{product_id}", response_model=CartResponse)
async def update_cart_item(
    product_id: str,
    item: CartItemRequest,
    response: Response,
    session_id: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
) -> CartResponse:
    _ensure_drop_started()
    if product_id != item.product_id:
        raise HTTPException(status_code=400, detail="Product mismatch")
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    session_key = store.get_or_create_session(session_id)
    cart = store.get_cart(session_key)
    if product_id not in cart.items:
        raise HTTPException(status_code=404, detail="Item not in cart")
    cart.items[product_id].quantity = item.quantity
    store.update_cart_timestamp(session_key)
    response.set_cookie(key=SESSION_COOKIE_NAME, value=session_key, httponly=True, samesite="lax")

    return CartResponse(
        session_id=session_key,
        updated_at=cart.updated_at or datetime.now(timezone.utc),
        items=[CartItemResponse(**cart_item.__dict__) for cart_item in cart.to_list()],
    )


@app.delete("/cart/items/{product_id}", response_model=CartResponse)
async def remove_cart_item(
    product_id: str,
    response: Response,
    session_id: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
) -> CartResponse:
    _ensure_drop_started()
    session_key = store.get_or_create_session(session_id)
    cart = store.get_cart(session_key)
    if product_id not in cart.items:
        raise HTTPException(status_code=404, detail="Item not in cart")
    del cart.items[product_id]
    store.update_cart_timestamp(session_key)
    response.set_cookie(key=SESSION_COOKIE_NAME, value=session_key, httponly=True, samesite="lax")

    return CartResponse(
        session_id=session_key,
        updated_at=cart.updated_at or datetime.now(timezone.utc),
        items=[CartItemResponse(**cart_item.__dict__) for cart_item in cart.to_list()],
    )
