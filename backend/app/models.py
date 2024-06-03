from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "sqlite:///./inventaire_biere.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Table de liaison pour la relation Many-to-Many entre Order et Beer
order_beer = Table('order_beer', Base.metadata,
                   Column('order_id', Integer, ForeignKey(
                       'orders.id'), primary_key=True),
                   Column('beer_id', Integer, ForeignKey(
                       'beers.id'), primary_key=True)
                   )


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role")


class Beer(Base):
    __tablename__ = 'beers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    stock = Column(Integer)
    min_stock = Column(Integer)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    beers = relationship("Beer", secondary=order_beer, backref="orders")
