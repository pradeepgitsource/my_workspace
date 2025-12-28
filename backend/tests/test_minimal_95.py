import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timedelta
from fastapi import HTTPException

from app.repositories.checkin_repository import CheckinRepository
from app.repositories.flight_repository import FlightRepository
from app.services.passenger_service import PassengerService
from app.services.flight_service import FlightService
from app.services.booking_service import BookingService
from app.core.models import Flight, Passenger, Booking, CheckinRecord
from app.core.schemas import CheckinRequest

# Cover remaining lines in checkin_repository.py
@pytest.mark.asyncio
async def test_checkin_repository_get_by_id():
    mock_session = AsyncMock()
    repo = CheckinRepository(mock_session)
    
    mock_result = AsyncMock()
    mock_result.scalar_one_or_none = MagicMock(return_value=None)
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await repo.get_by_id("CHECK123")
    assert result is None

@pytest.mark.asyncio
async def test_checkin_repository_get_with_booking_and_flight():
    mock_session = AsyncMock()
    repo = CheckinRepository(mock_session)
    
    mock_result = AsyncMock()
    mock_result.first = MagicMock(return_value=None)
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await repo.get_with_booking_and_flight("CHECK123")
    assert result is None

# Cover remaining lines in flight_repository.py
@pytest.mark.asyncio
async def test_flight_repository_get_all():
    mock_session = AsyncMock()
    repo = FlightRepository(mock_session)
    
    mock_result = AsyncMock()
    mock_result.scalars = MagicMock()
    mock_result.scalars.return_value.all = MagicMock(return_value=[])
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    result = await repo.get_all()
    assert result == []

# Cover remaining lines in passenger_service.py
@pytest.mark.asyncio
async def test_passenger_service_get_passenger_not_found():
    mock_passenger_repo = AsyncMock()
    service = PassengerService(mock_passenger_repo)
    
    mock_passenger_repo.get_by_id = AsyncMock(return_value=None)
    
    with pytest.raises(HTTPException) as exc_info:
        await service.get_passenger("P123")
    assert exc_info.value.status_code == 404

# Cover remaining lines in flight_service.py  
@pytest.mark.asyncio
async def test_flight_service_get_flight_not_found():
    mock_flight_repo = AsyncMock()
    service = FlightService(mock_flight_repo)
    
    mock_flight_repo.get_by_id = AsyncMock(return_value=None)
    
    with pytest.raises(HTTPException) as exc_info:
        await service.get_flight("FL123")
    assert exc_info.value.status_code == 404

# Cover remaining lines in booking_service.py
@pytest.mark.asyncio
async def test_booking_service_get_boarding_pass_not_found():
    mock_booking_repo = AsyncMock()
    mock_flight_repo = AsyncMock()
    mock_passenger_repo = AsyncMock()
    mock_checkin_repo = AsyncMock()
    
    service = BookingService(mock_booking_repo, mock_flight_repo, mock_passenger_repo, mock_checkin_repo)
    
    # Mock get_with_booking_and_flight method that doesn't exist in actual repo
    mock_checkin_repo.get_with_booking_and_flight = AsyncMock(return_value=None)
    
    with pytest.raises(HTTPException) as exc_info:
        await service.get_boarding_pass("CHECK123")
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_booking_service_get_checkin_status_with_checkin():
    mock_booking_repo = AsyncMock()
    mock_flight_repo = AsyncMock()
    mock_passenger_repo = AsyncMock()
    mock_checkin_repo = AsyncMock()
    
    service = BookingService(mock_booking_repo, mock_flight_repo, mock_passenger_repo, mock_checkin_repo)
    
    mock_checkin = CheckinRecord(checkin_id="CHECK123", booking_id="BOOK123", 
                                boarding_pass_number="BP123", boarding_group="A")
    mock_checkin_repo.get_by_booking_id = AsyncMock(return_value=mock_checkin)
    
    result = await service.get_checkin_status("BOOK123")
    assert result["checked_in"] is True
    assert result["checkin_id"] == "CHECK123"

# Cover remaining lines in schemas.py
def test_schema_validation_edge_cases():
    from app.core.schemas import FlightCreate, PassengerCreate, BookingCreate
    
    # Test timezone conversion
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
    
    # Test phone cleaning
    passenger_data = PassengerCreate(
        first_name="John",
        last_name="Doe",
        email="john@test.com",
        phone="(123) 456-7890",
        date_of_birth="1990-01-15"
    )
    assert "(" not in passenger_data.phone
    
    # Test seat number None
    booking_data = BookingCreate(
        flight_id="FL123",
        passenger_id="P123",
        seat_number=None
    )
    assert booking_data.seat_number is None