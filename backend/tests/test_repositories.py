import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.flight_repository import FlightRepository
from app.repositories.passenger_repository import PassengerRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.checkin_repository import CheckinRepository
from app.core.schemas import FlightCreate, PassengerCreate, BookingCreate
from app.core.models import Flight, Passenger, Booking, CheckinRecord

@pytest.mark.asyncio
async def test_flight_repository_create(db_session: AsyncSession):
    """Test flight repository create method."""
    repo = FlightRepository(db_session)
    
    flight_data = FlightCreate(
        flight_id="TEST123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180
    )
    
    flight = await repo.create(flight_data)
    
    assert flight.flight_id == "TEST123"
    assert flight.total_seats == 180
    assert flight.available_seats == 180

@pytest.mark.asyncio
async def test_flight_repository_get_by_id(db_session: AsyncSession):
    """Test flight repository get by ID."""
    repo = FlightRepository(db_session)
    
    # Create flight first
    flight_data = FlightCreate(
        flight_id="TEST123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180
    )
    await repo.create(flight_data)
    
    # Get flight
    flight = await repo.get_by_id("TEST123")
    assert flight is not None
    assert flight.flight_id == "TEST123"
    
    # Test non-existent flight
    flight = await repo.get_by_id("NONEXISTENT")
    assert flight is None

@pytest.mark.asyncio
async def test_flight_repository_get_all(db_session: AsyncSession):
    """Test flight repository get all."""
    repo = FlightRepository(db_session)
    
    # Initially empty
    flights = await repo.get_all()
    assert len(flights) == 0
    
    # Create flights
    for i in range(3):
        flight_data = FlightCreate(
            flight_id=f"TEST{i}",
            departure_airport="JFK",
            arrival_airport="LAX",
            departure_time=datetime.utcnow() + timedelta(hours=6),
            arrival_time=datetime.utcnow() + timedelta(hours=12),
            aircraft_type="Boeing 737",
            total_seats=180
        )
        await repo.create(flight_data)
    
    flights = await repo.get_all()
    assert len(flights) == 3

@pytest.mark.asyncio
async def test_flight_repository_update_seats(db_session: AsyncSession):
    """Test flight repository update available seats."""
    repo = FlightRepository(db_session)
    
    flight_data = FlightCreate(
        flight_id="TEST123",
        departure_airport="JFK",
        arrival_airport="LAX",
        departure_time=datetime.utcnow() + timedelta(hours=6),
        arrival_time=datetime.utcnow() + timedelta(hours=12),
        aircraft_type="Boeing 737",
        total_seats=180
    )
    await repo.create(flight_data)
    
    # Update seats
    await repo.update_available_seats("TEST123", -1)
    
    flight = await repo.get_by_id("TEST123")
    assert flight.available_seats == 179

@pytest.mark.asyncio
async def test_passenger_repository_create(db_session: AsyncSession):
    """Test passenger repository create method."""
    repo = PassengerRepository(db_session)
    
    passenger_data = PassengerCreate(
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        phone="+1234567890",
        date_of_birth="1990-01-15"
    )
    
    passenger = await repo.create(passenger_data)
    
    assert passenger.first_name == "John"
    assert passenger.email == "john.doe@test.com"
    assert passenger.passenger_id is not None

@pytest.mark.asyncio
async def test_passenger_repository_get_by_email(db_session: AsyncSession):
    """Test passenger repository get by email."""
    repo = PassengerRepository(db_session)
    
    passenger_data = PassengerCreate(
        first_name="John",
        last_name="Doe",
        email="john.doe@test.com",
        phone="+1234567890",
        date_of_birth="1990-01-15"
    )
    await repo.create(passenger_data)
    
    # Get by email
    passenger = await repo.get_by_email("john.doe@test.com")
    assert passenger is not None
    assert passenger.email == "john.doe@test.com"
    
    # Test non-existent email
    passenger = await repo.get_by_email("nonexistent@test.com")
    assert passenger is None

@pytest.mark.asyncio
async def test_booking_repository_create(db_session: AsyncSession):
    """Test booking repository create method."""
    repo = BookingRepository(db_session)
    
    booking_data = BookingCreate(
        flight_id="TEST123",
        passenger_id="P123",
        seat_number="12A"
    )
    
    booking = await repo.create(booking_data, "12A")
    
    assert booking.flight_id == "TEST123"
    assert booking.seat_number == "12A"
    assert booking.booking_id is not None

@pytest.mark.asyncio
async def test_booking_repository_update_status(db_session: AsyncSession):
    """Test booking repository update status."""
    repo = BookingRepository(db_session)
    
    booking_data = BookingCreate(
        flight_id="TEST123",
        passenger_id="P123",
        seat_number="12A"
    )
    booking = await repo.create(booking_data, "12A")
    
    # Update status
    await repo.update_status(booking.booking_id, "checked_in")
    
    updated_booking = await repo.get_by_id(booking.booking_id)
    assert updated_booking.booking_status == "checked_in"

@pytest.mark.asyncio
async def test_checkin_repository_create(db_session: AsyncSession):
    """Test checkin repository create method."""
    repo = CheckinRepository(db_session)
    
    checkin = await repo.create("B123", "BP123", "A1", "B")
    
    assert checkin.booking_id == "B123"
    assert checkin.boarding_pass_number == "BP123"
    assert checkin.gate_number == "A1"
    assert checkin.boarding_group == "B"

@pytest.mark.asyncio
async def test_checkin_repository_get_by_booking_id(db_session: AsyncSession):
    """Test checkin repository get by booking ID."""
    repo = CheckinRepository(db_session)
    
    checkin = await repo.create("B123", "BP123", "A1", "B")
    
    # Get by booking ID
    found_checkin = await repo.get_by_booking_id("B123")
    assert found_checkin is not None
    assert found_checkin.booking_id == "B123"
    
    # Test non-existent booking
    found_checkin = await repo.get_by_booking_id("NONEXISTENT")
    assert found_checkin is None