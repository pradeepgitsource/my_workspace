from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from models import CheckinRecord, Booking, Flight

logger = logging.getLogger(__name__)

class ICheckinRepository(ABC):
    @abstractmethod
    async def find_by_booking_id(self, booking_id: str) -> Optional[CheckinRecord]:
        pass
    
    @abstractmethod
    async def save(self, checkin: CheckinRecord) -> CheckinRecord:
        pass
    
    @abstractmethod
    async def find_checkin_details_by_id(self, checkin_id: str) -> Optional[tuple]:
        pass

class CheckinRepository(ICheckinRepository):
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def find_by_booking_id(self, booking_id: str) -> Optional[CheckinRecord]:
        result = await self.db.execute(select(CheckinRecord).where(CheckinRecord.booking_id == booking_id))
        return result.scalar_one_or_none()
    
    async def save(self, checkin: CheckinRecord) -> CheckinRecord:
        self.db.add(checkin)
        await self.db.commit()
        await self.db.refresh(checkin)
        return checkin
    
    async def find_checkin_details_by_id(self, checkin_id: str) -> Optional[tuple]:
        result = await self.db.execute(
            select(CheckinRecord, Booking, Flight)
            .join(Booking)
            .join(Flight)
            .where(CheckinRecord.checkin_id == checkin_id)
        )
        return result.first()