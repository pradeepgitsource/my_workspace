import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.booking.booking_controller import router
from app.core.user_models import User
from models import Booking
from schemas import BookingCreate

# Create test app
app = FastAPI()
app.include_router(router)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_user():
    return User(id=1, username="testuser", email="test@example.com", hashed_password="hashed")

@pytest.fixture
def sample_booking():
    return Booking(
        booking_id="BK123",
        flight_id="FL123",
        passenger_id="PS123",
        seat_number="12A"
    )

@patch('app.booking.booking_controller.get_current_active_user')
@patch('app.booking.booking_controller.get_booking_service')
def test_create_booking_success(mock_get_service, mock_get_user, client, mock_user, sample_booking):
    # Arrange
    mock_get_user.return_value = mock_user
    mock_service = Mock()
    mock_service.create_booking = AsyncMock(return_value=sample_booking)
    mock_get_service.return_value = mock_service
    
    booking_data = {
        "flight_id": "FL123",
        "passenger_id": "PS123",
        "seat_number": "12A"
    }
    
    # Act
    response = client.post("/api/bookings", json=booking_data)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["booking_id"] == "BK123"

@patch('app.booking.booking_controller.get_current_active_user')
@patch('app.booking.booking_controller.get_booking_service')
def test_get_booking_success(mock_get_service, mock_get_user, client, mock_user, sample_booking):
    # Arrange
    mock_get_user.return_value = mock_user
    mock_service = Mock()
    mock_service.get_booking_by_id = AsyncMock(return_value=sample_booking)
    mock_get_service.return_value = mock_service
    
    # Act
    response = client.get("/api/bookings/BK123")
    
    # Assert
    assert response.status_code == 200
    assert response.json()["booking_id"] == "BK123"

@patch('app.booking.booking_controller.get_current_active_user')
@patch('app.booking.booking_controller.get_booking_service')
def test_cancel_booking_success(mock_get_service, mock_get_user, client, mock_user):
    # Arrange
    mock_get_user.return_value = mock_user
    mock_service = Mock()
    mock_service.cancel_booking = AsyncMock()
    mock_get_service.return_value = mock_service
    
    # Act
    response = client.delete("/api/bookings/BK123")
    
    # Assert
    assert response.status_code == 204

def test_create_booking_validation_error(client):
    # Act
    response = client.post("/api/bookings", json={})
    
    # Assert
    assert response.status_code == 422

@patch('app.booking.booking_controller.get_current_active_user')
@patch('app.booking.booking_controller.get_booking_service')
def test_create_booking_service_error(mock_get_service, mock_get_user, client, mock_user):
    # Arrange
    mock_get_user.return_value = mock_user
    mock_service = Mock()
    mock_service.create_booking = AsyncMock(side_effect=Exception("Service error"))
    mock_get_service.return_value = mock_service
    
    booking_data = {
        "flight_id": "FL123",
        "passenger_id": "PS123",
        "seat_number": "12A"
    }
    
    # Act
    response = client.post("/api/bookings", json=booking_data)
    
    # Assert
    assert response.status_code == 500