"""
TODO: add pydantic models for jaffle shop
"""

from pydantic import BaseModel


class Customer(BaseModel):
    id: str
    name: str
