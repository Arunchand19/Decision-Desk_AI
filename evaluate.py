import json
import os

from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite:///./evaluation.db")
os.environ.setdefault("JWT_SECRET", "evaluation-secret")

from src.api import app
from src.database import init_db


def main() -> None:
    cases = json.loads(open("sample_test_cases.json", encoding="utf-8").read())
    init_db()
    client = TestClient(app)
    email = "evaluation@example.com"
    client.post("/register", json={"email": email, "password": "password123"})
    token = client.post("/login", json={"email": email, "password": "password123"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    correct = 0
    for case in cases:
        response = client.post("/tickets", headers=headers, json={"message": case["message"]})
        action = response.json()["decision"]["action"]
        correct += action == case["expected_action"]
        print(f"{'OK' if action == case['expected_action'] else 'MISS'}: {action} | {case['message']}")
    print(f"{len(cases)} test cases")
    print(f"Correct: {correct}")
    print(f"Incorrect: {len(cases) - correct}")
    print(f"Accuracy: {correct / len(cases):.0%}")


if __name__ == "__main__":
    main()
