from __future__ import annotations

import secrets
from datetime import datetime, timezone
from typing import Dict

from .models import Cart


SESSION_COOKIE_NAME = "dropguard_session"


class SessionStore:
    def __init__(self) -> None:
        self._carts: Dict[str, Cart] = {}

    def get_or_create_session(self, session_id: str | None) -> str:
        if session_id and session_id in self._carts:
            return session_id
        new_session_id = secrets.token_urlsafe(16)
        self._carts[new_session_id] = Cart(updated_at=datetime.now(timezone.utc))
        return new_session_id

    def get_cart(self, session_id: str) -> Cart:
        return self._carts.setdefault(
            session_id,
            Cart(updated_at=datetime.now(timezone.utc)),
        )

    def update_cart_timestamp(self, session_id: str) -> None:
        cart = self._carts.get(session_id)
        if cart:
            cart.updated_at = datetime.now(timezone.utc)
