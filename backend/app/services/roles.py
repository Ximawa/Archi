from sqlalchemy.orm import Session
from app.schemas.roles import RoleCreate, RoleSch
from app.db.models import Role

def create_role_service(role: RoleCreate, db: Session):
    db_role = Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def read_roles_service(db: Session):
    roles = db.query(Role).all()
    return roles    