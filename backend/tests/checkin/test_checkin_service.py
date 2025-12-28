import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.checkin.checkin_service import CheckinService
from models import Booking, Flight, CheckinRecord
from schemas import CheckinRequest
from app.shared.exceptions import (
    BookingNotFoundError, AlreadyCheckedInError, PassengerMismatchError,
    CheckinWindowError
)

@pytest.fixture
def mock_db():
    return Mock(spec=AsyncSession)

@pytest.fixture
def checkin_service(mock_db):
    return CheckinService(mock_db)

@pytest.fixture
def sample_checkin_data():
    return CheckinRequest(
        booking_id="BK123",
        passenger_id="PS123"
    )

@pytest.fixture
def sample_booking():
    return Booking(
        booking_id="BK123",
        flight_id="FL123",
        passenger_id="PS123",
        seat_number="12A"
    )

@pytest.fixture
def sample_flight():
    return Flight(
        flight_id="FL123",
        departure_time=datetime.utcnow() + timedelta(hours=2)
    )

@pytest.mark.asyncio
@patch('app.checkin.checkin_service.validate_checkin_window')
@patch('app.checkin.checkin_service.generate_boarding_pass_number')
@patch('app.checkin.checkin_service.get_boarding_group')
async def test_process_checkin_success(mock_boarding_group, mock_boarding_pass, mock_validate_window,
                                     checkin_service, sample_checkin_data, sample_booking, sample_flight):
    # Arrange
    mock_validate_window.return_value = (True, "")
    mock_boarding_pass.return_value = "BP123456"
    mock_boarding_group.return_value = "A"
    
    checkin_service.booking_repository.find_booking_with_flight = AsyncMock(return_value=(sample_booking, sample_flight))
    checkin_service.checkin_repository.find_by_booking_id = AsyncMock(return_value=None)
    checkin_service.booking_repository.update_status = AsyncMock()
    
    created_checkin = CheckinRecord(
        checkin_id="CI123",
        booking_id="BK123",
        boarding_pass_number="BP123456",
        boarding_group="A",
        gate_number="A1"
    )
    checkin_service.checkin_repository.save = AsyncMock(return_value=created_checkin)
    
    # Act
    result = await checkin_service.process_checkin(sample_checkin_data, "user123")
    
    # Assert
    assert result.checkin_id == "CI123"
    assert result.boarding_pass_number == "BP123456"
    checkin_service.booking_repository.update_status.assert_called_once_with("BK123", "checked_in")

@pytest.mark.asyncio
async def test_process_checkin_booking_not_found(checkin_service, sample_checkin_data):
    # Arrange
    checkin_service.booking_repository.find_booking_with_flight = AsyncMock(return_value=None)
    
    # Act & Assert
    with pytest.raises(BookingNotFoundError):
        await checkin_service.process_checkin(sample_checkin_data, "user123")

@pytest.mark.asyncio
async def test_process_checkin_passenger_mismatch(checkin_service, sample_checkin_data, sample_flight):
    # Arrange
    wrong_booking = Booking(booking_id="BK123", passenger_id="WRONG", seat_number="12A")
    checkin_service.booking_repository.find_booking_with_flight = AsyncMock(return_value=(wrong_booking, sample_flight))
    
    # Act & Assert
    with pytest.raises(PassengerMismatchError):
        await checkin_service.process_checkin(sample_checkin_data, "user123")

@pytest.mark.asyncio
async def test_process_checkin_already_checked_in(checkin_service, sample_checkin_data, sample_booking, sample_flight):
    # Arrange
    existing_checkin = CheckinRecord(checkin_id="CI999", booking_id="BK123")
    checkin_service.booking_repository.find_booking_with_flight = AsyncMock(return_value=(sample_booking, sample_flight))
    checkin_service.checkin_repository.find_by_booking_id = AsyncMock(return_value=existing_checkin)
    
    # Act & Assert
    with pytest.raises(AlreadyCheckedInError):
        await checkin_service.process_checkin(sample_checkin_data, "user123")

@pytest.mark.asyncio
@patch('app.checkin.checkin_service.validate_checkin_window')
async def test_process_checkin_window_error(mock_validate_window, checkin_service, sample_checkin_data, sample_booking, sample_flight):
    # Arrange
    mock_validate_window.return_value = (False, "Check-in window closed")
    checkin_service.booking_repository.find_booking_with_flight = AsyncMock(return_value=(sample_booking, sample_flight))
    checkin_service.checkin_repository.find_by_booking_id = AsyncMock(return_value=None)
    
    # Act & Assert
    with pytest.raises(CheckinWindowError):
        await checkin_service.process_checkin(sample_checkin_data, "user123")

@pytest.mark.asyncio
async def test_process_checkin_rollback_on_error(checkin_service, sample_checkin_data, sample_booking, sample_flight):
    # Arrange
    checkin_service.booking_repository.find_booking_with_flight = AsyncMock(return_value=(sample_booking, sample_flight))
    checkin_service.checkin_repository.find_by_booking_id = AsyncMock(return_value=None)
    checkin_service.booking_repository.update_status = AsyncMock(side_effect=Exception("DB Error"))
    checkin_service.db.rollback = AsyncMock()
    
    # Act & Assert
    with pytest.raises(Exception):
        await checkin_service.process_checkin(sample_checkin_data, "user123")
    
    checkin_service.db.rollback.assert_called_once()

@pytest.mark.asyncio
async def test_get_boarding_pass_success(checkin_service):
    # Arrange
    checkin_record = CheckinRecord(checkin_id="CI123", boarding_pass_number="BP123")
    booking = Booking(booking_id="BK123", seat_number="12A")
    flight = Flight(flight_id="FL123")
    
    checkin_service.checkin_repository.find_checkin_details_by_id = AsyncMock(return_value=(checkin_record, booking, flight))
    
    # Act
    result = await checkin_service.get_boarding_pass("CI123")
    
    # Assert
    assert result.checkin_id == "CI123"
    assert result.boarding_pass_number == "BP123"

@pytest.mark.asyncio
async def test_get_boarding_pass_not_found(checkin_service):
    # Arrange
    checkin_service.checkin_repository.find_checkin_details_by_id = AsyncMock(return_value=None)
    
    # Act & Assert
    with pytest.raises(BookingNotFoundError):
        await checkin_service.get_boarding_pass("INVALID")

@pytest.mark.asyncio
async def test_get_checkin_status_checked_in(checkin_service):
    # Arrange
    checkin_record = CheckinRecord(checkin_id="CI123", booking_id="BK123")
    checkin_service.checkin_repository.find_by_booking_id = AsyncMock(return_value=checkin_record)
    
    # Act
    result = await checkin_service.get_checkin_status("BK123")
    
    # Assert
    assert result["booking_id"] == "BK123"
    assert result["checked_in"] is True
    assert result["checkin_id"] == "CI123"

@pytest.mark.asyncio
async def test_get_checkin_status_not_checked_in(checkin_service):
    # Arrange
    checkin_service.checkin_repository.find_by_booking_id = AsyncMock(return_value=None)
    
    # Act
    result = await checkin_service.get_checkin_status("BK123")
    
    # Assert
    assert result["booking_id"] == "BK123"
    assert result["checked_in"] is False
    assert result["checkin_id"] is None