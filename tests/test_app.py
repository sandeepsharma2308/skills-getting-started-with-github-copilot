import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200 or response.status_code == 400
    # Should be in participants if signup succeeded
    get_resp = client.get("/activities")
    participants = get_resp.json()[activity]["participants"]
    assert email in participants
    # Unregister
    response = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert response.status_code == 200
    # Should not be in participants
    get_resp = client.get("/activities")
    participants = get_resp.json()[activity]["participants"]
    assert email not in participants

def test_signup_duplicate():
    activity = "Basketball"
    email = "alex@mergington.edu"  # already registered
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_unregister_not_registered():
    activity = "Tennis Club"
    email = "notregistered@mergington.edu"
    response = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
