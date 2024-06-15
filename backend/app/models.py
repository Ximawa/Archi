from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./inventaire_biere.db"  # Example database URL

engine = create_engine(
    DATABASE_URL,
    # Required for SQLite; omit for other databases
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


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
