import json
from app import app


def test_health_endpoint():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"


def test_recommend_calories_ok():
    client = app.test_client()
    payload = {"weight": 80, "program": "Fat Loss FL 3 day"}
    resp = client.post("/recommend_calories",
                       data=json.dumps(payload),
                       content_type="application/json")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["recommended_calories"] == 80 * 22  # factor from PROGRAMS


def test_recommend_calories_missing_fields():
    client = app.test_client()
    resp = client.post("/recommend_calories",
                       data=json.dumps({}),
                       content_type="application/json")
    assert resp.status_code == 400
