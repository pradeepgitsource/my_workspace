import pytest
from datetime import datetime, timedelta
import uuid

from app.core.utils import (
    generate_id,
    generate_boarding_pass_number,
    get_boarding_group,
    assign_seat,
    validate_checkin_window
)

def test_generate_id():
    """Test ID generation utility."""
    id1 = generate_id()
    id2 = generate_id()
    
    # Should be valid UUIDs
    assert uuid.UUID(id1)
    assert uuid.UUID(id2)
    
    # Should be unique
    assert id1 != id2
    
    # Should be strings
    assert isinstance(id1, str)
    assert isinstance(id2, str)

def test_generate_boarding_pass_number():
    """Test boarding pass number generation."""
    flight_id = "TEST123"
    booking_id = "booking-12345678-abcd-efgh"
    
    boarding_pass = generate_boarding_pass_number(flight_id, booking_id)
    
    # Should contain flight ID
    assert flight_id in boarding_pass
    
    # Should contain first 8 chars of booking ID
    assert "booking-" in boarding_pass
    
    # Should contain timestamp
    assert len(boarding_pass.split("-")) >= 3
    
    # Should be consistent format
    parts = boarding_pass.split("-")
    assert parts[0] == flight_id
    # The timestamp should be the last part after splitting
    assert len(parts[-1]) == 14  # Timestamp format YYYYMMDDHHMMSS

def test_generate_boarding_pass_number_different_times():
    """Test boarding pass numbers generated at different times are unique."""
    flight_id = "TEST123"
    booking_id = "booking-12345678"
    
    pass1 = generate_boarding_pass_number(flight_id, booking_id)
    
    # Small delay to ensure different timestamp
    import time
    time.sleep(1.1)  # Ensure at least 1 second difference
    
    pass2 = generate_boarding_pass_number(flight_id, booking_id)
    
    # Should be different due to timestamp
    assert pass1 != pass2

def test_get_boarding_group_group_a():
    """Test boarding group A assignment (rows 1-10)."""
    test_seats = ["1A", "5B", "10C", "10F"]
    
    for seat in test_seats:
        group = get_boarding_group(seat)
        assert group == "A"

def test_get_boarding_group_group_b():
    """Test boarding group B assignment (rows 11-30)."""
    test_seats = ["11A", "15B", "25C", "30F"]
    
    for seat in test_seats:
        group = get_boarding_group(seat)
        assert group == "B"

def test_get_boarding_group_group_c():
    """Test boarding group C assignment (rows 31+)."""
    test_seats = ["31A", "35B", "45C", "99F"]
    
    for seat in test_seats:
        group = get_boarding_group(seat)
        assert group == "C"

def test_get_boarding_group_edge_cases():
    """Test boarding group assignment edge cases."""
    # Boundary cases
    assert get_boarding_group("10A") == "A"  # Last row of group A
    assert get_boarding_group("11A") == "B"  # First row of group B
    assert get_boarding_group("30A") == "B"  # Last row of group B
    assert get_boarding_group("31A") == "C"  # First row of group C
    
    # Different seat letters
    assert get_boarding_group("15A") == "B"
    assert get_boarding_group("15B") == "B"
    assert get_boarding_group("15C") == "B"
    assert get_boarding_group("15D") == "B"
    assert get_boarding_group("15E") == "B"
    assert get_boarding_group("15F") == "B"

def test_assign_seat():
    """Test seat assignment utility."""
    # First passenger on 180-seat flight
    seat1 = assign_seat(180, 180)
    assert seat1 == "1A"
    
    # Second passenger
    seat2 = assign_seat(180, 179)
    assert seat2 == "2A"
    
    # 50th passenger
    seat50 = assign_seat(180, 131)  # 180 - 131 + 1 = 50
    assert seat50 == "50A"
    
    # Last passenger
    seat_last = assign_seat(180, 1)
    assert seat_last == "180A"

def test_assign_seat_edge_cases():
    """Test seat assignment edge cases."""
    # Small aircraft
    seat_small = assign_seat(10, 10)
    assert seat_small == "1A"
    
    # Large aircraft
    seat_large = assign_seat(500, 1)
    assert seat_large == "500A"
    
    # Single seat aircraft
    seat_single = assign_seat(1, 1)
    assert seat_single == "1A"

