"""
All jaffle shop routers
"""

import duckdb
from urllib.parse import urlencode
from fastapi import APIRouter, Depends, Response, Request

from app.db import get_db
from app.const import PAGE_SIZE

# defined routers
customers_router = APIRouter(tags=["customers"])
orders_router = APIRouter(tags=["orders"])
item_router = APIRouter(tags=["items"])
product_router = APIRouter(tags=["products"])
supplies_router = APIRouter(tags=["supplies"])
store_router = APIRouter(tags=["stores"])


def _get_list_response(db: duckdb.DuckDBPyConnection, query: str):
    """
    Get a list response from a collection endpoint
    """
    cursor = db.sql(query)
    column_names = [desc[0] for desc in cursor.description]
    return [dict(zip(column_names, row)) for row in cursor.fetchall()]


def _get_paged_response(
    db: duckdb.DuckDBPyConnection,
    request: Request,
    table_name: str,
    page: int = 1,
    response: Response = None,
    where_clause: str = "",
    sort_by: str = "",
):
    """
    Get a paged response from a collection endpoint
    Will insert next header if applicable
    """

    offset = (page - 1) * PAGE_SIZE
    last_item = offset + PAGE_SIZE
    count = db.query(f"SELECT COUNT(*) FROM {table_name} {where_clause}").fetchone()[0]

    # get base url from request
    # forwarded_host = request.headers.get(
    #     "X-Forwarded-Host", request.headers.get("Host")
    # )
    # scheme = request.headers.get("X-Forwarded-Proto", "http")

    url = f"/{table_name}"
    query_params = dict(request.query_params)
    if last_item < count and response:
        query_params["page"] = page + 1
        next_link = f'<{url}?{urlencode(query_params)}>; rel="next"'
        response.headers["Link"] = next_link

    return _get_list_response(
        db,
        f"SELECT * FROM {table_name} {where_clause} {sort_by} LIMIT {PAGE_SIZE} OFFSET {offset}",
    )


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


@customers_router.get("/customers")
async def get_customers(
    page: int = 1,
    response: Response = None,
    request: Request = None,
    db: duckdb.DuckDBPyConnection = Depends(get_db),
):
    return _get_paged_response(db, request, "customers", page, response)


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


def _enrich_orders(db: duckdb.DuckDBPyConnection, orders: list[dict]):
    """
    Enrich orders with list of items
    """
    for order in orders:
        order["items"] = _get_list_response(
            db, f"SELECT * FROM items WHERE order_id = '{order['id']}'"
        )
    return orders


@orders_router.get("/orders")
async def get_orders(
    page: int = 1,
    start_date: str = None,
    end_date: str = None,
    response: Response = None,
    request: Request = None,
    db: duckdb.DuckDBPyConnection = Depends(get_db),
):
    where_clause = ""
    if start_date:
        where_clause += f" AND ordered_at >= '{start_date}'"
    if end_date:
        where_clause += f" AND ordered_at <= '{end_date}'"
    if where_clause:
        where_clause = f"WHERE {where_clause[5:]}"
    sort_by = "ORDER BY ordered_at ASC"
    orders = _get_paged_response(
        db, request, "orders", page, response, where_clause, sort_by
    )
    return _enrich_orders(db, orders)


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
    request: Request = None,
    db: duckdb.DuckDBPyConnection = Depends(get_db),
):
    return _get_paged_response(db, request, "items", page, response)


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
    request: Request = None,
    db: duckdb.DuckDBPyConnection = Depends(get_db),
):
    return _get_paged_response(db, request, "products", page, response)


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
    request: Request = None,
    db: duckdb.DuckDBPyConnection = Depends(get_db),
):
    return _get_paged_response(db, request, "stores", page, response)


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
    request: Request = None,
    db: duckdb.DuckDBPyConnection = Depends(get_db),
):
    return _get_paged_response(db, request, "supplies", page, response)


@supplies_router.get("/supplies/{supply_id}")
async def get_supply(supply_id: str, db: duckdb.DuckDBPyConnection = Depends(get_db)):
    return _get_single_response(db, f"SELECT * FROM supplies WHERE id = '{supply_id}'")
