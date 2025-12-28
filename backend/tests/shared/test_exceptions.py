import pytest
from fastapi import status

from app.shared.exceptions import (
    BaseBusinessException, BookingNotFoundError, FlightNotFoundError,
    PassengerNotFoundError, NoSeatsAvailableError, AlreadyCheckedInError,
    PassengerMismatchError, CheckinWindowError, UnauthorizedAccessError,
    BusinessValidationError
)

def test_base_business_exception_default():
    # Act
    exc = BaseBusinessException("Test message")
    
    # Assert
    assert exc.message == "Test message"
    assert exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert str(exc) == "Test message"

def test_base_business_exception_custom_status():
    # Act
    exc = BaseBusinessException("Test message", status.HTTP_400_BAD_REQUEST)
    
    # Assert
    assert exc.message == "Test message"
    assert exc.status_code == status.HTTP_400_BAD_REQUEST

def test_booking_not_found_error_with_id():
    # Act
    exc = BookingNotFoundError("BK123")
    
    # Assert
    assert exc.message == "Booking BK123 not found"
    assert exc.status_code == status.HTTP_404_NOT_FOUND

def test_booking_not_found_error_without_id():
    # Act
    exc = BookingNotFoundError()
    
    # Assert
    assert exc.message == "Booking not found"
    assert exc.status_code == status.HTTP_404_NOT_FOUND

def test_flight_not_found_error_with_id():
    # Act
    exc = FlightNotFoundError("FL123")
    
    # Assert
    assert exc.message == "Flight FL123 not found"
    assert exc.status_code == status.HTTP_404_NOT_FOUND

def test_flight_not_found_error_without_id():
    # Act
    exc = FlightNotFoundError()
    
    # Assert
    assert exc.message == "Flight not found"
    assert exc.status_code == status.HTTP_404_NOT_FOUND

def test_passenger_not_found_error_with_id():
    # Act
    exc = PassengerNotFoundError("PS123")
    
    # Assert
    assert exc.message == "Passenger PS123 not found"
    assert exc.status_code == status.HTTP_404_NOT_FOUND

def test_passenger_not_found_error_without_id():
    # Act
    exc = PassengerNotFoundError()
    
    # Assert
    assert exc.message == "Passenger not found"
    assert exc.status_code == status.HTTP_404_NOT_FOUND

def test_no_seats_available_error():
    # Act
    exc = NoSeatsAvailableError()
    
    # Assert
    assert exc.message == "No seats available"
    assert exc.status_code == status.HTTP_409_CONFLICT

def test_already_checked_in_error_with_id():
    # Act
    exc = AlreadyCheckedInError("BK123")
    
    # Assert
    assert exc.message == "Booking BK123 already checked in"
    assert exc.status_code == status.HTTP_409_CONFLICT

def test_already_checked_in_error_without_id():
    # Act
    exc = AlreadyCheckedInError()
    
    # Assert
    assert exc.message == "Already checked in"
    assert exc.status_code == status.HTTP_409_CONFLICT

def test_passenger_mismatch_error():
    # Act
    exc = PassengerMismatchError()
    
    # Assert
    assert exc.message == "Passenger ID mismatch"
    assert exc.status_code == status.HTTP_400_BAD_REQUEST

def test_checkin_window_error():
    # Act
    exc = CheckinWindowError("Check-in window closed")
    
    # Assert
    assert exc.message == "Check-in window closed"
    assert exc.status_code == status.HTTP_409_CONFLICT

def test_unauthorized_access_error_default():
    # Act
    exc = UnauthorizedAccessError()
    
    # Assert
    assert exc.message == "Unauthorized access"
    assert exc.status_code == status.HTTP_401_UNAUTHORIZED

def test_unauthorized_access_error_custom():
    # Act
    exc = UnauthorizedAccessError("Custom unauthorized message")
    
    # Assert
    assert exc.message == "Custom unauthorized message"
    assert exc.status_code == status.HTTP_401_UNAUTHORIZED

def test_business_validation_error():
    # Act
    exc = BusinessValidationError("Validation failed")
    
    # Assert
    assert exc.message == "Validation failed"
    assert exc.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_exception_inheritance():
    # Act & Assert
    assert issubclass(BookingNotFoundError, BaseBusinessException)
    assert issubclass(FlightNotFoundError, BaseBusinessException)
    assert issubclass(PassengerNotFoundError, BaseBusinessException)
    assert issubclass(NoSeatsAvailableError, BaseBusinessException)
    assert issubclass(AlreadyCheckedInError, BaseBusinessException)
    assert issubclass(PassengerMismatchError, BaseBusinessException)
    assert issubclass(CheckinWindowError, BaseBusinessException)
    assert issubclass(UnauthorizedAccessError, BaseBusinessException)
    assert issubclass(BusinessValidationError, BaseBusinessException)