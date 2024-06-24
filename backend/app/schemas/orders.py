from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class OrderItemBase(BaseModel):
    beer_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderSch(BaseModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    items: List[OrderItemBase]

    ConfigDict(from_attributes=True)