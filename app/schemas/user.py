from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None  # Parol yangilash uchun

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str
    phone: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str
