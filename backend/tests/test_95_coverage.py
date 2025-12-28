import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
from fastapi import HTTPException

from app.repositories.booking_repository import BookingRepository
from app.repositories.checkin_repository import CheckinRepository
from app.repositories.flight_repository import FlightRepository
from app.services.booking_service import BookingService
from app.services.passenger_service import PassengerService
from app.services.flight_service import FlightService
from app.core.models import Flight, Passenger, Booking, CheckinRecord
from app.core.schemas import BookingCreate, CheckinRequest, PassengerCreate, FlightCreate
from app.core.database import get_db

# Repository Tests
@pytest.mark.asyncio
async def test_booking_repository_all_methods():
    """Test all booking repository methods."""
    mock_session = AsyncMock()
    repo = BookingRepository(mock_session)
    
    # Test create
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    booking_data = BookingCreate(flight_id="FL123", passenger_id="P123", seat_number="12A")
    result = await repo.create(booking_data, "12A")
    
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    assert isinstance(result, Booking)
    
    # Test get_with_flight
    mock_result = AsyncMock()
    mock_result.scalar_one_or_none = MagicMock(return_value=None)
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await repo.get_with_flight("BOOK123")
    assert result is None
    
    # Test update_status
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()
    
    await repo.update_status("BOOK123", "cancelled")
    mock_session.execute.assert_called()
    mock_session.commit.assert_called()

@pytest.mark.asyncio
async def test_checkin_repository_all_methods():
    """Test all checkin repository methods."""
    mock_session = AsyncMock()
    repo = CheckinRepository(mock_session)
    
    # Test create
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    checkin_data = CheckinRequest(booking_id="BOOK123", passenger_id="P123")
    result = await repo.create(checkin_data, "BP123456", "A1", "A")
    
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    assert isinstance(result, CheckinRecord)
    
    # Test get_by_booking_id
    mock_result = AsyncMock()
    mock_result.scalar_one_or_none = MagicMock(return_value=None)
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await repo.get_by_booking_id("BOOK123")
    assert result is None

@pytest.mark.asyncio
async def test_flight_repository_all_methods():
    """Test all flight repository methods."""
    mock_session = AsyncMock()
    repo = FlightRepository(mock_session)
    
    # Test get_all
    mock_result = AsyncMock()
    mock_result.scalars = MagicMock()
    mock_result.scalars.return_value.all = MagicMock(return_value=[])
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await repo.get_all()
    assert result == []
    
    # Test update_available_seats
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()
    
    await repo.update_available_seats("FL123", -1)
    mock_session.execute.assert_called()
    mock_session.commit.assert_called()

@pytest.mark.asyncio
async def test_passenger_repository_get_by_id():
    """Test passenger repository get_by_id method."""
    mock_session = AsyncMock()
    repo = PassengerRepository(mock_session)
    
    mock_result = AsyncMock()
    mock_result.scalar_one_or_none = MagicMock(return_value=None)
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await repo.get_by_id("P123")
    assert result is None

# Service Tests
@pytest.mark.asyncio
async def test_booking_service_comprehensive():
    """Test booking service comprehensive scenarios."""
    mock_booking_repo = AsyncMock()
    mock_flight_repo = AsyncMock()
    mock_passenger_repo = AsyncMock()
    mock_checkin_repo = AsyncMock()
    
    service = BookingService(mock_booking_repo, mock_flight_repo, mock_passenger_repo, mock_checkin_repo)
    
    # Test create_booking with no available seats
    mock_flight = Flight(flight_id="FL123", departure_airport="JFK", arrival_airport="LAX", 
                        departure_time=datetime.utcnow() + timedelta(hours=6),
                        arrival_time=datetime.utcnow() + timedelta(hours=12),
                        aircraft_type="Boeing 737", total_seats=180, available_seats=0, status="scheduled")
    mock_flight_repo.get_by_id = AsyncMock(return_value=mock_flight)
    
    booking_data = BookingCreate(flight_id="FL123", passenger_id="P123", seat_number="12A")
    
    with pytest.raises(HTTPException) as exc_info:
        await service.create_booking(booking_data)
    assert exc_info.value.status_code == 400
    
    # Test checkin with passenger mismatch
    mock_booking = Booking(booking_id="BOOK123", flight_id="FL123", passenger_id="P456", 
                          seat_number="12A", booking_status="confirmed")
    mock_booking.flight = mock_flight
    mock_booking_repo.get_with_flight = AsyncMock(return_value=mock_booking)
    
    checkin_data = CheckinRequest(booking_id="BOOK123", passenger_id="P123")
    
    with pytest.raises(HTTPException) as exc_info:
        await service.checkin(checkin_data)
    assert exc_info.value.status_code == 400
    
    # Test cancel_booking
    mock_booking_repo.update_status = AsyncMock()
    mock_flight_repo.update_available_seats = AsyncMock()
    
    await service.cancel_booking("BOOK123")
    mock_booking_repo.update_status.assert_called_with("BOOK123", "cancelled")
    mock_flight_repo.update_available_seats.assert_called_with("FL123", 1)

@pytest.mark.asyncio
async def test_passenger_service_comprehensive():
    """Test passenger service comprehensive scenarios."""
    mock_passenger_repo = AsyncMock()
    service = PassengerService(mock_passenger_repo)
    
    # Test get_passenger with valid passenger
    mock_passenger = Passenger(passenger_id="P123", first_name="John", last_name="Doe",
                              email="john@test.com", phone="+1234567890", date_of_birth="1990-01-15")
    mock_passenger_repo.get_by_id = AsyncMock(return_value=mock_passenger)
    
    result = await service.get_passenger("P123")
    assert result.passenger_id == "P123"
    
    # Test get_bookings
    mock_bookings = [Booking(booking_id="BOOK123", flight_id="FL123", passenger_id="P123", 
                            seat_number="12A", booking_status="confirmed")]
    mock_passenger_repo.get_bookings = AsyncMock(return_value=mock_bookings)
    
    result = await service.get_bookings("P123")
    assert len(result) == 1

