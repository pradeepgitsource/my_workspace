import pytest
from unittest.mock import Mock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.flight.flight_repository import FlightRepository
from app.passenger.passenger_repository import PassengerRepository
from models import Flight, Passenger

@pytest.fixture
def mock_db():
    return Mock(spec=AsyncSession)

@pytest.fixture
def flight_repository(mock_db):
    return FlightRepository(mock_db)

@pytest.fixture
def passenger_repository(mock_db):
    return PassengerRepository(mock_db)

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

# Flight Repository Tests
@pytest.mark.asyncio
async def test_flight_find_by_id_success(flight_repository, mock_db, sample_flight):
    # Arrange
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = sample_flight
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    # Act
    result = await flight_repository.find_by_id("FL123")
    
    # Assert
    assert result == sample_flight
    mock_db.execute.assert_called_once()

@pytest.mark.asyncio
async def test_flight_find_by_id_not_found(flight_repository, mock_db):
    # Arrange
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    # Act
    result = await flight_repository.find_by_id("INVALID")
    
    # Assert
    assert result is None

@pytest.mark.asyncio
async def test_flight_update_available_seats(flight_repository, mock_db):
    # Arrange
    mock_db.execute = AsyncMock()
    
    # Act
    await flight_repository.update_available_seats("FL123", -1)
    
    # Assert
    mock_db.execute.assert_called_once()

@pytest.mark.asyncio
async def test_flight_update_available_seats_positive(flight_repository, mock_db):
    # Arrange
    mock_db.execute = AsyncMock()
    
    # Act
    await flight_repository.update_available_seats("FL123", 5)
    
    # Assert
    mock_db.execute.assert_called_once()

# Passenger Repository Tests
@pytest.mark.asyncio
async def test_passenger_find_by_id_success(passenger_repository, mock_db, sample_passenger):
    # Arrange
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = sample_passenger
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    # Act
    result = await passenger_repository.find_by_id("PS123")
    
    # Assert
    assert result == sample_passenger
    mock_db.execute.assert_called_once()

@pytest.mark.asyncio
async def test_passenger_find_by_id_not_found(passenger_repository, mock_db):
    # Arrange
    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    # Act
    result = await passenger_repository.find_by_id("INVALID")
    
    # Assert
    assert result is None

@pytest.mark.asyncio
async def test_passenger_find_by_id_database_error(passenger_repository, mock_db):
    # Arrange
    mock_db.execute = AsyncMock(side_effect=Exception("Database error"))
    
    # Act & Assert
    with pytest.raises(Exception):
        await passenger_repository.find_by_id("PS123")

@pytest.mark.asyncio
async def test_flight_find_by_id_database_error(flight_repository, mock_db):
    # Arrange
    mock_db.execute = AsyncMock(side_effect=Exception("Database error"))
    
    # Act & Assert
    with pytest.raises(Exception):
        await flight_repository.find_by_id("FL123")

@pytest.mark.asyncio
async def test_flight_update_seats_database_error(flight_repository, mock_db):
    # Arrange
    mock_db.execute = AsyncMock(side_effect=Exception("Database error"))
    
    # Act & Assert
    with pytest.raises(Exception):
        await flight_repository.update_available_seats("FL123", -1)