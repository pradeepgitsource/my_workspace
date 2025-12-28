import pytest
from unittest.mock import Mock, AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.booking.booking_repository import BookingRepository
from models import Booking, Flight
from app.shared.exceptions import BookingNotFoundError

@pytest.fixture
def mock_db():
    return Mock(spec=AsyncSession)

@pytest.fixture
def booking_repository(mock_db):
    return BookingRepository(mock_db)

@pytest.fixture
def sample_booking():
    return Booking(
        booking_id="BK123",
        flight_id="FL123",
        passenger_id="PS123",
        seat_number="12A",
        booking_status="confirmed"
    )

@pytest.mark.asyncio
async def test_find_by_id_success(booking_repository, mock_db, sample_booking):
    # Arrange
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = sample_booking
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    # Act
    result = await booking_repository.find_by_id("BK123")
    
    # Assert
    assert result == sample_booking
    mock_db.execute.assert_called_once()

@pytest.mark.asyncio
async def test_find_by_id_not_found(booking_repository, mock_db):
    # Arrange
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    # Act
    result = await booking_repository.find_by_id("INVALID")
    
    # Assert
    assert result is None

@pytest.mark.asyncio
async def test_save_success(booking_repository, mock_db, sample_booking):
    # Arrange
    mock_db.add = Mock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    # Act
    result = await booking_repository.save(sample_booking)
    
    # Assert
    assert result == sample_booking
    mock_db.add.assert_called_once_with(sample_booking)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(sample_booking)

@pytest.mark.asyncio
async def test_update_status_success(booking_repository, mock_db):
    # Arrange
    mock_db.execute = AsyncMock()
    
    # Act
    await booking_repository.update_status("BK123", "cancelled")
    
    # Assert
    mock_db.execute.assert_called_once()

@pytest.mark.asyncio
async def test_find_booking_with_flight_success(booking_repository, mock_db, sample_booking):
    # Arrange
    sample_flight = Flight(flight_id="FL123", departure_airport="NYC", arrival_airport="LAX")
    mock_result = Mock()
    mock_result.first.return_value = (sample_booking, sample_flight)
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    # Act
    result = await booking_repository.find_booking_with_flight("BK123")
    
    # Assert
    assert result == (sample_booking, sample_flight)
    mock_db.execute.assert_called_once()

@pytest.mark.asyncio
async def test_find_booking_with_flight_not_found(booking_repository, mock_db):
    # Arrange
    mock_result = Mock()
    mock_result.first.return_value = None
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    # Act
    result = await booking_repository.find_booking_with_flight("INVALID")
    
    # Assert
    assert result is None