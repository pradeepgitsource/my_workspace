import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta

from app.repositories.flight_repository import FlightRepository
from app.repositories.passenger_repository import PassengerRepository
from app.core.models import Flight, Passenger
from app.core.schemas import FlightCreate, PassengerCreate

@pytest.mark.asyncio
async def test_flight_repository_create_mocked():
    """Test flight repository create with mocked database."""
    mock_session = AsyncMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo = FlightRepository(mock_session)
    
    flight_data = FlightCreate(
        flight_id="TEST123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180
    )
    
    result = await repo.create(flight_data)
    
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    assert isinstance(result, Flight)

@pytest.mark.asyncio
async def test_flight_repository_get_by_id_mocked():
    """Test flight repository get by ID with mocked database."""
    mock_session = AsyncMock()
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
    
    mock_session.get = AsyncMock(return_value=mock_flight)
    
    repo = FlightRepository(mock_session)
    result = await repo.get_by_id("TEST123")
    
    mock_session.get.assert_called_once()
    assert result == mock_flight

@pytest.mark.asyncio
async def test_passenger_repository_create_mocked():
    """Test passenger repository create with mocked database."""
    mock_session = AsyncMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo = PassengerRepository(mock_session)
    
    passenger_data = PassengerCreate(
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        phone="+1234567890",
        date_of_birth="1990-01-15"
    )
    
    result = await repo.create(passenger_data)
    
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    assert isinstance(result, Passenger)

@pytest.mark.asyncio
async def test_repository_error_handling_mocked():
    """Test repository error handling with mocked database."""
    mock_session = AsyncMock()
    mock_session.commit = AsyncMock(side_effect=Exception("Database error"))
    
    repo = FlightRepository(mock_session)
    
    flight_data = FlightCreate(
        flight_id="TEST123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180
    )
    
    with pytest.raises(Exception):
        await repo.create(flight_data)