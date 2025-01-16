# from __future__ import annotations
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import List

class ProductBase(BaseModel):
    name: str
    price: float
    description: Optional [str] = None
    inventory: int
    on_sales: Optional [bool] = False

class ProductCreate(ProductBase):
    pass

# class ProductUpdate(ProductBase):
#     price: Optional [float] = None
#     inventory: Optional [int] = None
#     on_sales: Optional [bool] = None

class ProductResponse(ProductBase):
    id: int
    created: datetime 
    user_id: int
    owner: "UserResponse"

    class Config:
        from_attributes = True

# count feature
class ProductsListResponse(BaseModel):
    count: int
    products: List[ProductResponse]

    class Config:
        from_attributes= True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional [int] = None