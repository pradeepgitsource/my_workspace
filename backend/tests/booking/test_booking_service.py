import pytest
from unittest.mock import Mock, AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from app.booking.booking_service import BookingService
from models import Booking, Flight, Passenger
from schemas import BookingCreate
from app.shared.exceptions import (
    BookingNotFoundError, FlightNotFoundError, PassengerNotFoundError,
    NoSeatsAvailableError
)

@pytest.fixture
def mock_db():
    return Mock(spec=AsyncSession)

@pytest.fixture
def booking_service(mock_db):
    return BookingService(mock_db)

@pytest.fixture
def sample_booking_data():
    return BookingCreate(
        flight_id="FL123",
        passenger_id="PS123",
        seat_number="12A"
    )

@pytest.fixture
def sample_flight():
    return Flight(
        flight_id="FL123",
        departure_airport="NYC",
        arrival_airport="LAX",
        total_seats=200,
        available_seats=50
    )

@pytest.fixture
def sample_passenger():
    return Passenger(
        passenger_id="PS123",
        first_name="John",
        last_name="Doe",
        email="john@example.com"
    )

@pytest.mark.asyncio
@patch('app.booking.booking_service.assign_seat')
async def test_create_booking_success(mock_assign_seat, booking_service, sample_booking_data, sample_flight, sample_passenger):
    # Arrange
    mock_assign_seat.return_value = "12A"
    booking_service.flight_repository.find_by_id = AsyncMock(return_value=sample_flight)
    booking_service.passenger_repository.find_by_id = AsyncMock(return_value=sample_passenger)
    booking_service.flight_repository.update_available_seats = AsyncMock()
    
    created_booking = Booking(booking_id="BK123", flight_id="FL123", passenger_id="PS123", seat_number="12A")
    booking_service.booking_repository.save = AsyncMock(return_value=created_booking)
    
    # Act
    result = await booking_service.create_booking(sample_booking_data, "user123")
    
    # Assert
    assert result.booking_id == "BK123"
    booking_service.flight_repository.find_by_id.assert_called_once_with("FL123")
    booking_service.passenger_repository.find_by_id.assert_called_once_with("PS123")
    booking_service.flight_repository.update_available_seats.assert_called_once_with("FL123", -1)

@pytest.mark.asyncio
async def test_create_booking_flight_not_found(booking_service, sample_booking_data):
    # Arrange
    booking_service.flight_repository.find_by_id = AsyncMock(return_value=None)
    
    # Act & Assert
    with pytest.raises(FlightNotFoundError):
        await booking_service.create_booking(sample_booking_data, "user123")

@pytest.mark.asyncio
async def test_create_booking_passenger_not_found(booking_service, sample_booking_data, sample_flight):
    # Arrange
    booking_service.flight_repository.find_by_id = AsyncMock(return_value=sample_flight)
    booking_service.passenger_repository.find_by_id = AsyncMock(return_value=None)
    
    # Act & Assert
    with pytest.raises(PassengerNotFoundError):
        await booking_service.create_booking(sample_booking_data, "user123")

@pytest.mark.asyncio
async def test_create_booking_no_seats_available(booking_service, sample_booking_data, sample_passenger):
    # Arrange
    no_seats_flight = Flight(flight_id="FL123", available_seats=0)
    booking_service.flight_repository.find_by_id = AsyncMock(return_value=no_seats_flight)
    booking_service.passenger_repository.find_by_id = AsyncMock(return_value=sample_passenger)
    
    # Act & Assert
    with pytest.raises(NoSeatsAvailableError):
        await booking_service.create_booking(sample_booking_data, "user123")

@pytest.mark.asyncio
async def test_create_booking_rollback_on_error(booking_service, sample_booking_data, sample_flight, sample_passenger):
    # Arrange
    booking_service.flight_repository.find_by_id = AsyncMock(return_value=sample_flight)
    booking_service.passenger_repository.find_by_id = AsyncMock(return_value=sample_passenger)
    booking_service.flight_repository.update_available_seats = AsyncMock(side_effect=Exception("DB Error"))
    booking_service.db.rollback = AsyncMock()
    
    # Act & Assert
    with pytest.raises(Exception):
        await booking_service.create_booking(sample_booking_data, "user123")
    
    booking_service.db.rollback.assert_called_once()

@pytest.mark.asyncio
async def test_get_booking_by_id_success(booking_service):
    # Arrange
    sample_booking = Booking(booking_id="BK123")
    booking_service.booking_repository.find_by_id = AsyncMock(return_value=sample_booking)
    
    # Act
    result = await booking_service.get_booking_by_id("BK123")
    
    # Assert
    assert result == sample_booking

@pytest.mark.asyncio
async def test_get_booking_by_id_not_found(booking_service):
    # Arrange
    booking_service.booking_repository.find_by_id = AsyncMock(return_value=None)
    
    # Act & Assert
    with pytest.raises(BookingNotFoundError):
        await booking_service.get_booking_by_id("INVALID")

@pytest.mark.asyncio
async def test_cancel_booking_success(booking_service):
    # Arrange
    sample_booking = Booking(booking_id="BK123", flight_id="FL123")
    booking_service.booking_repository.find_by_id = AsyncMock(return_value=sample_booking)
    booking_service.booking_repository.update_status = AsyncMock()
    booking_service.flight_repository.update_available_seats = AsyncMock()
    booking_service.db.commit = AsyncMock()
    
    # Act
    await booking_service.cancel_booking("BK123", "user123")
    
    # Assert
    booking_service.booking_repository.update_status.assert_called_once_with("BK123", "cancelled")
    booking_service.flight_repository.update_available_seats.assert_called_once_with("FL123", 1)

@pytest.mark.asyncio
async def test_cancel_booking_not_found(booking_service):
    # Arrange
    booking_service.booking_repository.find_by_id = AsyncMock(return_value=None)
    
    # Act & Assert
    with pytest.raises(BookingNotFoundError):
        await booking_service.cancel_booking("INVALID", "user123")

@pytest.mark.asyncio
async def test_cancel_booking_rollback_on_error(booking_service):
    # Arrange
    sample_booking = Booking(booking_id="BK123", flight_id="FL123")
    booking_service.booking_repository.find_by_id = AsyncMock(return_value=sample_booking)
    booking_service.booking_repository.update_status = AsyncMock(side_effect=Exception("DB Error"))
    booking_service.db.rollback = AsyncMock()
    
    # Act & Assert
    with pytest.raises(Exception):
        await booking_service.cancel_booking("BK123", "user123")
    
    booking_service.db.rollback.assert_called_once()