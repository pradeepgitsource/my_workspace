import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta
from httpx import AsyncClient, ASGITransport

from main_refactored import app
from app.core.models import Flight, Passenger, Booking

@pytest.mark.asyncio
async def test_create_flight_endpoint_mocked():
    """Test flight creation endpoint with mocked services."""
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": (datetime.utcnow() + timedelta(hours=6)).isoformat(),
        "arrival_time": (datetime.utcnow() + timedelta(hours=12)).isoformat(),
        "aircraft_type": "Boeing 737",
        "total_seats": 180
    }
    
    mock_flight = Flight(
        flight_id="TEST123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180,
        available_seats=180,
        status="scheduled"
    )
    
    with patch('app.services.flight_service.FlightService.create_flight', return_value=mock_flight):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/api/flights", json=flight_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["flight_id"] == "TEST123"

@pytest.mark.asyncio
async def test_get_flights_endpoint_mocked():
    """Test get flights endpoint with mocked services."""
    mock_flights = [
        Flight(
            flight_id="TEST123",
            departure_airport="JFK",
            arrival_airport="LAX",
            departure_time=datetime.utcnow() + timedelta(hours=6),
            arrival_time=datetime.utcnow() + timedelta(hours=12),
            aircraft_type="Boeing 737",
            total_seats=180,
            available_seats=150,
            status="scheduled"
        )
    ]
    
    with patch('app.services.flight_service.FlightService.get_all_flights', return_value=mock_flights):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/flights")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["flight_id"] == "TEST123"

@pytest.mark.asyncio
async def test_create_passenger_endpoint_mocked():
    """Test passenger creation endpoint with mocked services."""
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    
    mock_passenger = Passenger(
        passenger_id="P123",
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        phone="+1234567890",
        date_of_birth="1990-01-15"
    )
    
    with patch('app.services.passenger_service.PassengerService.create_passenger', return_value=mock_passenger):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/api/passengers", json=passenger_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"

@pytest.mark.asyncio
async def test_health_endpoint():
    """Test health check endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["status"] == "running"