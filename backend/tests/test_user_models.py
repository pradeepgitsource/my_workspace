import pytest
from pydantic import ValidationError
from backend.app.core.user_models import User
from backend.app.core.auth_schemas import UserCreate, UserResponse, Token

def test_user_model():
    user = User(
        id=1,
        username="testuser",
        email="test@test.com",
        hashed_password="hashed_password"
    )
    assert user.id == 1
    assert user.username == "testuser"
    assert user.email == "test@test.com"
    assert user.hashed_password == "hashed_password"

def test_user_create_schema_valid():
    user_data = {
        "username": "testuser",
        "email": "test@test.com",
        "password": "testpass123"
    }
    user = UserCreate(**user_data)
    assert user.username == "testuser"
    assert user.email == "test@test.com"
    assert user.password == "testpass123"

def test_user_create_schema_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="invalid_email",
            password="testpass123"
        )

def test_user_create_schema_short_password():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="test@test.com",
            password="123"
        )

def test_user_create_schema_empty_username():
    with pytest.raises(ValidationError):
        UserCreate(
            username="",
            email="test@test.com",
            password="testpass123"
        )

def test_user_response_schema():
    user_data = {
        "id": 1,
        "username": "testuser",
        "email": "test@test.com"
    }
    user = UserResponse(**user_data)
    assert user.id == 1
    assert user.username == "testuser"
    assert user.email == "test@test.com"

def test_token_schema():
    token_data = {
        "access_token": "test_token",
        "token_type": "bearer"
    }
    token = Token(**token_data)
    assert token.access_token == "test_token"
    assert token.token_type == "bearer"

def test_user_response_from_user_model():
    user = User(
        id=1,
        username="testuser",
        email="test@test.com",
        hashed_password="hashed"
    )
    user_response = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email
    )
    assert user_response.id == 1
    assert user_response.username == "testuser"
    assert user_response.email == "test@test.com"