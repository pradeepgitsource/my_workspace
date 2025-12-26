import uuid
from datetime import datetime, timedelta

def generate_id() -> str:
    return str(uuid.uuid4())

def generate_boarding_pass_number(flight_id: str, booking_id: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"{flight_id}-{booking_id[:8]}-{timestamp}"

def get_boarding_group(seat_number: str) -> str:
    if not seat_number or len(seat_number) < 2:
        raise ValueError("Invalid seat number format")
    
    try:
        row = int(seat_number[:-1])
    except ValueError:
        raise ValueError("Invalid seat number format")
    
    if row <= 10:
        return "A"
    elif row <= 30:
        return "B"
    else:
        return "C"

def assign_seat(total_seats: int, available_seats: int) -> str:
    if total_seats <= 0:
        raise ValueError("Total seats must be positive")
    if available_seats > total_seats:
        raise ValueError("Available seats cannot exceed total seats")
    if available_seats < 0:
        raise ValueError("Available seats cannot be negative")
    
    row = total_seats - available_seats + 1
    seat_letter = 'A'
    return f"{row}{seat_letter}"

def validate_checkin_window(departure_time: datetime) -> tuple[bool, str]:
    now = datetime.utcnow()
    hours_until_departure = (departure_time - now).total_seconds() / 3600
    
    if hours_until_departure > 24:
        return False, "Check-in opens 24 hours before departure"
    elif hours_until_departure < 1:
        return False, "Check-in closes 1 hour before departure"
    else:
        return True, ""