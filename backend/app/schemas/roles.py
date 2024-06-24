from pydantic import BaseModel

class RoleCreate(BaseModel):
    name: str

class RoleSch(BaseModel):
    id: int
    name: str