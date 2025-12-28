from abc import ABC, abstractmethod
from typing import Optional
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from models import Booking, CheckinRecord
from schemas import BookingCreate, BookingResponse, CheckinRequest, BoardingPassResponse
from utils import assign_seat, generate_boarding_pass_number, get_boarding_group, validate_checkin_window
from app.repositories.booking_checkin_repository import (
    BookingRepository, FlightRepository, CheckinRepository, PassengerRepository
)
from app.core.exceptions import (
    BookingNotFoundError, FlightNotFoundError, PassengerNotFoundError,
    NoSeatsAvailableError, AlreadyCheckedInError, PassengerMismatchError,
    CheckinWindowError
)

logger = logging.getLogger(__name__)

class BookingServiceInterface(ABC):
    @abstractmethod
    async def create_booking(self, booking_data: BookingCreate, user_id: str) -> BookingResponse:
        pass
    
    @abstractmethod
    async def get_booking(self, booking_id: str) -> BookingResponse:
        pass
    
    @abstractmethod
    async def cancel_booking(self, booking_id: str, user_id: str) -> None:
        pass

class CheckinServiceInterface(ABC):
    @abstractmethod
    async def checkin(self, checkin_data: CheckinRequest, user_id: str) -> BoardingPassResponse:
        pass
    
    @abstractmethod
    async def get_boarding_pass(self, checkin_id: str) -> BoardingPassResponse:
        pass
    
    @abstractmethod
    async def get_checkin_status(self, booking_id: str) -> dict:
        pass

class BookingService(BookingServiceInterface):
    def __init__(self, db: AsyncSession):
        self.booking_repo = BookingRepository(db)
        self.flight_repo = FlightRepository(db)
        self.passenger_repo = PassengerRepository(db)
        self.db = db
    
    async def create_booking(self, booking_data: BookingCreate, user_id: str) -> BookingResponse:
        logger.info(f"Creating booking for user {user_id}")
        
        try:
            # Validate entities exist
            flight = await self.flight_repo.get_by_id(booking_data.flight_id)
            if not flight:
                raise FlightNotFoundError()
            
            passenger = await self.passenger_repo.get_by_id(booking_data.passenger_id)
            if not passenger:
                raise PassengerNotFoundError()
            
            # Validate business rules
            if flight.available_seats <= 0:
                raise NoSeatsAvailableError()
            
            # Assign seat
            seat_number = booking_data.seat_number or assign_seat(flight.total_seats, flight.available_seats)
            
            # Create booking
            booking = Booking(
                flight_id=booking_data.flight_id,
                passenger_id=booking_data.passenger_id,
                seat_number=seat_number
            )
            
            # Update available seats
            await self.flight_repo.update_available_seats(booking_data.flight_id, -1)
            
            # Save booking
            booking = await self.booking_repo.create(booking)
            
            logger.info(f"Booking {booking.booking_id} created successfully")
            return booking
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Booking creation failed: {str(e)}")
            raise
    
    async def get_booking(self, booking_id: str) -> BookingResponse:
        booking = await self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise BookingNotFoundError()
        return booking
    
    async def cancel_booking(self, booking_id: str, user_id: str) -> None:
        logger.info(f"Cancelling booking {booking_id} for user {user_id}")
        
        try:
            booking = await self.booking_repo.get_by_id(booking_id)
            if not booking:
                raise BookingNotFoundError()
            
            # Update booking status
            await self.booking_repo.update_status(booking_id, "cancelled")
            
            # Restore seat availability
            await self.flight_repo.update_available_seats(booking.flight_id, 1)
            
            await self.db.commit()
            logger.info(f"Booking {booking_id} cancelled successfully")
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Booking cancellation failed: {str(e)}")
            raise

class CheckinService(CheckinServiceInterface):
    def __init__(self, db: AsyncSession):
        self.booking_repo = BookingRepository(db)
        self.checkin_repo = CheckinRepository(db)
        self.db = db
    
    async def checkin(self, checkin_data: CheckinRequest, user_id: str) -> BoardingPassResponse:
        logger.info(f"Processing check-in for booking {checkin_data.booking_id}")
        
        try:
            # Get booking with flight info
            booking_flight = await self.booking_repo.get_booking_with_flight(checkin_data.booking_id)
            if not booking_flight:
                raise BookingNotFoundError()
            
            booking, flight = booking_flight
            
            # Validate passenger ID
            if booking.passenger_id != checkin_data.passenger_id:
                raise PassengerMismatchError()
            
            # Check if already checked in
            existing_checkin = await self.checkin_repo.get_by_booking_id(checkin_data.booking_id)
            if existing_checkin:
                raise AlreadyCheckedInError()
            
            # Validate check-in window
            is_valid, error_msg = validate_checkin_window(flight.departure_time)
            if not is_valid:
                raise CheckinWindowError(error_msg)
            
            # Create check-in record
            boarding_pass_number = generate_boarding_pass_number(flight.flight_id, booking.booking_id)
            boarding_group = get_boarding_group(booking.seat_number)
            
            checkin_record = CheckinRecord(
                booking_id=checkin_data.booking_id,
                boarding_pass_number=boarding_pass_number,
                gate_number="A1",
                boarding_group=boarding_group
            )
            
            # Update booking status
            await self.booking_repo.update_status(checkin_data.booking_id, "checked_in")
            
            # Save checkin record
            checkin_record = await self.checkin_repo.create(checkin_record)
            
            logger.info(f"Check-in completed for booking {checkin_data.booking_id}")
            
            return BoardingPassResponse(
                checkin_id=checkin_record.checkin_id,
                boarding_pass_number=checkin_record.boarding_pass_number,
                flight_id=flight.flight_id,
                seat_number=booking.seat_number,
                boarding_group=checkin_record.boarding_group,
                gate_number=checkin_record.gate_number,
                checkin_time=checkin_record.checkin_time
            )
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Check-in failed for booking {checkin_data.booking_id}: {str(e)}")
            raise
    
    async def get_boarding_pass(self, checkin_id: str) -> BoardingPassResponse:
        checkin_data = await self.checkin_repo.get_by_id(checkin_id)
        if not checkin_data:
            raise BookingNotFoundError("Check-in not found")
        
        checkin_record, booking, flight = checkin_data
        
        return BoardingPassResponse(
            checkin_id=checkin_record.checkin_id,
            boarding_pass_number=checkin_record.boarding_pass_number,
            flight_id=flight.flight_id,
            seat_number=booking.seat_number,
            boarding_group=checkin_record.boarding_group,
            gate_number=checkin_record.gate_number,
            checkin_time=checkin_record.checkin_time
        )
    
    async def get_checkin_status(self, booking_id: str) -> dict:
        from datetime import datetime
        
        checkin = await self.checkin_repo.get_by_booking_id(booking_id)
        
        return {
            "booking_id": booking_id,
            "checked_in": checkin is not None,
            "checkin_id": checkin.checkin_id if checkin else None,
            "timestamp": datetime.utcnow()
        }