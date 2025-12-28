from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
import logging

from models import Booking, Flight
from app.shared.exceptions import BookingNotFoundError

logger = logging.getLogger(__name__)

class IBookingRepository(ABC):
    @abstractmethod
    async def find_by_id(self, booking_id: str) -> Optional[Booking]:
        pass
    
    @abstractmethod
    async def save(self, booking: Booking) -> Booking:
        pass
    
    @abstractmethod
    async def update_status(self, booking_id: str, status: str) -> None:
        pass
    
    @abstractmethod
    async def find_booking_with_flight(self, booking_id: str) -> Optional[tuple]:
        pass

class BookingRepository(IBookingRepository):
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def find_by_id(self, booking_id: str) -> Optional[Booking]:
        result = await self.db.execute(select(Booking).where(Booking.booking_id == booking_id))
        return result.scalar_one_or_none()
    
    async def save(self, booking: Booking) -> Booking:
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
    
    async def find_booking_with_flight(self, booking_id: str) -> Optional[tuple]:
        result = await self.db.execute(
            select(Booking, Flight)
            .join(Flight)
            .where(Booking.booking_id == booking_id)
        )
        return result.first()