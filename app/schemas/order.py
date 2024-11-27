from pydantic import BaseModel
from typing import Optional
from schemas.product import Product
from schemas.user import User

class OrderBase(BaseModel):
    quantity: int
    total_price: float

class OrderCreate(OrderBase):
    user_id: int
    product_id: int

class Order(OrderBase):
    id: int
    user: Optional[User] = None
    product: Optional[Product] = None

    class Config:
        orm_mode = True
