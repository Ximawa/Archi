# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import StreamingResponse

# from .db.models import User, Beer as BeerModel, Role, Order, OrderItem, SessionLocal, Base, engine
# from .schemas import UserCreate, UserSch, BeerCreate, UserLoginAns, UserLogin, Beer, RoleSch, RoleCreate, OrderItemBase, OrderSch, OrderCreate
# from passlib.context import CryptContext
# from typing import List
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from io import BytesIO
# from datetime import datetime

# New
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints.roles import router as roles_router
from app.api.endpoints.users import router as users_router
from app.api.endpoints.beers import router as beers_router
from app.api.endpoints.orders import router as orders_router
from app.db.session import engine 
from app.db.base import Base


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(roles_router, prefix="/roles", tags=["roles"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(beers_router, prefix="/beers", tags=["beers"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])

Base.metadata.create_all(bind=engine)




