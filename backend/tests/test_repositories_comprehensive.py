import pytest
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.flight_repository import FlightRepository
from app.repositories.passenger_repository import PassengerRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.checkin_repository import CheckinRepository
from app.core.models import Flight, Passenger, Booking, CheckinRecord

@pytest.mark.asyncio
async def test_flight_repository_create(db_session: AsyncSession):
    """Test flight repository create operation."""
    repo = FlightRepository(db_session)
    
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": datetime.utcnow() + timedelta(hours=6),
        "arrival_time": datetime.utcnow() + timedelta(hours=12),
        "aircraft_type": "Boeing 737",
        "total_seats": 180,
        "available_seats": 180,
        "status": "scheduled"
    }
    
    flight = await repo.create(flight_data)
    
    assert flight.flight_id == "TEST123"
    assert flight.total_seats == 180
    assert flight.available_seats == 180

@pytest.mark.asyncio
async def test_flight_repository_get_by_id(db_session: AsyncSession):
    """Test flight repository get by ID."""
    repo = FlightRepository(db_session)
    
    # Create flight first
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": datetime.utcnow() + timedelta(hours=6),
        "arrival_time": datetime.utcnow() + timedelta(hours=12),
        "aircraft_type": "Boeing 737",
        "total_seats": 180,
        "available_seats": 180,
        "status": "scheduled"
    }
    
    await repo.create(flight_data)
    
    # Get flight
    flight = await repo.get_by_id("TEST123")
    
    assert flight is not None
    assert flight.flight_id == "TEST123"
    assert flight.departure_airport == "JFK"

@pytest.mark.asyncio
async def test_flight_repository_get_all(db_session: AsyncSession):
    """Test flight repository get all flights."""
    repo = FlightRepository(db_session)
    
    # Create multiple flights
    for i in range(3):
        flight_data = {
            "flight_id": f"TEST{i}",
            "departure_airport": "JFK",
            "arrival_airport": "LAX",
            "departure_time": datetime.utcnow() + timedelta(hours=6+i),
            "arrival_time": datetime.utcnow() + timedelta(hours=12+i),
            "aircraft_type": "Boeing 737",
            "total_seats": 180,
            "available_seats": 180,
            "status": "scheduled"
        }
        await repo.create(flight_data)
    
    flights = await repo.get_all()
    
    assert len(flights) == 3
    assert all(f.flight_id.startswith("TEST") for f in flights)

@pytest.mark.asyncio
async def test_flight_repository_update_available_seats(db_session: AsyncSession):
    """Test flight repository update available seats."""
    repo = FlightRepository(db_session)
    
    # Create flight
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": datetime.utcnow() + timedelta(hours=6),
        "arrival_time": datetime.utcnow() + timedelta(hours=12),
        "aircraft_type": "Boeing 737",
        "total_seats": 180,
        "available_seats": 180,
        "status": "scheduled"
    }
    
    await repo.create(flight_data)
    
    # Update available seats
    await repo.update_available_seats("TEST123", -1)
    
    flight = await repo.get_by_id("TEST123")
    assert flight.available_seats == 179

@pytest.mark.asyncio
async def test_passenger_repository_create(db_session: AsyncSession):
    """Test passenger repository create operation."""
    repo = PassengerRepository(db_session)
    
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    
    passenger = await repo.create(passenger_data)
    
    assert passenger.first_name == "John"
    assert passenger.email == "john.doe@test.com"
    assert passenger.passenger_id is not None

@pytest.mark.asyncio
async def test_passenger_repository_get_by_email(db_session: AsyncSession):
    """Test passenger repository get by email."""
    repo = PassengerRepository(db_session)
    
    # Create passenger
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    
    created_passenger = await repo.create(passenger_data)
    
    # Get by email
    passenger = await repo.get_by_email("john.doe@test.com")
    
    assert passenger is not None
    assert passenger.passenger_id == created_passenger.passenger_id
    assert passenger.first_name == "John"

@pytest.mark.asyncio
async def test_passenger_repository_get_bookings(db_session: AsyncSession):
    """Test passenger repository get bookings."""
    passenger_repo = PassengerRepository(db_session)
    flight_repo = FlightRepository(db_session)
    booking_repo = BookingRepository(db_session)
    
    # Create passenger
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    passenger = await passenger_repo.create(passenger_data)
    
    # Create flight
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": datetime.utcnow() + timedelta(hours=6),
        "arrival_time": datetime.utcnow() + timedelta(hours=12),
        "aircraft_type": "Boeing 737",
        "total_seats": 180,
        "available_seats": 180,
        "status": "scheduled"
    }
    await flight_repo.create(flight_data)
    
    # Create booking
    booking_data = {
        "flight_id": "TEST123",
        "passenger_id": passenger.passenger_id,
        "seat_number": "12A",
        "booking_status": "confirmed"
    }
    await booking_repo.create(booking_data)
    
    # Get passenger bookings
    bookings = await passenger_repo.get_bookings(passenger.passenger_id)
    
    assert len(bookings) == 1
    assert bookings[0].seat_number == "12A"

