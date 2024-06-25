from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserSch, UserCreate, UserLoginAns, UserLogin
from app.services.users import create_user_service, login_user_service, read_users_service

router = APIRouter()

@router.post("/create", response_model=UserSch)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(user, db)


@router.post("/login", response_model=UserLoginAns)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    return login_user_service(user, db)


@router.get("/read_all", response_model=List[UserSch])
def read_users(db: Session = Depends(get_db)):
    return read_users_service(db)