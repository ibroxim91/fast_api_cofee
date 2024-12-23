from pydantic import BaseModel
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    description: Optional[str] = None
    # products: List["Product"] = []

    class Config:
        orm_mode = True  

    