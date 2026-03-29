import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret"
    with app.test_client() as client:
        yield client


# ---------- HEALTH ----------
def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


# ---------- AUTH ----------
def test_dashboard_redirects_when_not_logged_in(client):
    res = client.get("/dashboard")
    assert res.status_code == 302
    assert "/login" in res.headers["Location"]


def test_login_page_loads(client):
    res = client.get("/login")
    assert res.status_code == 200


def test_invalid_login_returns_error(client):
    res = client.post("/login", data={
        "username": "wrong",
        "password": "wrong"
    })
    assert res.status_code == 200  # stays on login page


# ---------- CALORIES API ----------
def test_calories_fat_loss(client):
    res = client.post("/recommend_calories", json={
        "weight": 70,
        "program": "Fat Loss"
    })
    assert res.status_code == 200
    assert res.get_json()["recommended_calories"] == 70 * 22


def test_calories_muscle_gain(client):
    res = client.post("/recommend_calories", json={
        "weight": 80,
        "program": "Muscle Gain"
    })
    assert res.status_code == 200
    assert res.get_json()["recommended_calories"] == 80 * 35


def test_calories_beginner(client):
    res = client.post("/recommend_calories", json={
        "weight": 60,
        "program": "Beginner"
    })
    assert res.status_code == 200
    assert res.get_json()["recommended_calories"] == 60 * 26