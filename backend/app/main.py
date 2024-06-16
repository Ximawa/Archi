from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.models import User, Beer as BeerModel, Role, Order, OrderItem, SessionLocal, Base, engine
from app.schemas import UserCreate, UserSch, BeerCreate, UserLogin, Beer, RoleSch, RoleCreate, OrderItemBase, OrderSch, OrderCreate
from passlib.context import CryptContext
from typing import List
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
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


@app.post("/roles", response_model=None)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@app.get("/roles", response_model=List[RoleSch])
def read_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles


@app.post("/users", response_model=UserSch)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email,
                   hashed_password=hashed_password, role_id=user.role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/login", response_model=UserSch)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    return db_user


@app.get("/users", response_model=List[UserSch])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.post("/beers", response_model=Beer)
def create_beer(beer: BeerCreate, db: Session = Depends(get_db)):
    db_beer = BeerModel(name=beer.name, stock=beer.stock,
                        min_stock=beer.min_stock)
    db.add(db_beer)
    db.commit()
    db.refresh(db_beer)
    return db_beer


@app.get("/beers", response_model=List[Beer])
def read_beers(db: Session = Depends(get_db)):
    beers = db.query(BeerModel).all()
    return beers


@app.post("/orders")
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    print(order_data)
    try:
        new_order = create_order_in_db(order_data, db)
        return {"order_id": new_order.id}
    except HTTPException as e:
        raise e


@app.post("/beers/{beer_id}/reduce_stock", response_model=Beer)
def reduce_beer_stock(beer_id: int, db: Session = Depends(get_db)):
    # Query the database for the beer
    beer = db.query(BeerModel).filter(BeerModel.id == beer_id).first()

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


@app.get("/beers/low_stock", response_model=List[Beer])
def read_low_stock_beers(db: Session = Depends(get_db)):
    low_stock_beers = db.query(BeerModel).filter(
        BeerModel.stock < BeerModel.min_stock).all()
    return low_stock_beers


@app.get("/order/{order_id}", response_model=OrderSch)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).join(OrderItem).filter(
        Order.id == order_id).first()

    return order


@app.get("/order-pdf/{order_id}")
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
        beer = db.query(BeerModel).filter(BeerModel.id == item.beer_id).first()
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


@app.get("/orders/all", response_model=List[OrderSch])
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
        beer = db.query(BeerModel).filter(BeerModel.id == item.beer_id).first()
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
