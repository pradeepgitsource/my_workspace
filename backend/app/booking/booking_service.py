from abc import ABC, abstractmethod
from typing import Optional
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from models import Booking
from schemas import BookingCreate, BookingResponse
from utils import assign_seat
from app.booking.booking_repository import BookingRepository
from app.flight.flight_repository import FlightRepository
from app.passenger.passenger_repository import PassengerRepository
from app.shared.exceptions import (
    BookingNotFoundError, FlightNotFoundError, PassengerNotFoundError,
    NoSeatsAvailableError
)

logger = logging.getLogger(__name__)

class IBookingService(ABC):
    @abstractmethod
    async def create_booking(self, booking_data: BookingCreate, user_id: str) -> BookingResponse:
        pass
    
    @abstractmethod
    async def get_booking_by_id(self, booking_id: str) -> BookingResponse:
        pass
    
    @abstractmethod
    async def cancel_booking(self, booking_id: str, user_id: str) -> None:
        pass

class BookingService(IBookingService):
    def __init__(self, db: AsyncSession):
        self.booking_repository = BookingRepository(db)
        self.flight_repository = FlightRepository(db)
        self.passenger_repository = PassengerRepository(db)
        self.db = db
    
    async def create_booking(self, booking_data: BookingCreate, user_id: str) -> BookingResponse:
        logger.info(f"Creating booking for user {user_id}")
        
        try:
            # Validate entities exist
            flight = await self.flight_repository.find_by_id(booking_data.flight_id)
            if not flight:
                raise FlightNotFoundError(booking_data.flight_id)
            
            passenger = await self.passenger_repository.find_by_id(booking_data.passenger_id)
            if not passenger:
                raise PassengerNotFoundError(booking_data.passenger_id)
            
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
            await self.flight_repository.update_available_seats(booking_data.flight_id, -1)
            
            # Save booking
            booking = await self.booking_repository.save(booking)
            
            logger.info(f"Booking {booking.booking_id} created successfully")
            return booking
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Booking creation failed: {str(e)}")
            raise
    
    async def get_booking_by_id(self, booking_id: str) -> BookingResponse:
        booking = await self.booking_repository.find_by_id(booking_id)
        if not booking:
            raise BookingNotFoundError(booking_id)
        return booking
    
    async def cancel_booking(self, booking_id: str, user_id: str) -> None:
        logger.info(f"Cancelling booking {booking_id} for user {user_id}")
        
        try:
            booking = await self.booking_repository.find_by_id(booking_id)
            if not booking:
                raise BookingNotFoundError(booking_id)
            
            # Update booking status
            await self.booking_repository.update_status(booking_id, "cancelled")
            
            # Restore seat availability
            await self.flight_repository.update_available_seats(booking.flight_id, 1)
            
            await self.db.commit()
            logger.info(f"Booking {booking_id} cancelled successfully")
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Booking cancellation failed: {str(e)}")
            raise