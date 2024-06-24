from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserSch, UserCreate, UserLoginAns, UserLogin
from app.db.models import User
from app.utils.security import get_password_hash, verify_password

router = APIRouter()

@router.post("/users", response_model=UserSch)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email,
                   hashed_password=hashed_password, role_id=user.role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=UserLoginAns)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    # Adjusted to match the expected response model structure of UserLoginAns
    return {
        "success": True,
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "role_id": db_user.role_id
        }
    }


@router.get("/users", response_model=List[UserSch])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users