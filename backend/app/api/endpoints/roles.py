from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.roles import RoleCreate, RoleSch
from app.db.models import Role
# from app.services.user_service import get_user, create_user
from app.db.session import get_db


router = APIRouter()

@router.post("/roles", response_model=None)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@router.get("/roles", response_model=List[RoleSch])
def read_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles
