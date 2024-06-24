from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
from sqlalchemy.orm import Session
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.db.session import get_db
from app.db.models import Order, OrderItem, Beer 
from app.schemas.schemas import OrderCreate, OrderSch

router = APIRouter()


@router.post("/orders")
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    try:
        new_order = create_order_in_db(order_data, db)
        return {"order_id": new_order.id}
    except HTTPException as e:
        raise e

@router.get("/order/{order_id}", response_model=OrderSch)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).join(OrderItem).filter(
        Order.id == order_id).first()

    return order

@router.get("/order-pdf/{order_id}")
def order_pdf(order_id: int, db: Session = Depends(get_db)):
    order_data = db.query(Order).join(
        OrderItem).filter(Order.id == order_id).first()
    if not order_data:
        raise HTTPException(status_code=404, detail="Order not found")

    # Create a PDF document in memory
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Add content to the PDF
    c.setFont("Helvetica", 12)
    created_at = order_data.created_at.strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(72, height - 50,
                 f"Date de commande : {created_at}")
    c.drawString(72, height - 72,
                 f"Id de la commande: {order_data.id}")

    # Draw a line to separate the header
    c.line(72, height - 110, width - 72, height - 110)

    # Assuming OrderItem has fields you want to display, add them here
    y_position = height - 130
    for item in order_data.items:
        # Assuming 'items' is a relationship field on your Order model
        beer = db.query(Beer).filter(Beer.id == item.beer_id).first()
        if not beer:
            raise HTTPException(status_code=404, detail=f"Beer with ID {
                item.beer_id} not found")
        item_name = beer.name
        c.drawString(72, y_position, f"Item: {
                     item_name} ---------------- Quantite: {item.quantity}")
        y_position -= 20

    # Finalize the PDF
    c.showPage()
    c.save()

    # Move the buffer to the beginning so it can be read
    buffer.seek(0)

    # Return the PDF as a streaming response
    return StreamingResponse(buffer, media_type='application/pdf')


@router.get("/orders/all", response_model=List[OrderSch])
def read_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders

def create_order_in_db(order_data: OrderCreate, db: Session):
    # Create a new order instance. Assuming Order model has an 'id' and 'items' relationship
    new_order = Order()
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order_data.items:
        # Check if the beer exists
        beer = db.query(Beer).filter(Beer.id == item.beer_id).first()
        if not beer:
            raise HTTPException(status_code=404, detail=f"Beer with ID {
                                item.beer_id} not found")

        # Create a new OrderItem and link it to the order and beer
        order_item = OrderItem(order_id=new_order.id,
                               beer_id=item.beer_id, quantity=item.quantity)
        db.add(order_item)

    # Commit the order items to the database
    db.commit()

    return new_order  # Return the newly created order
