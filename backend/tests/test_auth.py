import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from backend.app.core.auth import create_access_token, verify_password, get_password_hash, verify_token
from backend.app.core.dependencies import get_current_user
from backend.app.core.user_models import User
from datetime import datetime, timedelta
import jwt

def test_create_access_token():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0

def test_create_access_token_with_expires():
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data, expires_delta)
    assert isinstance(token, str)

def test_verify_password():
    password = "testpass123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpass", hashed) is False

def test_get_password_hash():
    password = "testpass123"
    hashed = get_password_hash(password)
    assert isinstance(hashed, str)
    assert hashed != password
    assert len(hashed) > 0

def test_verify_token_valid():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    payload = verify_token(token)
    assert payload["sub"] == "testuser"

def test_verify_token_invalid():
    with pytest.raises(HTTPException) as exc:
        verify_token("invalid_token")
    assert exc.value.status_code == 401

def test_verify_token_expired():
    data = {"sub": "testuser", "exp": datetime.utcnow() - timedelta(minutes=1)}
    token = jwt.encode(data, "test_secret", algorithm="HS256")
    with pytest.raises(HTTPException) as exc:
        verify_token(token)
    assert exc.value.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user_valid():
    mock_user = User(id=1, username="testuser", email="test@test.com", hashed_password="hashed")
    
    with patch('backend.app.core.dependencies.verify_token') as mock_verify, \
         patch('backend.app.core.dependencies.get_user_by_username') as mock_get_user:
        
        mock_verify.return_value = {"sub": "testuser"}
        mock_get_user.return_value = mock_user
        
        user = await get_current_user("valid_token")
        assert user.username == "testuser"

@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    with patch('backend.app.core.dependencies.verify_token') as mock_verify:
        mock_verify.side_effect = HTTPException(status_code=401)
        
        with pytest.raises(HTTPException) as exc:
            await get_current_user("invalid_token")
        assert exc.value.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user_user_not_found():
    with patch('backend.app.core.dependencies.verify_token') as mock_verify, \
         patch('backend.app.core.dependencies.get_user_by_username') as mock_get_user:
        
        mock_verify.return_value = {"sub": "testuser"}
        mock_get_user.return_value = None
        
        with pytest.raises(HTTPException) as exc:
            await get_current_user("valid_token")
        assert exc.value.status_code == 401