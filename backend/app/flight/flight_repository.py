from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
import logging

from models import Flight

logger = logging.getLogger(__name__)

class IFlightRepository(ABC):
    @abstractmethod
    async def find_by_id(self, flight_id: str) -> Optional[Flight]:
        pass
    
    @abstractmethod
    async def update_available_seats(self, flight_id: str, seats: int) -> None:
        pass

class FlightRepository(IFlightRepository):
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def find_by_id(self, flight_id: str) -> Optional[Flight]:
        result = await self.db.execute(select(Flight).where(Flight.flight_id == flight_id))
        return result.scalar_one_or_none()
    
    async def update_available_seats(self, flight_id: str, seats: int) -> None:
        await self.db.execute(
            update(Flight)
            .where(Flight.flight_id == flight_id)
            .values(available_seats=Flight.available_seats + seats)
        )