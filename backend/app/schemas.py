from pydantic import BaseModel
from typing import List, Optional


class BeerBase(BaseModel):
    name: str
    stock: int
    min_stock: int


class BeerCreate(BeerBase):
    pass


class Beer(BeerBase):
    id: int

    class Config:
        orm_mode = True


class OrderItemBase(BaseModel):
    beerId: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderSch(BaseModel):
    id: Optional[int] = None
    items: List[OrderItem]

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    role_id: int


class User(UserBase):
    id: int
    role_id: int

    class Config:
        orm_mode = True
