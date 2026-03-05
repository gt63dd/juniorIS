from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from dropguard.app import app
from dropguard.config import DropConfig
import dropguard.app as app_module


client = TestClient(app)


def _set_drop_started() -> None:
    app_module.DEFAULT_CONFIG = DropConfig(
        drop_start=datetime.now(timezone.utc) - timedelta(hours=1)
    )


def test_products_list_and_detail():
    _set_drop_started()
    response = client.get("/products")
    assert response.status_code == 200
    payload = response.json()
    assert "products" in payload
    assert len(payload["products"]) >= 1

    product_id = payload["products"][0]["product_id"]
    detail_response = client.get(f"/products/{product_id}")
    assert detail_response.status_code == 200
    assert detail_response.json()["product_id"] == product_id


def test_cart_add_update_remove_flow():
    _set_drop_started()

    cart_response = client.get("/cart")
    assert cart_response.status_code == 200
    session_cookie = cart_response.cookies.get("dropguard_session")
    assert session_cookie

    products_response = client.get("/products")
    product_id = products_response.json()["products"][0]["product_id"]

    add_response = client.post(
        "/cart/items",
        json={"product_id": product_id, "quantity": 2},
        cookies={"dropguard_session": session_cookie},
    )
    assert add_response.status_code == 200
    assert add_response.json()["items"][0]["quantity"] == 2

    update_response = client.patch(
        f"/cart/items/{product_id}",
        json={"product_id": product_id, "quantity": 3},
        cookies={"dropguard_session": session_cookie},
    )
    assert update_response.status_code == 200
    assert update_response.json()["items"][0]["quantity"] == 3

    remove_response = client.delete(
        f"/cart/items/{product_id}",
        cookies={"dropguard_session": session_cookie},
    )
    assert remove_response.status_code == 200
    assert remove_response.json()["items"] == []
