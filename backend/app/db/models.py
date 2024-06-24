from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base


class Beer(Base):
    __tablename__ = "beers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    stock = Column(Integer)
    min_stock = Column(Integer)
    order_items = relationship("OrderItem", back_populates="beer")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    beer_id = Column(Integer, ForeignKey('beers.id'))
    quantity = Column(Integer)

    order = relationship("Order", back_populates="items")
    beer = relationship("Beer", back_populates="order_items")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role")
