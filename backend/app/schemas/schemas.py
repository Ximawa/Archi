from pydantic import BaseModel, ConfigDict, Extra
from typing import List, Optional
from datetime import datetime


class BeerBase(BaseModel):
    name: str
    stock: int
    min_stock: int


class BeerCreate(BeerBase):
    pass


class Beer(BeerBase):
    id: int

    ConfigDict(from_attributes=True)


class OrderItemBase(BaseModel):
    beer_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int

    ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderSch(BaseModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    items: List[OrderItemBase]

    ConfigDict(from_attributes=True)


class RoleCreate(BaseModel):
    name: str


class RoleSch(BaseModel):
    id: int
    name: str


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    role_id: int


class UserLogin(BaseModel):
    username: str
    password: str


class UserSch(UserBase):
    id: Optional[int] = None
    role_id: int

    ConfigDict(from_attributes=True)


class User(BaseModel):
    id: int
    username: str
    email: str
    role_id: int


class UserLoginAns(BaseModel):
    success: bool
    user: User
