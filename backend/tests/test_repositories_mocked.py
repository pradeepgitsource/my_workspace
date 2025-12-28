import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta

from app.repositories.flight_repository import FlightRepository
from app.repositories.passenger_repository import PassengerRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.checkin_repository import CheckinRepository
from app.core.models import Flight, Passenger, Booking, CheckinRecord

@pytest.mark.asyncio
async def test_flight_repository_create_mocked():
    """Test flight repository create with mocked database."""
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
    
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo = FlightRepository(mock_session)
    
    with patch.object(Flight, '__init__', return_value=None):
        with patch('app.repositories.flight_repository.Flight', return_value=mock_flight):
            result = await repo.create({
                "flight_id": "TEST123",
                "departure_airport": "JFK",
                "arrival_airport": "LAX",
                "departure_time": datetime.utcnow() + timedelta(hours=6),
                "arrival_time": datetime.utcnow() + timedelta(hours=12),
                "aircraft_type": "Boeing 737",
                "total_seats": 180,
                "available_seats": 180,
                "status": "scheduled"
            })
    
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

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
    
    mock_session.get.assert_called_once_with(Flight, "TEST123")
    assert result == mock_flight

@pytest.mark.asyncio
async def test_passenger_repository_create_mocked():
    """Test passenger repository create with mocked database."""
    mock_session = AsyncMock()
    mock_passenger = Passenger(
        passenger_id="P123",
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        phone="+1234567890",
        date_of_birth="1990-01-15"
    )
    
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo = PassengerRepository(mock_session)
    
    with patch.object(Passenger, '__init__', return_value=None):
        with patch('app.repositories.passenger_repository.Passenger', return_value=mock_passenger):
            result = await repo.create({
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@test.com",
                "phone": "+1234567890",
                "date_of_birth": "1990-01-15"
            })
    
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_booking_repository_create_mocked():
    """Test booking repository create with mocked database."""
    mock_session = AsyncMock()
    mock_booking = Booking(
        booking_id="B123",
        flight_id="TEST123",
        passenger_id="P123",
        seat_number="12A",
        booking_status="confirmed",
        booking_date=datetime.utcnow()
    )
    
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo = BookingRepository(mock_session)
    
    with patch.object(Booking, '__init__', return_value=None):
        with patch('app.repositories.booking_repository.Booking', return_value=mock_booking):
            result = await repo.create({
                "flight_id": "TEST123",
                "passenger_id": "P123",
                "seat_number": "12A",
                "booking_status": "confirmed"
            })
    
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_checkin_repository_create_mocked():
    """Test checkin repository create with mocked database."""
    mock_session = AsyncMock()
    mock_checkin = CheckinRecord(
        checkin_id="C123",
        booking_id="B123",
        boarding_pass_number="TEST123-B123-20241226",
        gate_number="A1",
        boarding_group="B",
        checkin_time=datetime.utcnow()
    )
    
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    repo = CheckinRepository(mock_session)
    
    with patch.object(CheckinRecord, '__init__', return_value=None):
        with patch('app.repositories.checkin_repository.CheckinRecord', return_value=mock_checkin):
            result = await repo.create({
                "booking_id": "B123",
                "boarding_pass_number": "TEST123-B123-20241226",
                "gate_number": "A1",
                "boarding_group": "B"
            })
    
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_repository_error_handling_mocked():
    """Test repository error handling with mocked database."""
    mock_session = AsyncMock()
    mock_session.commit = AsyncMock(side_effect=Exception("Database error"))
    
    repo = FlightRepository(mock_session)
    
    with pytest.raises(Exception):
        await repo.create({
            "flight_id": "TEST123",
            "departure_airport": "JFK",
            "arrival_airport": "LAX",
            "departure_time": datetime.utcnow() + timedelta(hours=6),
            "arrival_time": datetime.utcnow() + timedelta(hours=12),
            "aircraft_type": "Boeing 737",
            "total_seats": 180
        })