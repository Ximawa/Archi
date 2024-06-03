from pydantic import BaseModel
from typing import List
from datetime import datetime


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleSch(RoleBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    role_id: int


class UserSch(UserBase):
    id: int
    role: RoleSch

    class Config:
        orm_mode = True


class BeerBase(BaseModel):
    name: str
    stock: int
    min_stock: int


class BeerCreate(BeerBase):
    pass


class BeerSch(BeerBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    quantity: int


class OrderCreate(OrderBase):
    beers: List[int]


class OrderSch(OrderBase):
    id: int
    timestamp: datetime
    beers: List[BeerSch]

    class Config:
        orm_mode = True
