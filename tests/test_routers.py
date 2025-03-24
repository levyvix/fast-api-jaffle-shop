from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI Jaffle Shop!"}


def test_customers_router():
    # simple collection test
    response = client.get("/customers")
    assert response.status_code == 200
    assert len(response.json()) == 100

    # simple item test
    first_item = response.json()[0]
    response = client.get(f"/customers/{first_item['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == first_item["id"]


def test_items_router():
    # simple collection test
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 100

    # simple item test
    first_item = response.json()[0]
    response = client.get(f"/items/{first_item['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == first_item["id"]


def test_products_router():
    # simple collection test
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 10

    # simple item test
    first_item = response.json()[0]
    response = client.get(f"/products/{first_item['sku']}")
    assert response.status_code == 200
    assert response.json()["sku"] == first_item["sku"]


def test_orders_router():
    # simple collection test
    response = client.get("/orders")
    assert response.status_code == 200
    assert len(response.json()) == 100

    # simple item test
    first_item = response.json()[0]
    response = client.get(f"/orders/{first_item['id']}")


def test_stores_router():
    # simple collection test
    response = client.get("/stores")
    assert response.status_code == 200
    assert len(response.json()) == 6

    # simple item test
    first_item = response.json()[0]
    response = client.get(f"/stores/{first_item['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == first_item["id"]


def test_supplies_router():
    # simple collection test
    response = client.get("/supplies")
    assert response.status_code == 200
    assert len(response.json()) == 65

    # simple item test
    first_item = response.json()[0]
    response = client.get(f"/supplies/{first_item['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == first_item["id"]
