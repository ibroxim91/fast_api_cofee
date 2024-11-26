from pydantic import BaseModel
from typing import Optional
from schemas.category import Category

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ProductCreate(ProductBase):
    category_id: int

class Product(ProductBase):
    id: int
    category: Optional[Category] = None

    class Config:
        orm_mode = True
