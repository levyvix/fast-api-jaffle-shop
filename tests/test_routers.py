import pytest

from fastapi.testclient import TestClient
from app.main import app
from app.const import API_V1_PREFIX, DEFAULT_PAGE_SIZE

from tests.utils import EXPECTED_TABLES_COUNTS_ALL, PRIMARY_KEYS

client = TestClient(app)


def test_customers_router():
    # simple collection test
    response = client.get(API_V1_PREFIX + "/customers")
    assert response.status_code == 200
    assert len(response.json()) == 100

    # simple item test
    first_item = response.json()[0]
    response = client.get(API_V1_PREFIX + f"/customers/{first_item['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == first_item["id"]


def test_items_router():
    # simple collection test
    response = client.get(API_V1_PREFIX + "/items")
    assert response.status_code == 200
    assert len(response.json()) == 100

    # simple item test
    first_item = response.json()[0]
    response = client.get(API_V1_PREFIX + f"/items/{first_item['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == first_item["id"]


def test_products_router():
    # simple collection test
    response = client.get(API_V1_PREFIX + "/products")
    assert response.status_code == 200
    assert len(response.json()) == 10

    # simple item test
    first_item = response.json()[0]
    response = client.get(API_V1_PREFIX + f"/products/{first_item['sku']}")
    assert response.status_code == 200
    assert response.json()["sku"] == first_item["sku"]


def test_orders_router():
    # simple collection test
    response = client.get(API_V1_PREFIX + "/orders")
    assert response.status_code == 200
    assert len(response.json()) == 100

    # simple item test
    first_item = response.json()[0]
    response = client.get(API_V1_PREFIX + f"/orders/{first_item['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == first_item["id"]

    # test with start_date
    response = client.get(API_V1_PREFIX + "/orders?start_date=2017-01-01")
    assert response.status_code == 200
    assert len(response.json()) == 100
    from datetime import datetime

    assert (
        datetime.fromisoformat(response.json()[0]["ordered_at"]).date()
        == datetime.fromisoformat("2017-01-01").date()
    )

    # test with start and end date
    response = client.get(
        API_V1_PREFIX
        + "/orders?start_date=2017-01-01&end_date=2017-01-02&page_size=5000"
    )
    assert response.status_code == 200
    assert len(response.json()) == 176
    for order in response.json():
        assert (
            datetime.fromisoformat(order["ordered_at"]).date()
            >= datetime.fromisoformat("2017-01-01").date()
        )
        assert (
            datetime.fromisoformat(order["ordered_at"]).date()
            <= datetime.fromisoformat("2017-01-02").date()
        )


def test_stores_router():
    # simple collection test
    response = client.get(API_V1_PREFIX + "/stores")
    assert response.status_code == 200
    assert len(response.json()) == 6

    # simple item test
    first_item = response.json()[0]
    response = client.get(API_V1_PREFIX + f"/stores/{first_item['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == first_item["id"]


def test_supplies_router():
    # simple collection test
    response = client.get(API_V1_PREFIX + "/supplies")
    assert response.status_code == 200
    assert len(response.json()) == 65

    # simple item test
    first_item = response.json()[0]
    response = client.get(API_V1_PREFIX + f"/supplies/{first_item['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == first_item["id"]


@pytest.mark.parametrize(
    "table_name", ["customers", "products", "stores", "supplies"]
)  # , "orders", "items"])
@pytest.mark.parametrize("page_size", [None, 500])
def test_pagination(table_name, page_size):
    expected_page_size = page_size or DEFAULT_PAGE_SIZE
    current_page = 1
    collected_items = []

    while True:
        response = client.get(
            API_V1_PREFIX
            + f"/{table_name}?page={current_page}&page_size={expected_page_size}"
        )
        assert response.status_code == 200
        item_count = len(response.json())
        assert item_count <= expected_page_size
        collected_items += response.json()
        if item_count < expected_page_size:
            break
        current_page += 1

    expected_item_count = EXPECTED_TABLES_COUNTS_ALL[table_name]

    assert len(collected_items) == EXPECTED_TABLES_COUNTS_ALL[table_name]
    expected_last_page = expected_item_count // expected_page_size + 1
    assert current_page == expected_last_page

    # verify primary keys are unique
    if primary_key := PRIMARY_KEYS.get(table_name):
        primary_keys = set()
        for item in collected_items:
            assert item[primary_key] not in primary_keys
            primary_keys.add(item[primary_key])
        assert len(primary_keys) == expected_item_count
