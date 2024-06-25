import sys
import os
from random import randint

# Ajouter le répertoire backend/app au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.db.models import User , Role, Beer
from app.utils.security import get_password_hash

def init_db():
    # Créer les tables dans la base de données
    Base.metadata.create_all(bind=engine)
    
    # Créer une session pour ajouter des données
    db = SessionLocal()

    # Ajouter des rôles
    patron = Role(name="Manager")
    barman = Role(name="Barman")
    db.add(patron)
    db.add(barman)
    db.commit()

    # Ajouter des données de démonstration
    demo_patron = User(
        username="Patron",
        email="demo@example.com",
        hashed_password=get_password_hash("wiwi"),
        role_id=patron.id,
    )
    demo_barman = User(
        username="Barman",
        email="demoBarman@example.com",
        hashed_password=get_password_hash("barman"),
        role_id=barman.id,
    )
    db.add(demo_patron)
    db.add(demo_barman)
    db.commit()
    db.close()

    # Ajouter des bières
    beers = [
        "Heineken",
        "Stella Artois",
        "Guinness",
        "Carlsberg",
        "Budweiser",
        "Amstel",
        "Hoegaarden",
        "Leffe Blonde",
        "Leffe Brune",
        "Chimay Blue",
        "Corona",
        "Kronenbourg 1664",
        "Pilsner Urquell",
        "Paulaner",
        "Beck's"
    ]

    beer_objects = []
    for beer_name in beers:
        stock = randint(5, 20)  # Random stock between 5 and 20
        min_stock = randint(3, 10)  # Random minimum stock between 3 and 10
        beer_objects.append(Beer(name=beer_name, stock=stock, min_stock=min_stock))
    
    db.add_all(beer_objects)
    db.commit()

    

if __name__ == "__main__":
    init_db()