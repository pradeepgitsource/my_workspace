import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timedelta
from fastapi import HTTPException

from app.repositories.booking_repository import BookingRepository
from app.repositories.checkin_repository import CheckinRepository
from app.repositories.flight_repository import FlightRepository
from app.services.booking_service import BookingService
from app.services.passenger_service import PassengerService
from app.services.flight_service import FlightService
from app.core.models import Flight, Passenger, Booking, CheckinRecord
from app.core.schemas import BookingCreate, CheckinRequest

# Cover missing lines in booking_repository.py (lines 13-21, 24-25, 36-41)
@pytest.mark.asyncio
async def test_booking_repository_create_real():
    mock_session = AsyncMock()
    repo = BookingRepository(mock_session)
    
    booking_data = BookingCreate(flight_id="FL123", passenger_id="P123")
    result = await repo.create(booking_data, "12A")
    
    assert result.flight_id == "FL123"
    assert result.passenger_id == "P123"
    assert result.seat_number == "12A"

@pytest.mark.asyncio
async def test_booking_repository_get_by_id_real():
    mock_session = AsyncMock()
    repo = BookingRepository(mock_session)
    
    mock_result = AsyncMock()
    mock_result.scalar_one_or_none = MagicMock(return_value=None)
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    await repo.get_by_id("BOOK123")
    mock_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_booking_repository_update_status_real():
    mock_session = AsyncMock()
    repo = BookingRepository(mock_session)
    
    await repo.update_status("BOOK123", "cancelled")
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()

# Cover missing lines in checkin_repository.py (lines 9, 13-22, 25-26, 29-30, 33-39)
@pytest.mark.asyncio
async def test_checkin_repository_create_real():
    mock_session = AsyncMock()
    repo = CheckinRepository(mock_session)
    
    result = await repo.create("BOOK123", "BP123", "A1", "A")
    
    assert result.booking_id == "BOOK123"
    assert result.boarding_pass_number == "BP123"
    assert result.gate_number == "A1"
    assert result.boarding_group == "A"

@pytest.mark.asyncio
async def test_checkin_repository_get_by_booking_id_real():
    mock_session = AsyncMock()
    repo = CheckinRepository(mock_session)
    
    mock_result = AsyncMock()
    mock_result.scalar_one_or_none = MagicMock(return_value=None)
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    await repo.get_by_booking_id("BOOK123")
    mock_session.execute.assert_called_once()

# Cover missing lines in flight_repository.py (lines 33-34, 37-42)
@pytest.mark.asyncio
async def test_flight_repository_update_seats_real():
    mock_session = AsyncMock()
    repo = FlightRepository(mock_session)
    
    await repo.update_available_seats("FL123", -1)
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_called_once()

# Cover missing lines in booking_service.py (lines 23, 28, 48, 54, 66, 72, 82, 106-112, 123-124)
@pytest.mark.asyncio
async def test_booking_service_missing_lines():
    mock_booking_repo = AsyncMock()
    mock_flight_repo = AsyncMock()
    mock_passenger_repo = AsyncMock()
    mock_checkin_repo = AsyncMock()
    
    service = BookingService(mock_booking_repo, mock_flight_repo, mock_passenger_repo, mock_checkin_repo)
    
    # Line 23: Flight not found
    mock_flight_repo.get_by_id = AsyncMock(return_value=None)
    booking_data = BookingCreate(flight_id="FL123", passenger_id="P123")
    
    with pytest.raises(HTTPException):
        await service.create_booking(booking_data)
    
    # Line 28: Passenger not found
    mock_flight = Flight(flight_id="FL123", departure_airport="JFK", arrival_airport="LAX",
                        departure_time=datetime.utcnow() + timedelta(hours=6),
                        arrival_time=datetime.utcnow() + timedelta(hours=12),
                        aircraft_type="Boeing 737", total_seats=180, available_seats=180)
    mock_flight_repo.get_by_id = AsyncMock(return_value=mock_flight)
    mock_passenger_repo.get_by_id = AsyncMock(return_value=None)
    
    with pytest.raises(HTTPException):
        await service.create_booking(booking_data)
    
    # Line 48: Booking not found in get_booking
    mock_booking_repo.get_by_id = AsyncMock(return_value=None)
    
    with pytest.raises(HTTPException):
        await service.get_booking("BOOK123")
    
    # Line 54: Booking not found in cancel_booking
    with pytest.raises(HTTPException):
        await service.cancel_booking("BOOK123")
    
    # Line 66: Booking not found in checkin
    mock_booking_repo.get_with_flight = AsyncMock(return_value=None)
    checkin_data = CheckinRequest(booking_id="BOOK123", passenger_id="P123")
    
    with pytest.raises(HTTPException):
        await service.checkin(checkin_data)
    
    # Line 72: Passenger ID mismatch
    mock_booking = Booking(booking_id="BOOK123", flight_id="FL123", passenger_id="P456", 
                          seat_number="12A", booking_status="confirmed")
    mock_booking_repo.get_with_flight = AsyncMock(return_value=(mock_booking, mock_flight))
    
    with pytest.raises(HTTPException):
        await service.checkin(checkin_data)
    
    # Line 82: Check-in window invalid
    mock_booking.passenger_id = "P123"
    mock_flight.departure_time = datetime.utcnow() + timedelta(hours=30)  # Too far
    mock_checkin_repo.get_by_booking_id = AsyncMock(return_value=None)
    
    with pytest.raises(HTTPException):
        await service.checkin(checkin_data)

