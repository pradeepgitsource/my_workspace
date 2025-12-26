import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError

from app.core.schemas import (
    FlightCreate, FlightResponse,
    PassengerCreate, PassengerResponse,
    BookingCreate, BookingResponse,
    CheckinRequest, BoardingPassResponse
)

def test_flight_create_valid():
    """Test valid flight creation schema."""
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": datetime.utcnow() + timedelta(hours=6),
        "arrival_time": datetime.utcnow() + timedelta(hours=12),
        "aircraft_type": "Boeing 737",
        "total_seats": 180
    }
    
    flight = FlightCreate(**flight_data)
    
    assert flight.flight_id == "TEST123"
    assert flight.total_seats == 180
    assert flight.departure_airport == "JFK"

def test_flight_create_invalid_seats():
    """Test flight creation with invalid seat count."""
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": datetime.utcnow() + timedelta(hours=6),
        "arrival_time": datetime.utcnow() + timedelta(hours=12),
        "aircraft_type": "Boeing 737",
        "total_seats": -10  # Invalid
    }
    
    with pytest.raises(ValidationError):
        FlightCreate(**flight_data)

def test_flight_create_missing_required_field():
    """Test flight creation with missing required field."""
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        # Missing arrival_airport
        "departure_time": datetime.utcnow() + timedelta(hours=6),
        "arrival_time": datetime.utcnow() + timedelta(hours=12),
        "aircraft_type": "Boeing 737",
        "total_seats": 180
    }
    
    with pytest.raises(ValidationError):
        FlightCreate(**flight_data)

def test_flight_create_invalid_time_order():
    """Test flight creation with departure after arrival."""
    departure_time = datetime.utcnow() + timedelta(hours=12)
    arrival_time = datetime.utcnow() + timedelta(hours=6)  # Before departure
    
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": departure_time,
        "arrival_time": arrival_time,
        "aircraft_type": "Boeing 737",
        "total_seats": 180
    }
    
    with pytest.raises(ValidationError):
        FlightCreate(**flight_data)

def test_passenger_create_valid():
    """Test valid passenger creation schema."""
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    
    passenger = PassengerCreate(**passenger_data)
    
    assert passenger.first_name == "John"
    assert passenger.email == "john.doe@test.com"

def test_passenger_create_invalid_email():
    """Test passenger creation with invalid email."""
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "invalid-email",  # Invalid format
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    
    with pytest.raises(ValidationError):
        PassengerCreate(**passenger_data)

def test_passenger_create_empty_name():
    """Test passenger creation with empty name."""
    passenger_data = {
        "first_name": "",  # Empty
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    
    with pytest.raises(ValidationError):
        PassengerCreate(**passenger_data)

def test_booking_create_valid():
    """Test valid booking creation schema."""
    booking_data = {
        "flight_id": "TEST123",
        "passenger_id": "P123",
        "seat_number": "12A"
    }
    
    booking = BookingCreate(**booking_data)
    
    assert booking.flight_id == "TEST123"
    assert booking.seat_number == "12A"

def test_booking_create_invalid_seat_format():
    """Test booking creation with invalid seat format."""
    booking_data = {
        "flight_id": "TEST123",
        "passenger_id": "P123",
        "seat_number": "INVALID"  # Invalid format
    }
    
    with pytest.raises(ValidationError):
        BookingCreate(**booking_data)

def test_checkin_request_valid():
    """Test valid checkin request schema."""
    checkin_data = {
        "booking_id": "B123",
        "passenger_id": "P123"
    }
    
    checkin = CheckinRequest(**checkin_data)
    
    assert checkin.booking_id == "B123"
    assert checkin.passenger_id == "P123"

def test_checkin_request_missing_field():
    """Test checkin request with missing field."""
    checkin_data = {
        "booking_id": "B123"
        # Missing passenger_id
    }
    
    with pytest.raises(ValidationError):
        CheckinRequest(**checkin_data)

def test_flight_response_serialization():
    """Test flight response serialization."""
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": datetime.utcnow() + timedelta(hours=6),
        "arrival_time": datetime.utcnow() + timedelta(hours=12),
        "aircraft_type": "Boeing 737",
        "total_seats": 180,
        "available_seats": 179,
        "status": "scheduled"
    }
    
    flight = FlightResponse(**flight_data)
    
    assert flight.flight_id == "TEST123"
    assert flight.available_seats == 179
    
    # Test JSON serialization
    json_data = flight.model_dump()
    assert "flight_id" in json_data
    assert json_data["total_seats"] == 180

def test_passenger_response_serialization():
    """Test passenger response serialization."""
    passenger_data = {
        "passenger_id": "P123",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    
    passenger = PassengerResponse(**passenger_data)
    
    assert passenger.passenger_id == "P123"
    assert passenger.first_name == "John"
    
    # Test JSON serialization
    json_data = passenger.model_dump()
    assert "passenger_id" in json_data
    assert json_data["email"] == "john.doe@test.com"

def test_booking_response_serialization():
    """Test booking response serialization."""
    booking_data = {
        "booking_id": "B123",
        "flight_id": "TEST123",
        "passenger_id": "P123",
        "seat_number": "12A",
        "booking_status": "confirmed",
        "booking_date": datetime.utcnow()
    }
    
    booking = BookingResponse(**booking_data)
    
    assert booking.booking_id == "B123"
    assert booking.seat_number == "12A"
    
    # Test JSON serialization
    json_data = booking.model_dump()
    assert "booking_id" in json_data
    assert json_data["booking_status"] == "confirmed"

def test_boarding_pass_response_serialization():
    """Test boarding pass response serialization."""
    boarding_pass_data = {
        "checkin_id": "C123",
        "booking_id": "B123",
        "flight_id": "TEST123",
        "passenger_name": "John Doe",
        "seat_number": "12A",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": datetime.utcnow() + timedelta(hours=6),
        "boarding_pass_number": "TEST123-B123-20241226",
        "gate_number": "A1",
        "boarding_group": "B",
        "checkin_time": datetime.utcnow()
    }
    
    boarding_pass = BoardingPassResponse(**boarding_pass_data)
    
    assert boarding_pass.checkin_id == "C123"
    assert boarding_pass.boarding_group == "B"
    
    # Test JSON serialization
    json_data = boarding_pass.model_dump()
    assert "checkin_id" in json_data
    assert json_data["gate_number"] == "A1"

def test_schema_field_validation_edge_cases():
    """Test schema validation edge cases."""
    # Test very long flight ID
    with pytest.raises(ValidationError):
        FlightCreate(
            flight_id="A" * 100,  # Too long
            departure_airport="JFK",
            arrival_airport="LAX",
            departure_time=datetime.utcnow() + timedelta(hours=6),
            arrival_time=datetime.utcnow() + timedelta(hours=12),
            aircraft_type="Boeing 737",
            total_seats=180
        )
    
    # Test zero seats
    with pytest.raises(ValidationError):
        FlightCreate(
            flight_id="TEST123",
            departure_airport="JFK",
            arrival_airport="LAX",
            departure_time=datetime.utcnow() + timedelta(hours=6),
            arrival_time=datetime.utcnow() + timedelta(hours=12),
            aircraft_type="Boeing 737",
            total_seats=0  # Invalid
        )
    
    # Test past departure time
    with pytest.raises(ValidationError):
        FlightCreate(
            flight_id="TEST123",
            departure_airport="JFK",
            arrival_airport="LAX",
            departure_time=datetime.utcnow() - timedelta(hours=1),  # Past time
            arrival_time=datetime.utcnow() + timedelta(hours=12),
            aircraft_type="Boeing 737",
            total_seats=180
        )