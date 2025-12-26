import pytest
from datetime import datetime, timedelta

from app.core.utils import (
    generate_id,
    generate_boarding_pass_number,
    get_boarding_group,
    assign_seat,
    validate_checkin_window
)

def test_generate_id():
    """Test ID generation."""
    id1 = generate_id()
    id2 = generate_id()
    
    assert isinstance(id1, str)
    assert isinstance(id2, str)
    assert id1 != id2  # Should be unique
    assert len(id1) > 0

def test_generate_boarding_pass_number():
    """Test boarding pass number generation."""
    flight_id = "AA123"
    booking_id = "B12345678"
    
    boarding_pass = generate_boarding_pass_number(flight_id, booking_id)
    
    assert boarding_pass.startswith("AA123-B1234567")  # First 8 chars of booking_id
    assert len(boarding_pass.split("-")) == 3  # flight-booking-timestamp

def test_get_boarding_group():
    """Test boarding group assignment."""
    # Group A (rows 1-10)
    assert get_boarding_group("5A") == "A"
    assert get_boarding_group("10F") == "A"
    
    # Group B (rows 11-30)
    assert get_boarding_group("15C") == "B"
    assert get_boarding_group("30A") == "B"
    
    # Group C (rows 31+)
    assert get_boarding_group("35B") == "C"
    assert get_boarding_group("50F") == "C"

def test_assign_seat():
    """Test automatic seat assignment."""
    # First seat
    seat = assign_seat(total_seats=180, available_seats=180)
    assert seat == "1A"
    
    # Second seat
    seat = assign_seat(total_seats=180, available_seats=179)
    assert seat == "2A"
    
    # Last seat
    seat = assign_seat(total_seats=180, available_seats=1)
    assert seat == "180A"

def test_validate_checkin_window():
    """Test check-in window validation."""
    now = datetime.utcnow()
    
    # Too early (more than 24 hours)
    departure = now + timedelta(hours=25)
    valid, message = validate_checkin_window(departure)
    assert not valid
    assert "24 hours before" in message
    
    # Too late (less than 1 hour)
    departure = now + timedelta(minutes=30)
    valid, message = validate_checkin_window(departure)
    assert not valid
    assert "1 hour before" in message
    
    # Valid window (6 hours before)
    departure = now + timedelta(hours=6)
    valid, message = validate_checkin_window(departure)
    assert valid
    assert message == ""
    
    # Edge case: exactly 24 hours
    departure = now + timedelta(hours=24)
    valid, message = validate_checkin_window(departure)
    assert valid
    
    # Edge case: exactly 1 hour
    departure = now + timedelta(hours=1)
    valid, message = validate_checkin_window(departure)
    assert valid