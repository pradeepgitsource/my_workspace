from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from models import Passenger

logger = logging.getLogger(__name__)

class IPassengerRepository(ABC):
    @abstractmethod
    async def find_by_id(self, passenger_id: str) -> Optional[Passenger]:
        pass

class PassengerRepository(IPassengerRepository):
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def find_by_id(self, passenger_id: str) -> Optional[Passenger]:
        result = await self.db.execute(select(Passenger).where(Passenger.passenger_id == passenger_id))
        return result.scalar_one_or_none()