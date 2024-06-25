from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.db.models import Order, OrderItem, Beer 
from app.schemas.schemas import OrderCreate, OrderSch

def create_order_in_db_service(order_data: OrderCreate, db: Session):
    new_order = Order()
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order_data.items:
        beer = db.query(Beer).filter(Beer.id == item.beer_id).first()
        if not beer:
            raise HTTPException(status_code=404, detail=f"Beer with ID {
                                item.beer_id} not found")

        order_item = OrderItem(order_id=new_order.id,
                               beer_id=item.beer_id, quantity=item.quantity)
        db.add(order_item)

    db.commit()

    return new_order

def create_order_service(order_data: OrderCreate, db: Session):
    try:
        new_order = create_order_in_db_service(order_data, db)
        return {"order_id": new_order.id}
    except HTTPException as e:
        raise e

def read_order_service(order_id: int, db: Session):
    order = db.query(Order).join(OrderItem).filter(
        Order.id == order_id).first()

    return order

def order_pdf_service(order_id: int, db: Session):
    order_data = db.query(Order).join(
        OrderItem).filter(Order.id == order_id).first()
    if not order_data:
        raise HTTPException(status_code=404, detail="Order not found")

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica", 12)
    created_at = order_data.created_at.strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(72, height - 50,
                 f"Date de commande : {created_at}")
    c.drawString(72, height - 72,
                 f"Id de la commande: {order_data.id}")

    c.line(72, height - 110, width - 72, height - 110)

    y_position = height - 130
    for item in order_data.items:
        beer = db.query(Beer).filter(Beer.id == item.beer_id).first()
        if not beer:
            raise HTTPException(status_code=404, detail=f"Beer with ID {
                                item.beer_id} not found")
        item_name = beer.name
        c.drawString(72, y_position, f"Item: {
                     item_name} ---------------- Quantite: {item.quantity}")
        y_position -= 20

    c.showPage()
    c.save()

    buffer.seek(0)
    return StreamingResponse(buffer, media_type='application/pdf')

def read_orders_service(db: Session):
    orders = db.query(Order).join(OrderItem).all()
    return orders