import uuid
from datetime import datetime, timedelta

def generate_id() -> str:
    """Generate unique ID"""
    return str(uuid.uuid4())

def generate_boarding_pass_number(flight_id: str, booking_id: str) -> str:
    """Generate boarding pass number"""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"{flight_id}-{booking_id[:8]}-{timestamp}"

def get_boarding_group(seat_number: str) -> str:
    """Determine boarding group based on seat"""
    row = int(seat_number[:-1])
    if row <= 10:
        return "A"  # First class
    elif row <= 30:
        return "B"  # Business
    else:
        return "C"  # Economy

def assign_seat(total_seats: int, available_seats: int) -> str:
    """Auto-assign seat"""
    row = total_seats - available_seats + 1
    seat_letter = 'A'
    return f"{row}{seat_letter}"

def validate_checkin_window(departure_time: datetime) -> tuple[bool, str]:
    """Validate if check-in is allowed"""
    now = datetime.utcnow()
    hours_until_departure = (departure_time - now).total_seconds() / 3600
    
    if hours_until_departure > 24:
        return False, "Check-in opens 24 hours before departure"
    elif hours_until_departure < 1:
        return False, "Check-in closes 1 hour before departure"
    else:
        return True, ""