@pytest.mark.asyncio
async def test_flight_service_comprehensive():
    """Test flight service comprehensive scenarios."""
    mock_flight_repo = AsyncMock()
    service = FlightService(mock_flight_repo)
    
    # Test get_all_flights
    mock_flights = [Flight(flight_id="FL123", departure_airport="JFK", arrival_airport="LAX",
                          departure_time=datetime.utcnow() + timedelta(hours=6),
                          arrival_time=datetime.utcnow() + timedelta(hours=12),
                          aircraft_type="Boeing 737", total_seats=180, available_seats=180, status="scheduled")]
    mock_flight_repo.get_all = AsyncMock(return_value=mock_flights)
    
    result = await service.get_all_flights()
    assert len(result) == 1
    
    # Test get_flight with valid flight
    mock_flight_repo.get_by_id = AsyncMock(return_value=mock_flights[0])
    
    result = await service.get_flight("FL123")
    assert result.flight_id == "FL123"

# Schema Tests
def test_flight_create_edge_cases():
    """Test FlightCreate schema edge cases."""
    # Test timezone handling
    departure_time = datetime.now().replace(tzinfo=None) + timedelta(hours=6)
    arrival_time = departure_time + timedelta(hours=6)
    
    flight_data = FlightCreate(
        flight_id="FL123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=departure_time,
        arrival_time=arrival_time,
        aircraft_type="Boeing 737",
        total_seats=180
    )
    assert flight_data.flight_id == "FL123"

def test_passenger_create_edge_cases():
    """Test PassengerCreate schema edge cases."""
    # Test phone number cleaning
    passenger_data = PassengerCreate(
        first_name="  john  ",
        last_name="  doe  ",
        email="john@test.com",
        phone="(123) 456-7890",
        date_of_birth="1990-01-15"
    )
    assert passenger_data.first_name == "John"
    assert passenger_data.last_name == "Doe"
    assert "(" not in passenger_data.phone

def test_booking_create_edge_cases():
    """Test BookingCreate schema edge cases."""
    # Test seat number validation
    booking_data = BookingCreate(
        flight_id="FL123",
        passenger_id="P123",
        seat_number="12a"
    )
    assert booking_data.seat_number == "12A"

# Database Tests
def test_database_get_database():
    """Test database connection function."""
    db_gen = get_db()
    # Just test that it returns a generator
    assert hasattr(db_gen, '__anext__')

# Model Tests
def test_models_creation():
    """Test model creation."""
    # Test Flight model
    flight = Flight(
        flight_id="FL123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180,
        available_seats=180
    )
    assert flight.flight_id == "FL123"
    
    # Test Passenger model
    passenger = Passenger(
        passenger_id="P123",
        first_name="John",
        last_name="Doe",
        email="john@test.com",
        phone="+1234567890",
        date_of_birth="1990-01-15"
    )
    assert passenger.passenger_id == "P123"
    
    # Test Booking model
    booking = Booking(
        booking_id="BOOK123",
        flight_id="FL123",
        passenger_id="P123",
        seat_number="12A",
        booking_status="confirmed"
    )
    assert booking.booking_id == "BOOK123"
    
    # Test CheckinRecord model
    checkin = CheckinRecord(
        checkin_id="CHECK123",
        booking_id="BOOK123",
        boarding_pass_number="BP123456",
        boarding_group="A"
    )
    assert checkin.checkin_id == "CHECK123"

# Error Handling Tests
@pytest.mark.asyncio
async def test_service_error_handling():
    """Test service error handling."""
    mock_flight_repo = AsyncMock()
    mock_flight_repo.create = AsyncMock(side_effect=Exception("Database error"))
    
    service = FlightService(mock_flight_repo)
    
    flight_data = FlightCreate(
        flight_id="FL123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180
    )
    
    with pytest.raises(Exception):
        await service.create_flight(flight_data)

# Additional Schema Validation Tests
def test_schema_validation_comprehensive():
    """Test comprehensive schema validation."""
    # Test invalid flight ID length
    with pytest.raises(ValueError):
        FlightCreate(
            flight_id="",
            departure_airport="JFK",
            arrival_airport="LAX",
            departure_time=datetime.utcnow() + timedelta(hours=6),
            arrival_time=datetime.utcnow() + timedelta(hours=12),
            aircraft_type="Boeing 737",
            total_seats=180
        )
    
    # Test invalid total seats
    with pytest.raises(ValueError):
        FlightCreate(
            flight_id="FL123",
            departure_airport="JFK",
            arrival_airport="LAX",
            departure_time=datetime.utcnow() + timedelta(hours=6),
            arrival_time=datetime.utcnow() + timedelta(hours=12),
            aircraft_type="Boeing 737",
            total_seats=0
        )
    
    # Test invalid passenger name
    with pytest.raises(ValueError):
        PassengerCreate(
            first_name="A",
            last_name="Doe",
            email="john@test.com",
            phone="+1234567890",
            date_of_birth="1990-01-15"
        )
    
    # Test invalid seat number
    with pytest.raises(ValueError):
        BookingCreate(
            flight_id="FL123",
            passenger_id="P123",
            seat_number="999Z"
        )