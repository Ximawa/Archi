from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.beers import BeerSch , BeerCreate
from app.db.models import Beer

router = APIRouter()

@router.post("/beers", response_model=BeerSch)
def create_beer(beer: BeerCreate, db: Session = Depends(get_db)):
    db_beer = Beer(name=beer.name, stock=beer.stock,
                        min_stock=beer.min_stock)
    db.add(db_beer)
    db.commit()
    db.refresh(db_beer)
    return db_beer


@router.get("/beers", response_model=List[BeerSch])
def read_beers(db: Session = Depends(get_db)):
    beers = db.query(Beer).all()
    return beers

@router.post("/beers/{beer_id}/reduce_stock", response_model=BeerSch)
def reduce_beer_stock(beer_id: int, db: Session = Depends(get_db)):
    # Query the database for the beer
    beer = db.query(Beer).filter(Beer.id == beer_id).first()

    # Check if the beer exists
    if beer is None:
        raise HTTPException(status_code=404, detail="Beer not found")

    # Reduce the stock by 1
    if beer.stock > 0:  # Ensure stock doesn't go negative
        beer.stock -= 1
        db.commit()
        db.refresh(beer)
    else:
        raise HTTPException(status_code=400, detail="Beer stock is already 0")

    return beer

@router.get("/beers/low_stock", response_model=List[BeerSch])
def read_low_stock_beers(db: Session = Depends(get_db)):
    low_stock_beers = db.query(Beer).filter(
        Beer.stock < Beer.min_stock).all()
    return low_stock_beers