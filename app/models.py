"""
TODO: add pydantic models for jaffle shop
"""

from typing import Optional, List

from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class Customer(BaseModel):
    id: str
    name: str


class Supply(BaseModel):
    id: str
    name: str
    cost: Decimal
    perishable: bool
    sku: str


class Item(BaseModel):
    id: str
    order_id: str
    sku: str


class Order(BaseModel):
    id: str
    customer_id: str
    store_id: str
    ordered_at: datetime
    subtotal: Decimal
    tax_paid: Decimal
    order_total: Decimal
    items: Optional[List[Item]]


class Product(BaseModel):
    sku: str
    name: str
    sku: str
    price: Decimal
    description: str


class Store(BaseModel):
    id: str
    name: str
    opened_at: datetime
    tax_rate: Decimal
