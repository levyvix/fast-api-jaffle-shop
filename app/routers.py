"""
All jaffle shop routers
"""

import duckdb

from fastapi import APIRouter, Depends, Response

from app.db import get_db
from app.const import PAGE_SIZE, BASE_URL

# defined routers
customers_router = APIRouter(tags=["customers"])
orders_router = APIRouter(tags=["orders"])
item_router = APIRouter(tags=["items"])
product_router = APIRouter(tags=["products"])
supplies_router = APIRouter(tags=["supplies"])
store_router = APIRouter(tags=["stores"])


def _get_paged_response(
    db: duckdb.DuckDBPyConnection, table_name: str, page: int, response: Response
):
    """
    Get a paged response from a collection endpoint
    Will insert next header if applicable
    """

    offset = (page - 1) * PAGE_SIZE
    last_item = offset + PAGE_SIZE
    count = db.sql(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

    url = f"{BASE_URL}/{table_name}"
    if last_item < count:
        next_page = page + 1
        next_link = f'<{url}?page={next_page}>; rel="next"'
        response.headers["Link"] = next_link

    cursor = db.sql(f"SELECT * FROM {table_name} LIMIT {PAGE_SIZE} OFFSET {offset}")
    column_names = [desc[0] for desc in cursor.description]
    return [dict(zip(column_names, row)) for row in cursor.fetchall()]


def _get_single_response(db: duckdb.DuckDBPyConnection, query: str):
    """
    Get a single response from a collection endpoint
    """
    cursor = db.sql(query)
    column_names = [desc[0] for desc in cursor.description]
    return dict(zip(column_names, cursor.fetchone()))


#
# Customers
#
CUSTOMER_COLUMNS = [
    "id",
    "name",
]


@customers_router.get("/customers")
async def get_customers(
    page: int = 1,
    response: Response = None,
    db: duckdb.DuckDBPyConnection = Depends(get_db),
):
    return _get_paged_response(db, "customers", page, response)


@customers_router.get("/customers/{customer_id}")
async def get_customer(
    customer_id: str, db: duckdb.DuckDBPyConnection = Depends(get_db)
):
    return _get_single_response(
        db, f"SELECT * FROM customers WHERE id = '{customer_id}'"
    )


#
# Orders
#
@orders_router.get("/orders")
async def get_orders(
    page: int = 1,
    response: Response = None,
    db: duckdb.DuckDBPyConnection = Depends(get_db),
):
    return _get_paged_response(db, "orders", page, response)


@orders_router.get("/orders/{order_id}")
async def get_order(order_id: str, db: duckdb.DuckDBPyConnection = Depends(get_db)):
    return _get_single_response(db, f"SELECT * FROM orders WHERE id = '{order_id}'")


#
# Items
#
@item_router.get("/items")
async def get_items(
    page: int = 1,
    response: Response = None,
    db: duckdb.DuckDBPyConnection = Depends(get_db),
):
    return _get_paged_response(db, "items", page, response)


@item_router.get("/items/{item_id}")
async def get_item(item_id: str, db: duckdb.DuckDBPyConnection = Depends(get_db)):
    return _get_single_response(db, f"SELECT * FROM items WHERE id = '{item_id}'")


#
# Products
#
@product_router.get("/products")
async def get_products(
    page: int = 1,
    response: Response = None,
    db: duckdb.DuckDBPyConnection = Depends(get_db),
):
    return _get_paged_response(db, "products", page, response)


@product_router.get("/products/{sku}")
async def get_product(sku: str, db: duckdb.DuckDBPyConnection = Depends(get_db)):
    return _get_single_response(db, f"SELECT * FROM products WHERE sku = '{sku}'")


#
# Stores
#
@store_router.get("/stores")
async def get_stores(
    page: int = 1,
    response: Response = None,
    db: duckdb.DuckDBPyConnection = Depends(get_db),
):
    return _get_paged_response(db, "stores", page, response)


@store_router.get("/stores/{store_id}")
async def get_store(store_id: str, db: duckdb.DuckDBPyConnection = Depends(get_db)):
    return _get_single_response(db, f"SELECT * FROM stores WHERE id = '{store_id}'")


#
# Supplies
#
@supplies_router.get("/supplies")
async def get_supplies(
    page: int = 1,
    response: Response = None,
    db: duckdb.DuckDBPyConnection = Depends(get_db),
):
    return _get_paged_response(db, "supplies", page, response)


@supplies_router.get("/supplies/{supply_id}")
async def get_supply(supply_id: str, db: duckdb.DuckDBPyConnection = Depends(get_db)):
    return _get_single_response(db, f"SELECT * FROM supplies WHERE id = '{supply_id}'")
