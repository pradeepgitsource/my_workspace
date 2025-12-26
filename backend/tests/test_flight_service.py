import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException

from app.services.flight_service import FlightService
from app.repositories.flight_repository import FlightRepository
from app.core.schemas import FlightCreate
from app.core.models import Flight

@pytest.mark.asyncio
async def test_create_flight_success(db_session):
    """Test successful flight creation."""
    flight_repo = FlightRepository(db_session)
    flight_service = FlightService(flight_repo)
    
    flight_data = FlightCreate(
        flight_id="TEST123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180
    )
    
    result = await flight_service.create_flight(flight_data)
    
    assert result.flight_id == "TEST123"
    assert result.departure_airport == "JFK"
    assert result.total_seats == 180
    assert result.available_seats == 180

@pytest.mark.asyncio
async def test_create_flight_duplicate(db_session):
    """Test flight creation with duplicate ID."""
    flight_repo = FlightRepository(db_session)
    flight_service = FlightService(flight_repo)
    
    # Create first flight
    flight_data = FlightCreate(
        flight_id="TEST123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180
    )
    
    await flight_service.create_flight(flight_data)
    
    # Try to create duplicate
    with pytest.raises(HTTPException) as exc_info:
        await flight_service.create_flight(flight_data)
    
    assert exc_info.value.status_code == 409
    assert "already exists" in exc_info.value.detail

@pytest.mark.asyncio
async def test_get_flight_not_found(db_session):
    """Test getting non-existent flight."""
    flight_repo = FlightRepository(db_session)
    flight_service = FlightService(flight_repo)
    
    with pytest.raises(HTTPException) as exc_info:
        await flight_service.get_flight("NONEXISTENT")
    
    assert exc_info.value.status_code == 404
    assert "not found" in exc_info.value.detail