@pytest.mark.asyncio
async def test_booking_repository_create(db_session: AsyncSession):
    """Test booking repository create operation."""
    passenger_repo = PassengerRepository(db_session)
    flight_repo = FlightRepository(db_session)
    booking_repo = BookingRepository(db_session)
    
    # Create passenger and flight first
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    passenger = await passenger_repo.create(passenger_data)
    
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": datetime.utcnow() + timedelta(hours=6),
        "arrival_time": datetime.utcnow() + timedelta(hours=12),
        "aircraft_type": "Boeing 737",
        "total_seats": 180,
        "available_seats": 180,
        "status": "scheduled"
    }
    await flight_repo.create(flight_data)
    
    # Create booking
    booking_data = {
        "flight_id": "TEST123",
        "passenger_id": passenger.passenger_id,
        "seat_number": "12A",
        "booking_status": "confirmed"
    }
    
    booking = await booking_repo.create(booking_data)
    
    assert booking.flight_id == "TEST123"
    assert booking.seat_number == "12A"
    assert booking.booking_id is not None

@pytest.mark.asyncio
async def test_booking_repository_get_with_flight(db_session: AsyncSession):
    """Test booking repository get with flight details."""
    passenger_repo = PassengerRepository(db_session)
    flight_repo = FlightRepository(db_session)
    booking_repo = BookingRepository(db_session)
    
    # Setup data
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    passenger = await passenger_repo.create(passenger_data)
    
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": datetime.utcnow() + timedelta(hours=6),
        "arrival_time": datetime.utcnow() + timedelta(hours=12),
        "aircraft_type": "Boeing 737",
        "total_seats": 180,
        "available_seats": 180,
        "status": "scheduled"
    }
    await flight_repo.create(flight_data)
    
    booking_data = {
        "flight_id": "TEST123",
        "passenger_id": passenger.passenger_id,
        "seat_number": "12A",
        "booking_status": "confirmed"
    }
    booking = await booking_repo.create(booking_data)
    
    # Get booking with flight
    result = await booking_repo.get_with_flight(booking.booking_id)
    
    assert result is not None
    booking_result, flight_result = result
    assert booking_result.booking_id == booking.booking_id
    assert flight_result.flight_id == "TEST123"

@pytest.mark.asyncio
async def test_checkin_repository_create(db_session: AsyncSession):
    """Test checkin repository create operation."""
    passenger_repo = PassengerRepository(db_session)
    flight_repo = FlightRepository(db_session)
    booking_repo = BookingRepository(db_session)
    checkin_repo = CheckinRepository(db_session)
    
    # Setup data
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    passenger = await passenger_repo.create(passenger_data)
    
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": datetime.utcnow() + timedelta(hours=6),
        "arrival_time": datetime.utcnow() + timedelta(hours=12),
        "aircraft_type": "Boeing 737",
        "total_seats": 180,
        "available_seats": 180,
        "status": "scheduled"
    }
    await flight_repo.create(flight_data)
    
    booking_data = {
        "flight_id": "TEST123",
        "passenger_id": passenger.passenger_id,
        "seat_number": "12A",
        "booking_status": "confirmed"
    }
    booking = await booking_repo.create(booking_data)
    
    # Create checkin
    checkin_data = {
        "booking_id": booking.booking_id,
        "boarding_pass_number": "TEST123-12A-20241226",
        "gate_number": "A1",
        "boarding_group": "B"
    }
    
    checkin = await checkin_repo.create(checkin_data)
    
    assert checkin.booking_id == booking.booking_id
    assert checkin.boarding_pass_number == "TEST123-12A-20241226"
    assert checkin.checkin_id is not None

@pytest.mark.asyncio
async def test_checkin_repository_get_by_booking_id(db_session: AsyncSession):
    """Test checkin repository get by booking ID."""
    passenger_repo = PassengerRepository(db_session)
    flight_repo = FlightRepository(db_session)
    booking_repo = BookingRepository(db_session)
    checkin_repo = CheckinRepository(db_session)
    
    # Setup data
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    passenger = await passenger_repo.create(passenger_data)
    
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": datetime.utcnow() + timedelta(hours=6),
        "arrival_time": datetime.utcnow() + timedelta(hours=12),
        "aircraft_type": "Boeing 737",
        "total_seats": 180,
        "available_seats": 180,
        "status": "scheduled"
    }
    await flight_repo.create(flight_data)
    
    booking_data = {
        "flight_id": "TEST123",
        "passenger_id": passenger.passenger_id,
        "seat_number": "12A",
        "booking_status": "confirmed"
    }
    booking = await booking_repo.create(booking_data)
    
    checkin_data = {
        "booking_id": booking.booking_id,
        "boarding_pass_number": "TEST123-12A-20241226",
        "gate_number": "A1",
        "boarding_group": "B"
    }
    created_checkin = await checkin_repo.create(checkin_data)
    
    # Get checkin by booking ID
    checkin = await checkin_repo.get_by_booking_id(booking.booking_id)
    
    assert checkin is not None
    assert checkin.checkin_id == created_checkin.checkin_id
    assert checkin.boarding_group == "B"