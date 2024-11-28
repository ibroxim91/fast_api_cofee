from pydantic import BaseModel
from typing import Optional
from .product import Product
from .user import User
from typing import List


__all__ = [
    "OrderBase",
    "OrderCreate",
    "Order",
]

class ProductBase(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    id: int
    total_price: float
    products: List[ProductBase]

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    user_id: int
    product_id: int

class Order(OrderBase):
    id: int
    user: Optional[User] = None
    product: Optional[Product] = None

    class Config:
        orm_mode = True
