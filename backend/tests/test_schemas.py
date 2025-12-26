import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError

from app.core.schemas import (
    FlightCreate,
    PassengerCreate,
    BookingCreate,
    CheckinRequest
)

def test_flight_create_valid():
    """Test valid flight creation schema."""
    flight_data = {
        "flight_id": "AA123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": datetime.utcnow() + timedelta(hours=6),
        "arrival_time": datetime.utcnow() + timedelta(hours=12),
        "aircraft_type": "Boeing 737",
        "total_seats": 180
    }
    
    flight = FlightCreate(**flight_data)
    
    assert flight.flight_id == "AA123"
    assert flight.total_seats == 180

def test_passenger_create_valid():
    """Test valid passenger creation schema."""
    passenger_data = {
        "first_name": "john",
        "last_name": "doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    
    passenger = PassengerCreate(**passenger_data)
    
    # Names should be title cased
    assert passenger.first_name == "John"
    assert passenger.last_name == "Doe"
    assert passenger.phone == "+1234567890"

def test_passenger_create_invalid_email():
    """Test passenger creation with invalid email."""
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "invalid-email",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    
    with pytest.raises(ValidationError):
        PassengerCreate(**passenger_data)

def test_passenger_create_invalid_phone():
    """Test passenger creation with invalid phone."""
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "invalid-phone",
        "date_of_birth": "1990-01-15"
    }
    
    with pytest.raises(ValidationError):
        PassengerCreate(**passenger_data)

def test_passenger_create_short_name():
    """Test passenger creation with short name."""
    passenger_data = {
        "first_name": "J",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    
    with pytest.raises(ValidationError):
        PassengerCreate(**passenger_data)

def test_passenger_create_phone_cleaning():
    """Test phone number cleaning."""
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1 (234) 567-8900",
        "date_of_birth": "1990-01-15"
    }
    
    passenger = PassengerCreate(**passenger_data)
    
    # Phone should be cleaned (spaces and parentheses removed)
    assert passenger.phone == "+12345678900"

def test_booking_create_valid():
    """Test valid booking creation schema."""
    booking_data = {
        "flight_id": "AA123",
        "passenger_id": "P123",
        "seat_number": "12A"
    }
    
    booking = BookingCreate(**booking_data)
    
    assert booking.flight_id == "AA123"
    assert booking.seat_number == "12A"

def test_booking_create_invalid_seat():
    """Test booking creation with invalid seat."""
    booking_data = {
        "flight_id": "AA123",
        "passenger_id": "P123",
        "seat_number": "invalid-seat"
    }
    
    with pytest.raises(ValidationError):
        BookingCreate(**booking_data)

def test_booking_create_seat_case_conversion():
    """Test seat number case conversion."""
    booking_data = {
        "flight_id": "AA123",
        "passenger_id": "P123",
        "seat_number": "12a"
    }
    
    booking = BookingCreate(**booking_data)
    
    # Seat should be uppercase
    assert booking.seat_number == "12A"

def test_booking_create_no_seat():
    """Test booking creation without seat number."""
    booking_data = {
        "flight_id": "AA123",
        "passenger_id": "P123"
    }
    
    booking = BookingCreate(**booking_data)
    
    assert booking.seat_number is None

def test_checkin_request_valid():
    """Test valid check-in request schema."""
    checkin_data = {
        "booking_id": "B123",
        "passenger_id": "P123"
    }
    
    checkin = CheckinRequest(**checkin_data)
    
    assert checkin.booking_id == "B123"
    assert checkin.passenger_id == "P123"