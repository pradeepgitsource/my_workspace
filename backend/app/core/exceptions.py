from fastapi import HTTPException, status
from typing import Optional

class BaseCustomException(Exception):
    """Base custom exception class"""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class BookingNotFoundError(BaseCustomException):
    def __init__(self, booking_id: Optional[str] = None):
        message = f"Booking {booking_id} not found" if booking_id else "Booking not found"
        super().__init__(message, status.HTTP_404_NOT_FOUND)

class FlightNotFoundError(BaseCustomException):
    def __init__(self, flight_id: Optional[str] = None):
        message = f"Flight {flight_id} not found" if flight_id else "Flight not found"
        super().__init__(message, status.HTTP_404_NOT_FOUND)

class PassengerNotFoundError(BaseCustomException):
    def __init__(self, passenger_id: Optional[str] = None):
        message = f"Passenger {passenger_id} not found" if passenger_id else "Passenger not found"
        super().__init__(message, status.HTTP_404_NOT_FOUND)

class NoSeatsAvailableError(BaseCustomException):
    def __init__(self):
        super().__init__("No seats available", status.HTTP_409_CONFLICT)

class AlreadyCheckedInError(BaseCustomException):
    def __init__(self, booking_id: Optional[str] = None):
        message = f"Booking {booking_id} already checked in" if booking_id else "Already checked in"
        super().__init__(message, status.HTTP_409_CONFLICT)

class PassengerMismatchError(BaseCustomException):
    def __init__(self):
        super().__init__("Passenger ID mismatch", status.HTTP_400_BAD_REQUEST)

class CheckinWindowError(BaseCustomException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_409_CONFLICT)

class UnauthorizedError(BaseCustomException):
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)

class ValidationError(BaseCustomException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)