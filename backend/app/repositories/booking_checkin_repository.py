from abc import ABC, abstractmethod
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
import logging

from models import Booking, Flight, Passenger, CheckinRecord
from app.core.exceptions import (
    BookingNotFoundError, FlightNotFoundError, PassengerNotFoundError,
    NoSeatsAvailableError, AlreadyCheckedInError
)

logger = logging.getLogger(__name__)

class BookingRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_id(self, booking_id: str) -> Optional[Booking]:
        pass
    
    @abstractmethod
    async def create(self, booking: Booking) -> Booking:
        pass
    
    @abstractmethod
    async def update_status(self, booking_id: str, status: str) -> None:
        pass
    
    @abstractmethod
    async def get_booking_with_flight(self, booking_id: str) -> Optional[tuple]:
        pass

class FlightRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_id(self, flight_id: str) -> Optional[Flight]:
        pass
    
    @abstractmethod
    async def update_available_seats(self, flight_id: str, seats: int) -> None:
        pass

class CheckinRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_booking_id(self, booking_id: str) -> Optional[CheckinRecord]:
        pass
    
    @abstractmethod
    async def create(self, checkin: CheckinRecord) -> CheckinRecord:
        pass
    
    @abstractmethod
    async def get_by_id(self, checkin_id: str) -> Optional[tuple]:
        pass

class BookingRepository(BookingRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, booking_id: str) -> Optional[Booking]:
        result = await self.db.execute(select(Booking).where(Booking.booking_id == booking_id))
        return result.scalar_one_or_none()
    
    async def create(self, booking: Booking) -> Booking:
        self.db.add(booking)
        await self.db.commit()
        await self.db.refresh(booking)
        return booking
    
    async def update_status(self, booking_id: str, status: str) -> None:
        await self.db.execute(
            update(Booking)
            .where(Booking.booking_id == booking_id)
            .values(booking_status=status)
        )
    
    async def get_booking_with_flight(self, booking_id: str) -> Optional[tuple]:
        result = await self.db.execute(
            select(Booking, Flight)
            .join(Flight)
            .where(Booking.booking_id == booking_id)
        )
        return result.first()

class FlightRepository(FlightRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, flight_id: str) -> Optional[Flight]:
        result = await self.db.execute(select(Flight).where(Flight.flight_id == flight_id))
        return result.scalar_one_or_none()
    
    async def update_available_seats(self, flight_id: str, seats: int) -> None:
        await self.db.execute(
            update(Flight)
            .where(Flight.flight_id == flight_id)
            .values(available_seats=Flight.available_seats + seats)
        )

class CheckinRepository(CheckinRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_booking_id(self, booking_id: str) -> Optional[CheckinRecord]:
        result = await self.db.execute(select(CheckinRecord).where(CheckinRecord.booking_id == booking_id))
        return result.scalar_one_or_none()
    
    async def create(self, checkin: CheckinRecord) -> CheckinRecord:
        self.db.add(checkin)
        await self.db.commit()
        await self.db.refresh(checkin)
        return checkin
    
    async def get_by_id(self, checkin_id: str) -> Optional[tuple]:
        result = await self.db.execute(
            select(CheckinRecord, Booking, Flight)
            .join(Booking)
            .join(Flight)
            .where(CheckinRecord.checkin_id == checkin_id)
        )
        return result.first()

class PassengerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, passenger_id: str) -> Optional[Passenger]:
        result = await self.db.execute(select(Passenger).where(Passenger.passenger_id == passenger_id))
        return result.scalar_one_or_none()