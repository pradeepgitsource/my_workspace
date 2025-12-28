import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timedelta

from app.repositories.passenger_repository import PassengerRepository
from app.core.models import Passenger, Booking
from app.core.utils import generate_id, generate_boarding_pass_number, get_boarding_group, assign_seat, validate_checkin_window

@pytest.mark.asyncio
async def test_passenger_repository_get_by_email_working():
    """Test passenger repository get by email with mocked database."""
    mock_session = AsyncMock()
    mock_passenger = Passenger(
        passenger_id="1",
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        phone="+1234567890",
        date_of_birth="1990-01-15"
    )
    
    mock_result = AsyncMock()
    mock_result.scalar_one_or_none = MagicMock(return_value=mock_passenger)
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    repo = PassengerRepository(mock_session)
    result = await repo.get_by_email("john.doe@test.com")
    
    mock_session.execute.assert_called_once()
    assert result == mock_passenger

@pytest.mark.asyncio
async def test_passenger_repository_get_bookings_working():
    """Test passenger repository get bookings with mocked database."""
    mock_session = AsyncMock()
    mock_bookings = [
        Booking(booking_id="BOOK123", flight_id="TEST123", passenger_id="1", booking_status="confirmed"),
        Booking(booking_id="BOOK124", flight_id="TEST124", passenger_id="1", booking_status="confirmed")
    ]
    
    mock_result = AsyncMock()
    mock_result.scalars = MagicMock()
    mock_result.scalars.return_value.all = MagicMock(return_value=mock_bookings)
    mock_session.execute = AsyncMock(return_value=mock_result)
    
    repo = PassengerRepository(mock_session)
    result = await repo.get_bookings("1")
    
    mock_session.execute.assert_called_once()
    assert result == mock_bookings

def test_utils_generate_id_working():
    """Test generate_id produces valid UUID."""
    result = generate_id()
    assert isinstance(result, str)
    assert len(result) == 36  # UUID format length
    assert result.count('-') == 4  # UUID has 4 hyphens

def test_utils_generate_boarding_pass_number_working():
    """Test generate_boarding_pass_number format."""
    result = generate_boarding_pass_number("AA123", "BOOK456")
    assert isinstance(result, str)
    assert "AA123" in result
    assert "BOOK456" in result

def test_utils_get_boarding_group_working():
    """Test get_boarding_group with valid cases."""
    assert get_boarding_group("1A") == "A"
    assert get_boarding_group("15B") == "B"
    assert get_boarding_group("35C") == "C"

def test_utils_assign_seat_working():
    """Test assign_seat with valid parameters."""
    result = assign_seat(180, 150)
    assert isinstance(result, str)
    assert result == "31A"  # 180 - 150 + 1 = 31

def test_utils_validate_checkin_window_working():
    """Test validate_checkin_window returns tuple."""
    future_time = datetime.utcnow() + timedelta(hours=12)
    result = validate_checkin_window(future_time)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], bool)
    assert isinstance(result[1], str)

def test_utils_validate_checkin_window_valid_time():
    """Test validate_checkin_window with valid time."""
    valid_time = datetime.utcnow() + timedelta(hours=12)
    is_valid, message = validate_checkin_window(valid_time)
    assert is_valid is True
    assert message == ""

def test_utils_validate_checkin_window_too_early_time():
    """Test validate_checkin_window when too early."""
    early_time = datetime.utcnow() + timedelta(hours=25)
    is_valid, message = validate_checkin_window(early_time)
    assert is_valid is False
    assert "24 hours" in message

def test_utils_validate_checkin_window_too_late_time():
    """Test validate_checkin_window when too late."""
    late_time = datetime.utcnow() - timedelta(hours=2)
    is_valid, message = validate_checkin_window(late_time)
    assert is_valid is False
    assert "1 hour" in message

def test_utils_assign_seat_edge_cases():
    """Test assign_seat with edge cases."""
    with pytest.raises(ValueError, match="Total seats must be positive"):
        assign_seat(0, 0)
    
    with pytest.raises(ValueError, match="Available seats cannot exceed total seats"):
        assign_seat(100, 150)
    
    with pytest.raises(ValueError, match="Available seats cannot be negative"):
        assign_seat(100, -1)

def test_utils_get_boarding_group_invalid():
    """Test get_boarding_group with invalid input."""
    with pytest.raises(ValueError, match="Invalid seat number format"):
        get_boarding_group("")
    
    with pytest.raises(ValueError, match="Invalid seat number format"):
        get_boarding_group("A")
    
    with pytest.raises(ValueError, match="Invalid seat number format"):
        get_boarding_group("XYZ")