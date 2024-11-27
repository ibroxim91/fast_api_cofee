from pydantic import BaseModel
from typing import Optional, List

class CartAdd(BaseModel):
    product: int
    quantity: int = 1

class Cart(BaseModel):
    product_id: int
    quantity: int 
    total_price: float    

    class Config:
        orm_mode = True