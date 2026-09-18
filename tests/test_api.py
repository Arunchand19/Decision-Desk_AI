import os

os.environ["DATABASE_URL"] = "sqlite:///./test_support_ai.db"
os.environ["JWT_SECRET"] = "test-secret"

from fastapi.testclient import TestClient

from src.api import app
from src.database import Base, engine


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
client = TestClient(app)


def register_and_login(email: str) -> str:
    response = client.post("/register", json={"email": email, "password": "password123"})
    assert response.status_code == 201
    response = client.post("/login", json={"email": email, "password": "password123"})
    assert response.status_code == 200
    return response.json()["access_token"]


def test_ticket_requires_authentication():
    response = client.post("/tickets", json={"message": "My parcel is damaged and I need help."})
    assert response.status_code == 401


def test_users_can_only_read_their_own_tickets():
    alice_token = register_and_login("alice@example.com")
    bob_token = register_and_login("bob@example.com")
    response = client.post("/tickets", headers={"Authorization": f"Bearer {alice_token}"}, json={"message": "My package arrived damaged and I have no photos."})
    assert response.status_code == 201
    ticket_id = response.json()["id"]
    response = client.get(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {bob_token}"})
    assert response.status_code == 404
    response = client.get("/tickets", headers={"Authorization": f"Bearer {bob_token}"})
    assert response.status_code == 200
    assert response.json() == []


def test_ticket_persists_structured_decision():
    token = register_and_login("carol@example.com")
    response = client.post("/tickets", headers={"Authorization": f"Bearer {token}"}, json={"message": "My item arrived damaged and I have not taken photos."})
    assert response.status_code == 201
    decision = response.json()["decision"]
    assert decision["action"] == "REQUEST_PHOTOS"
    assert 0 <= decision["confidence"] <= 1
    assert decision["sources"]
