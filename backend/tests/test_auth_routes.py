import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
from backend.main_refactored import app
from backend.app.core.user_models import User

client = TestClient(app)

@patch('backend.app.routes.auth.get_user_by_username')
@patch('backend.app.routes.auth.get_password_hash')
@patch('backend.app.routes.auth.create_user')
def test_register_success(mock_create_user, mock_hash, mock_get_user):
    mock_get_user.return_value = None
    mock_hash.return_value = "hashed_password"
    mock_create_user.return_value = User(id=1, username="testuser", email="test@test.com", hashed_password="hashed")
    
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "testpass123"
    })
    
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

@patch('backend.app.routes.auth.get_user_by_username')
def test_register_user_exists(mock_get_user):
    mock_get_user.return_value = User(id=1, username="testuser", email="test@test.com", hashed_password="hashed")
    
    response = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "testpass123"
    })
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

@patch('backend.app.routes.auth.get_user_by_username')
@patch('backend.app.routes.auth.verify_password')
@patch('backend.app.routes.auth.create_access_token')
def test_login_success(mock_create_token, mock_verify, mock_get_user):
    mock_user = User(id=1, username="testuser", email="test@test.com", hashed_password="hashed")
    mock_get_user.return_value = mock_user
    mock_verify.return_value = True
    mock_create_token.return_value = "test_token"
    
    response = client.post("/auth/token", data={
        "username": "testuser",
        "password": "testpass123"
    })
    
    assert response.status_code == 200
    assert response.json()["access_token"] == "test_token"
    assert response.json()["token_type"] == "bearer"

@patch('backend.app.routes.auth.get_user_by_username')
def test_login_user_not_found(mock_get_user):
    mock_get_user.return_value = None
    
    response = client.post("/auth/token", data={
        "username": "nonexistent",
        "password": "testpass123"
    })
    
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

@patch('backend.app.routes.auth.get_user_by_username')
@patch('backend.app.routes.auth.verify_password')
def test_login_wrong_password(mock_verify, mock_get_user):
    mock_user = User(id=1, username="testuser", email="test@test.com", hashed_password="hashed")
    mock_get_user.return_value = mock_user
    mock_verify.return_value = False
    
    response = client.post("/auth/token", data={
        "username": "testuser",
        "password": "wrongpass"
    })
    
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

def test_register_invalid_data():
    response = client.post("/auth/register", json={
        "username": "",
        "email": "invalid_email",
        "password": "123"
    })
    
    assert response.status_code == 422

def test_login_missing_data():
    response = client.post("/auth/token", data={
        "username": "testuser"
    })
    
    assert response.status_code == 422