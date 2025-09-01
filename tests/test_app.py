import pytest
from app import app, WORKOUTS

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    # Clear workouts before each test
    WORKOUTS.clear()
    yield
    WORKOUTS.clear()


def test_health_check():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json == {"status": "ok"}


def test_add_workout_success():
    client = app.test_client()
    resp = client.post("/workouts", json={"workout": "Pushups", "duration": 20})
    assert resp.status_code == 201
    assert resp.json["workout"] == "Pushups"
    assert resp.json["duration"] == 20


def test_add_workout_missing_fields():
    client = app.test_client()
    resp = client.post("/workouts", json={"workout": "Situps"})
    assert resp.status_code == 400
    assert "error" in resp.json


def test_add_workout_invalid_duration():
    client = app.test_client()
    resp = client.post("/workouts", json={"workout": "Jogging", "duration": "abc"})
    assert resp.status_code == 400
    assert "error" in resp.json


def test_update_workout_success():
    client = app.test_client()
    client.post("/workouts", json={"workout": "Plank", "duration": 5})
    resp = client.put("/workouts/0", json={"workout": "Plank Hold", "duration": 10})
    assert resp.status_code == 200
    assert resp.json["workout"] == "Plank Hold"
    assert resp.json["duration"] == 10


def test_update_workout_not_found():
    client = app.test_client()
    resp = client.put("/workouts/99", json={"workout": "Run", "duration": 15})
    assert resp.status_code == 404


def test_update_workout_invalid_data():
    client = app.test_client()
    client.post("/workouts", json={"workout": "Cycling", "duration": 30})
    resp = client.put("/workouts/0", json={"workout": "Cycling"})
    assert resp.status_code == 400


def test_list_workouts():
    client = app.test_client()
    client.post("/workouts", json={"workout": "Yoga", "duration": 25})
    resp = client.get("/workouts")
    assert resp.status_code == 200
    assert resp.json["count"] == 1
    assert resp.json["items"][0]["workout"] == "Yoga"


def test_get_workout_valid_id():
    client = app.test_client()
    client.post("/workouts", json={"workout": "Swim", "duration": 40})
    resp = client.get("/workouts/0")
    assert resp.status_code == 200
    assert resp.json["workout"] == "Swim"


def test_get_workout_invalid_id():
    client = app.test_client()
    resp = client.get("/workouts/5")
    assert resp.status_code == 404


def test_stats_with_data():
    client = app.test_client()
    client.post("/workouts", json={"workout": "Run", "duration": 30})
    client.post("/workouts", json={"workout": "Bike", "duration": 60})
    resp = client.get("/stats")
    assert resp.status_code == 200
    assert resp.json["count"] == 2
    assert resp.json["total_duration"] == 90
    assert resp.json["average_duration"] == 45


def test_stats_no_data():
    client = app.test_client()
    resp = client.get("/stats")
    assert resp.status_code == 200
    assert resp.json["count"] == 0
    assert resp.json["total_duration"] == 0
    assert resp.json["average_duration"] == 0


def test_longest_and_shortest():
    client = app.test_client()
    client.post("/workouts", json={"workout": "Jump Rope", "duration": 15})
    client.post("/workouts", json={"workout": "Pushups", "duration": 45})
    longest = client.get("/longest")
    shortest = client.get("/shortest")
    assert longest.status_code == 200
    assert longest.json["workout"] == "Pushups"
    assert shortest.status_code == 200
    assert shortest.json["workout"] == "Jump Rope"


def test_longest_and_shortest_no_data():
    client = app.test_client()
    assert client.get("/longest").status_code == 404
    assert client.get("/shortest").status_code == 404


def test_search_workouts_found():
    client = app.test_client()
    client.post("/workouts", json={"workout": "Bench Press", "duration": 20})
    client.post("/workouts", json={"workout": "Bicep Curls", "duration": 15})
    resp = client.get("/search?name=bicep")
    assert resp.status_code == 200
    assert resp.json["count"] == 1
    assert resp.json["items"][0]["workout"] == "Bicep Curls"


def test_search_workouts_not_found():
    client = app.test_client()
    client.post("/workouts", json={"workout": "Pullups", "duration": 10})
    resp = client.get("/search?name=deadlift")
    assert resp.status_code == 200
    assert resp.json["count"] == 0