def test_validate_checkin_window_valid():
    """Test valid check-in window."""
    # 12 hours before departure (valid)
    departure_time = datetime.utcnow() + timedelta(hours=12)
    
    is_valid, message = validate_checkin_window(departure_time)
    
    assert is_valid is True
    assert message == ""

def test_validate_checkin_window_too_early():
    """Test check-in too early (more than 24 hours)."""
    # 25 hours before departure (too early)
    departure_time = datetime.utcnow() + timedelta(hours=25)
    
    is_valid, message = validate_checkin_window(departure_time)
    
    assert is_valid is False
    assert "24 hours before departure" in message

def test_validate_checkin_window_too_late():
    """Test check-in too late (less than 1 hour)."""
    # 30 minutes before departure (too late)
    departure_time = datetime.utcnow() + timedelta(minutes=30)
    
    is_valid, message = validate_checkin_window(departure_time)
    
    assert is_valid is False
    assert "1 hour before departure" in message

def test_validate_checkin_window_boundary_cases():
    """Test check-in window boundary cases."""
    # Exactly 24 hours before (should be valid)
    departure_24h = datetime.utcnow() + timedelta(hours=24)
    is_valid_24h, _ = validate_checkin_window(departure_24h)
    assert is_valid_24h is True
    
    # Exactly 1 hour before (should be valid)
    departure_1h = datetime.utcnow() + timedelta(hours=1)
    is_valid_1h, _ = validate_checkin_window(departure_1h)
    assert is_valid_1h is True
    
    # Just over 24 hours (should be invalid)
    departure_over_24h = datetime.utcnow() + timedelta(hours=24, minutes=1)
    is_valid_over, _ = validate_checkin_window(departure_over_24h)
    assert is_valid_over is False
    
    # Just under 1 hour (should be invalid)
    departure_under_1h = datetime.utcnow() + timedelta(minutes=59)
    is_valid_under, _ = validate_checkin_window(departure_under_1h)
    assert is_valid_under is False

def test_validate_checkin_window_past_departure():
    """Test check-in after departure time."""
    # 1 hour after departure (way too late)
    departure_time = datetime.utcnow() - timedelta(hours=1)
    
    is_valid, message = validate_checkin_window(departure_time)
    
    assert is_valid is False
    assert "1 hour before departure" in message

def test_utility_functions_with_real_data():
    """Test utility functions with realistic data."""
    # Generate realistic boarding pass
    flight_id = "AA1234"
    booking_id = "bk-" + generate_id()
    
    boarding_pass = generate_boarding_pass_number(flight_id, booking_id)
    assert "AA1234" in boarding_pass
    
    # Test realistic seat assignments
    seats_and_groups = [
        ("3A", "A"),
        ("12B", "B"),
        ("25C", "B"),
        ("35D", "C")
    ]
    
    for seat, expected_group in seats_and_groups:
        group = get_boarding_group(seat)
        assert group == expected_group
    
    # Test realistic check-in scenarios
    scenarios = [
        (timedelta(hours=2), True),    # 2 hours before - valid
        (timedelta(hours=12), True),   # 12 hours before - valid
        (timedelta(hours=23), True),   # 23 hours before - valid
        (timedelta(hours=26), False),  # 26 hours before - too early
        (timedelta(minutes=30), False) # 30 minutes before - too late
    ]
    
    for time_delta, expected_valid in scenarios:
        departure = datetime.utcnow() + time_delta
        is_valid, _ = validate_checkin_window(departure)
        assert is_valid == expected_valid

def test_utility_functions_error_handling():
    """Test utility functions with invalid inputs."""
    # Test boarding group with invalid seat format
    with pytest.raises(ValueError):
        get_boarding_group("INVALID")
    
    # Test boarding group with non-numeric row
    with pytest.raises(ValueError):
        get_boarding_group("AA")
    
    # Test assign_seat with invalid parameters
    with pytest.raises(ValueError):
        assign_seat(0, 1)  # Total seats can't be 0
    
    with pytest.raises(ValueError):
        assign_seat(10, 11)  # Available seats can't exceed total
    
    with pytest.raises(ValueError):
        assign_seat(-5, 1)  # Negative total seats