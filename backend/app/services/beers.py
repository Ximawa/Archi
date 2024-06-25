from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import Beer
from app.schemas.beers import BeerCreate

def create_beer_service(beer: BeerCreate, db: Session):
    db_beer = Beer(name=beer.name, stock=beer.stock,
                    min_stock=beer.min_stock)
    db.add(db_beer)
    db.commit()
    db.refresh(db_beer)
    return db_beer

def read_beers_service(db: Session):
    beers = db.query(Beer).all()
    return beers

def reduce_beer_stock_service(beer_id: int, db: Session):
    beer = db.query(Beer).filter(Beer.id == beer_id).first()

    if beer is None:
        raise HTTPException(status_code=404, detail="Beer not found")

    if beer.stock > 0: 
        beer.stock -= 1
        db.commit()
        db.refresh(beer)
    else:
        raise HTTPException(status_code=400, detail="Beer stock is already 0")

    return beer

def read_low_stock_beers_service(db: Session):
    low_stock_beers = db.query(Beer).filter(
        Beer.stock < Beer.min_stock).all()
    return low_stock_beers