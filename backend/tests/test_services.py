import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timedelta
from fastapi import HTTPException

from app.services.flight_service import FlightService
from app.services.passenger_service import PassengerService
from app.services.booking_service import BookingService
from app.core.schemas import FlightCreate, PassengerCreate, BookingCreate, CheckinRequest
from app.core.models import Flight, Passenger, Booking

@pytest.mark.asyncio
async def test_flight_service_create_success():
    """Test successful flight creation."""
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = None  # Flight doesn't exist
    mock_repo.create.return_value = Flight(
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
    
    service = FlightService(mock_repo)
    
    flight_data = FlightCreate(
        flight_id="TEST123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180
    )
    
    result = await service.create_flight(flight_data)
    
    assert result.flight_id == "TEST123"
    mock_repo.get_by_id.assert_called_once_with("TEST123")
    mock_repo.create.assert_called_once()

@pytest.mark.asyncio
async def test_flight_service_create_duplicate():
    """Test flight creation with duplicate ID."""
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = Flight(
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
    
    service = FlightService(mock_repo)
    
    flight_data = FlightCreate(
        flight_id="TEST123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await service.create_flight(flight_data)
    
    assert exc_info.value.status_code == 409

@pytest.mark.asyncio
async def test_flight_service_get_not_found():
    """Test getting non-existent flight."""
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = None
    
    service = FlightService(mock_repo)
    
    with pytest.raises(HTTPException) as exc_info:
        await service.get_flight("NONEXISTENT")
    
    assert exc_info.value.status_code == 404

@pytest.mark.asyncio
async def test_passenger_service_create_success():
    """Test successful passenger creation."""
    mock_repo = AsyncMock()
    mock_repo.get_by_email.return_value = None  # Email doesn't exist
    mock_repo.create.return_value = Passenger(
        passenger_id="P123",
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        phone="+1234567890",
        date_of_birth="1990-01-15"
    )
    
    service = PassengerService(mock_repo)
    
    passenger_data = PassengerCreate(
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        phone="+1234567890",
        date_of_birth="1990-01-15"
    )
    
    result = await service.create_passenger(passenger_data)
    
    assert result.first_name == "John"
    mock_repo.get_by_email.assert_called_once_with("john.doe@test.com")
    mock_repo.create.assert_called_once()

@pytest.mark.asyncio
async def test_passenger_service_create_duplicate_email():
    """Test passenger creation with duplicate email."""
    mock_repo = AsyncMock()
    mock_repo.get_by_email.return_value = Passenger(
        passenger_id="P123",
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        phone="+1234567890",
        date_of_birth="1990-01-15"
    )
    
    service = PassengerService(mock_repo)
    
    passenger_data = PassengerCreate(
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        phone="+1234567890",
        date_of_birth="1990-01-15"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await service.create_passenger(passenger_data)
    
    assert exc_info.value.status_code == 409

@pytest.mark.asyncio
async def test_booking_service_create_success():
    """Test successful booking creation."""
    mock_booking_repo = AsyncMock()
    mock_flight_repo = AsyncMock()
    mock_passenger_repo = AsyncMock()
    mock_checkin_repo = AsyncMock()
    
    # Mock flight exists with available seats
    mock_flight_repo.get_by_id.return_value = Flight(
        flight_id="TEST123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180,
        available_seats=10,
        status="scheduled"
    )
    
    # Mock passenger exists
    mock_passenger_repo.get_by_id.return_value = Passenger(
        passenger_id="P123",
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        phone="+1234567890",
        date_of_birth="1990-01-15"
    )
    
    # Mock booking creation
    mock_booking_repo.create.return_value = Booking(
        booking_id="B123",
        flight_id="TEST123",
        passenger_id="P123",
        seat_number="12A",
        booking_status="confirmed",
        booking_date=datetime.utcnow()
    )
    
    service = BookingService(mock_booking_repo, mock_flight_repo, mock_passenger_repo, mock_checkin_repo)
    
    booking_data = BookingCreate(
        flight_id="TEST123",
        passenger_id="P123",
        seat_number="12A"
    )
    
    result = await service.create_booking(booking_data)
    
    assert result.flight_id == "TEST123"
    assert result.seat_number == "12A"
    mock_flight_repo.update_available_seats.assert_called_once_with("TEST123", -1)

@pytest.mark.asyncio
async def test_booking_service_create_no_seats():
    """Test booking creation with no available seats."""
    mock_booking_repo = AsyncMock()
    mock_flight_repo = AsyncMock()
    mock_passenger_repo = AsyncMock()
    mock_checkin_repo = AsyncMock()
    
    # Mock flight exists but no available seats
    mock_flight_repo.get_by_id.return_value = Flight(
        flight_id="TEST123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180,
        available_seats=0,
        status="scheduled"
    )
    
    mock_passenger_repo.get_by_id.return_value = Passenger(
        passenger_id="P123",
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        phone="+1234567890",
        date_of_birth="1990-01-15"
    )
    
    service = BookingService(mock_booking_repo, mock_flight_repo, mock_passenger_repo, mock_checkin_repo)
    
    booking_data = BookingCreate(
        flight_id="TEST123",
        passenger_id="P123",
        seat_number="12A"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await service.create_booking(booking_data)
    
    assert exc_info.value.status_code == 409

@pytest.mark.asyncio
async def test_booking_service_checkin_success():
    """Test successful check-in."""
    mock_booking_repo = AsyncMock()
    mock_flight_repo = AsyncMock()
    mock_passenger_repo = AsyncMock()
    mock_checkin_repo = AsyncMock()
    
    # Mock booking and flight
    booking = Booking(
        booking_id="B123",
        flight_id="TEST123",
        passenger_id="P123",
        seat_number="12A",
        booking_status="confirmed",
        booking_date=datetime.utcnow()
    )
    
    flight = Flight(
        flight_id="TEST123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180,
        available_seats=179,
        status="scheduled"
    )
    
    mock_booking_repo.get_with_flight.return_value = (booking, flight)
    mock_checkin_repo.get_by_booking_id.return_value = None  # Not checked in yet
    
    from app.core.models import CheckinRecord
    mock_checkin_repo.create.return_value = CheckinRecord(
        checkin_id="C123",
        booking_id="B123",
        boarding_pass_number="TEST123-B123-20241226120000",
        gate_number="A1",
        boarding_group="B",
        checkin_time=datetime.utcnow()
    )
    
    service = BookingService(mock_booking_repo, mock_flight_repo, mock_passenger_repo, mock_checkin_repo)
    
    checkin_data = CheckinRequest(
        booking_id="B123",
        passenger_id="P123"
    )
    
    result = await service.checkin(checkin_data)
    
    assert result.flight_id == "TEST123"
    assert result.seat_number == "12A"
    assert result.boarding_group == "B"

@pytest.mark.asyncio
async def test_booking_service_checkin_already_checked_in():
    """Test check-in when already checked in."""
    mock_booking_repo = AsyncMock()
    mock_flight_repo = AsyncMock()
    mock_passenger_repo = AsyncMock()
    mock_checkin_repo = AsyncMock()
    
    booking = Booking(
        booking_id="B123",
        flight_id="TEST123",
        passenger_id="P123",
        seat_number="12A",
        booking_status="confirmed",
        booking_date=datetime.utcnow()
    )
    
    flight = Flight(
        flight_id="TEST123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180,
        available_seats=179,
        status="scheduled"
    )
    
    mock_booking_repo.get_with_flight.return_value = (booking, flight)
    
    # Already checked in
    from app.core.models import CheckinRecord
    mock_checkin_repo.get_by_booking_id.return_value = CheckinRecord(
        checkin_id="C123",
        booking_id="B123",
        boarding_pass_number="TEST123-B123-20241226120000",
        gate_number="A1",
        boarding_group="B",
        checkin_time=datetime.utcnow()
    )
    
    service = BookingService(mock_booking_repo, mock_flight_repo, mock_passenger_repo, mock_checkin_repo)
    
    checkin_data = CheckinRequest(
        booking_id="B123",
        passenger_id="P123"
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await service.checkin(checkin_data)
    
    assert exc_info.value.status_code == 409