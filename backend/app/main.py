from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .models import Beer, Order, Role, User, SessionLocal
from .schemas import *
from passlib.context import CryptContext
from typing import List


app = FastAPI()

origins = ["*"]  # Allow all origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/roles/", response_model=RoleSch)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@app.get("/roles/", response_model=List[RoleSch])
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles


@app.post("/users/", response_model=UserSch)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username,
                   hashed_password=hashed_password, role_id=user.role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/beers/", response_model=BeerSch)
def create_beer(beer: BeerCreate, db: Session = Depends(get_db)):
    db_beer = Beer(name=beer.name, stock=beer.stock, min_stock=beer.min_stock)
    db.add(db_beer)
    db.commit()
    db.refresh(db_beer)
    return db_beer


@app.get("/beers/", response_model=List[BeerSch])
def read_beers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    beers = db.query(Beer).offset(skip).limit(limit).all()
    return beers


@app.put("/beers/{beer_id}", response_model=BeerSch)
def update_beer(beer_id: int, beer: BeerCreate, db: Session = Depends(get_db)):
    db_beer = db.query(Beer).filter(Beer.id == beer_id).first()
    if db_beer is None:
        raise HTTPException(status_code=404, detail="Beer not found")
    db_beer.name = beer.name
    db_beer.stock = beer.stock
    db_beer.min_stock = beer.min_stock
    db.commit()
    db.refresh(db_beer)
    return db_beer


@app.delete("/beers/{beer_id}", response_model=BeerSch)
def delete_beer(beer_id: int, db: Session = Depends(get_db)):
    db_beer = db.query(Beer).filter(Beer.id == beer_id).first()
    if db_beer is None:
        raise HTTPException(status_code=404, detail="Beer not found")
    db.delete(db_beer)
    db.commit()
    return db_beer


@app.post("/orders/", response_model=OrderSch)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(quantity=order.quantity)
    for beer_id in order.beers:
        beer = db.query(Beer).filter(Beer.id == beer_id).first()
        if beer is None:
            raise HTTPException(status_code=404, detail=f"B {
                                beer_id} not found")
        db_order.beers.append(beer)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.get("/orders/", response_model=List[OrderSch])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders


@app.get("/beers/recommend", response_model=List[BeerSch])
def recommend_beers(db: Session = Depends(get_db)):
    beers = db.query(Beer).filter(Beer.stock < Beer.min_stock).all()
    return beers
