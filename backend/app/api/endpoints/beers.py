from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.beers import BeerSch , BeerCreate
from app.services.beers import create_beer_service, read_beers_service, reduce_beer_stock_service, read_low_stock_beers_service

router = APIRouter()

@router.post("/create", response_model=BeerSch)
def create_beer(beer: BeerCreate, db: Session = Depends(get_db)):
    return create_beer_service(beer, db)


@router.get("/read_all", response_model=List[BeerSch])
def read_beers(db: Session = Depends(get_db)):
    return read_beers_service(db)

@router.post("/reduce_stock/{beer_id}", response_model=BeerSch)
def reduce_beer_stock(beer_id: int, db: Session = Depends(get_db)):
    return reduce_beer_stock_service(beer_id, db)

@router.get("/low_stock", response_model=List[BeerSch])
def read_low_stock_beers(db: Session = Depends(get_db)):
    return read_low_stock_beers_service(db)