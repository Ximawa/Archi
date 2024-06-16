import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..main import app, get_db
from ..models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_user(test_db):
    response = client.post("/users", json={"username": "testuser",
                           "email": "test@example.com", "password": "testpassword", "role_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


def test_login_user_valid(test_db):
    client.post("/users", json={"username": "userTest",
                "password": "pswdTest", "email": "user@test.com", "role_id": 1})
    response = client.post(
        "/login", json={"username": "userTest", "password": "pswdTest"})
    assert response.status_code == 200
    assert response.json()["success"] == True


def test_login_user_invalid(test_db):
    response = client.post(
        "/login", json={"username": "invalidUser", "password": "invalidPassword"})
    assert response.status_code == 404


def test_create_role(test_db):
    response = client.post("/roles", json={"name": "New Role"})
    assert response.status_code == 200
    assert "id" in response.json()


def test_read_roles(test_db):
    client.post("/roles", json={"name": "Another Role"})
    response = client.get("/roles")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_create_beer_valid(test_db):
    response = client.post(
        "/beers", json={"name": "New Beer", "stock": 100, "min_stock": 10})
    assert response.status_code == 200
    assert response.json()["name"] == "New Beer"


def test_read_beers(test_db):
    response = client.get("/beers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_order(test_db):
    response = client.post(
        "/orders", json={"items": [{"beer_id": 1, "quantity": 2}]})
    assert response.status_code == 200
    assert "order_id" in response.json()


def test_read_low_stock_beers(test_db):
    response = client.get("/beers/low_stock")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_generate_order_pdf(test_db):
    response = client.get("/order-pdf/1")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
