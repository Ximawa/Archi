from pydantic import BaseModel, ConfigDict

class BeerBase(BaseModel):
    name: str
    stock: int
    min_stock: int

class BeerSch(BeerBase):
    id: int

    ConfigDict(from_attributes=True)

class BeerCreate(BeerBase):
    pass