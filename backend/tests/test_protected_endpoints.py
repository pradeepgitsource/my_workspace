import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.main_refactored import app
from backend.app.core.user_models import User

client = TestClient(app)

def test_protected_endpoint_without_token():
    response = client.get("/api/flights")
    assert response.status_code == 401

def test_protected_endpoint_invalid_token():
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/flights", headers=headers)
    assert response.status_code == 401

@patch('backend.app.core.dependencies.get_current_user')
def test_protected_endpoint_valid_token(mock_get_user):
    mock_user = User(id=1, username="testuser", email="test@test.com", hashed_password="hashed")
    mock_get_user.return_value = mock_user
    
    headers = {"Authorization": "Bearer valid_token"}
    response = client.get("/api/flights", headers=headers)
    assert response.status_code == 200

@patch('backend.app.core.dependencies.get_current_user')
def test_checkin_endpoint_protected(mock_get_user):
    mock_user = User(id=1, username="testuser", email="test@test.com", hashed_password="hashed")
    mock_get_user.return_value = mock_user
    
    headers = {"Authorization": "Bearer valid_token"}
    response = client.post("/api/checkin", 
                          json={"flight_number": "AA123", "passenger_name": "John Doe"},
                          headers=headers)
    assert response.status_code == 200

def test_checkin_endpoint_without_auth():
    response = client.post("/api/checkin", 
                          json={"flight_number": "AA123", "passenger_name": "John Doe"})
    assert response.status_code == 401

@patch('backend.app.core.dependencies.get_current_user')
def test_health_endpoint_not_protected(mock_get_user):
    # Health endpoint should not require authentication
    response = client.get("/health")
    assert response.status_code == 200
    # Ensure get_current_user was not called for health endpoint
    mock_get_user.assert_not_called()

def test_auth_endpoints_not_protected():
    # Register endpoint should not require authentication
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@test.com", 
        "password": "testpass123"
    })
    # Should not be 401 (may be 400 due to validation or other business logic)
    assert response.status_code != 401
    
    # Login endpoint should not require authentication
    response = client.post("/auth/token", data={
        "username": "testuser",
        "password": "testpass123"
    })
    # Should not be 401 (may be other status due to business logic)
    assert response.status_code != 401