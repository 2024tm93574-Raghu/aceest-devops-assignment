import sys
import os
import pytest

# FIX IMPORT PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200

def test_dashboard(client):
    res = client.get("/dashboard")
    assert res.status_code == 200

def test_calories_api(client):
    res = client.post("/recommend_calories", json={
        "weight": 70,
        "program": "Fat Loss"
    })
    assert res.status_code == 200