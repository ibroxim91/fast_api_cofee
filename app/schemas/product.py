from pydantic import BaseModel
from typing import Optional
from .category import Category
from fastapi import UploadFile, File


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ProductCreate(ProductBase):
    category_id: int
    image: Optional[str] = None


class Product(ProductBase):
    category_id: Optional[Category] = None

    class Config:
        orm_mode = True
