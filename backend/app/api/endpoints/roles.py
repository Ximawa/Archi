from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.roles import RoleCreate, RoleSch
from app.services.roles import create_role_service, read_roles_service
from app.db.session import get_db


router = APIRouter()

@router.post("/create", response_model=None)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role_service(role, db)


@router.get("/read_all", response_model=List[RoleSch])
def read_roles(db: Session = Depends(get_db)):
    return read_roles_service(db)