# Cover missing lines in passenger_service.py (lines 26, 34-42)
@pytest.mark.asyncio
async def test_passenger_service_missing_lines():
    mock_passenger_repo = AsyncMock()
    service = PassengerService(mock_passenger_repo)
    
    # Line 26: Passenger not found in get_passenger
    mock_passenger_repo.get_by_id = AsyncMock(return_value=None)
    
    with pytest.raises(HTTPException):
        await service.get_passenger("P123")

# Cover missing lines in flight_service.py (lines 31, 34-35)
@pytest.mark.asyncio
async def test_flight_service_missing_lines():
    mock_flight_repo = AsyncMock()
    service = FlightService(mock_flight_repo)
    
    # Line 31: Flight not found
    mock_flight_repo.get_by_id = AsyncMock(return_value=None)
    
    with pytest.raises(HTTPException):
        await service.get_flight("FL123")

# Cover missing lines in schemas.py (lines 26, 34, 42, 45, 109)
def test_schema_validation_missing_lines():
    from app.core.schemas import FlightCreate, PassengerCreate, BookingCreate
    
    # Line 26: Invalid departure time (past)
    with pytest.raises(ValueError):
        FlightCreate(
            flight_id="FL123",
            departure_airport="JFK", 
            arrival_airport="LAX",
            departure_time=datetime.utcnow() - timedelta(hours=1),
            arrival_time=datetime.utcnow() + timedelta(hours=6),
            aircraft_type="Boeing 737",
            total_seats=180
        )
    
    # Line 34: Invalid arrival time (before departure)
    with pytest.raises(ValueError):
        FlightCreate(
            flight_id="FL123",
            departure_airport="JFK",
            arrival_airport="LAX", 
            departure_time=datetime.utcnow() + timedelta(hours=6),
            arrival_time=datetime.utcnow() + timedelta(hours=3),
            aircraft_type="Boeing 737",
            total_seats=180
        )
    
    # Line 42: Invalid name length
    with pytest.raises(ValueError):
        PassengerCreate(
            first_name="A",
            last_name="Doe",
            email="test@test.com",
            phone="+1234567890", 
            date_of_birth="1990-01-15"
        )
    
    # Line 45: Invalid phone format
    with pytest.raises(ValueError):
        PassengerCreate(
            first_name="John",
            last_name="Doe", 
            email="test@test.com",
            phone="invalid",
            date_of_birth="1990-01-15"
        )
    
    # Line 109: Invalid seat format
    with pytest.raises(ValueError):
        BookingCreate(
            flight_id="FL123",
            passenger_id="P123",
            seat_number="999Z"
        )

# Cover missing line in database.py (line 19)
@pytest.mark.asyncio
async def test_database_close():
    from app.core.database import get_db
    
    db_gen = get_db()
    db = await db_gen.__anext__()
    try:
        await db_gen.__anext__()
    except StopAsyncIteration:
        pass  # Expected

# Cover missing line in models.py (line 10)
def test_models_generate_uuid():
    from app.core.models import generate_uuid
    
    uuid1 = generate_uuid()
    uuid2 = generate_uuid()
    assert uuid1 != uuid2
    assert len(uuid1) == 36