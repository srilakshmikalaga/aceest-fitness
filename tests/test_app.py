
import json
from app import app

def test_health():
    client = app.test_client()
    rv = client.get("/health")
    assert rv.status_code == 200
    assert rv.get_json()["status"] == "ok"

def test_add_and_list_workouts_json():
    client = app.test_client()
    rv = client.post("/workouts", json={"workout": "Cardio"})
    assert rv.status_code == 400
    rv = client.post("/workouts", json={"workout": "Cardio", "duration": 45})
    assert rv.status_code == 201
    data = rv.get_json()
    assert data["workout"] == "Cardio"
    assert data["duration"] == 45
    rv = client.get("/workouts")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["count"] >= 1
