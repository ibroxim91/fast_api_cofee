from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
