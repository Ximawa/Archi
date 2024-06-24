from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserSch(UserBase):
    id: Optional[int] = None
    role_id: int

    ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str
    role_id: int

class User(BaseModel):
    id: int
    username: str
    email: str
    role_id: int

class UserLoginAns(BaseModel):
    success: bool
    user: User

class UserLogin(BaseModel):
    username: str
    password: str
