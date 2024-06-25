from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Order, OrderItem, Beer 
from app.schemas.schemas import OrderCreate, OrderSch
from app.services.orders import create_order_service, read_order_service, order_pdf_service, read_orders_service

router = APIRouter()


@router.post("/create")
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    return create_order_service(order_data, db)

@router.get("/read_all", response_model=List[OrderSch])
def read_orders(db: Session = Depends(get_db)):
    return read_orders_service(db)

@router.get("/{order_id}", response_model=OrderSch)
def read_order(order_id: int, db: Session = Depends(get_db)):
    return read_order_service(order_id, db)

@router.get("/pdf/{order_id}")
def order_pdf(order_id: int, db: Session = Depends(get_db)):
    return order_pdf_service(order_id, db)




