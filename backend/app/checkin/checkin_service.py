from abc import ABC, abstractmethod
from typing import Dict
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from models import CheckinRecord
from schemas import CheckinRequest, BoardingPassResponse
from utils import generate_boarding_pass_number, get_boarding_group, validate_checkin_window
from app.booking.booking_repository import BookingRepository
from app.checkin.checkin_repository import CheckinRepository
from app.shared.exceptions import (
    BookingNotFoundError, AlreadyCheckedInError, PassengerMismatchError,
    CheckinWindowError
)

logger = logging.getLogger(__name__)

class ICheckinService(ABC):
    @abstractmethod
    async def process_checkin(self, checkin_data: CheckinRequest, user_id: str) -> BoardingPassResponse:
        pass
    
    @abstractmethod
    async def get_boarding_pass(self, checkin_id: str) -> BoardingPassResponse:
        pass
    
    @abstractmethod
    async def get_checkin_status(self, booking_id: str) -> Dict:
        pass

class CheckinService(ICheckinService):
    def __init__(self, db: AsyncSession):
        self.booking_repository = BookingRepository(db)
        self.checkin_repository = CheckinRepository(db)
        self.db = db
    
    async def process_checkin(self, checkin_data: CheckinRequest, user_id: str) -> BoardingPassResponse:
        logger.info(f"Processing check-in for booking {checkin_data.booking_id}")
        
        try:
            # Get booking with flight info
            booking_flight = await self.booking_repository.find_booking_with_flight(checkin_data.booking_id)
            if not booking_flight:
                raise BookingNotFoundError(checkin_data.booking_id)
            
            booking, flight = booking_flight
            
            # Validate passenger ID
            if booking.passenger_id != checkin_data.passenger_id:
                raise PassengerMismatchError()
            
            # Check if already checked in
            existing_checkin = await self.checkin_repository.find_by_booking_id(checkin_data.booking_id)
            if existing_checkin:
                raise AlreadyCheckedInError(checkin_data.booking_id)
            
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
            await self.booking_repository.update_status(checkin_data.booking_id, "checked_in")
            
            # Save checkin record
            checkin_record = await self.checkin_repository.save(checkin_record)
            
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
        checkin_data = await self.checkin_repository.find_checkin_details_by_id(checkin_id)
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
    
    async def get_checkin_status(self, booking_id: str) -> Dict:
        checkin = await self.checkin_repository.find_by_booking_id(booking_id)
        
        return {
            "booking_id": booking_id,
            "checked_in": checkin is not None,
            "checkin_id": checkin.checkin_id if checkin else None,
            "timestamp": datetime.utcnow()
        }