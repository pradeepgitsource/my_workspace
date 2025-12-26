from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.core.models import Passenger, Booking
from app.core.schemas import PassengerCreate

class PassengerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, passenger_data: PassengerCreate) -> Passenger:
        passenger = Passenger(
            first_name=passenger_data.first_name,
            last_name=passenger_data.last_name,
            email=str(passenger_data.email),
            phone=passenger_data.phone,
            date_of_birth=passenger_data.date_of_birth
        )
        self.db.add(passenger)
        await self.db.commit()
        await self.db.refresh(passenger)
        return passenger

    async def get_by_id(self, passenger_id: str) -> Optional[Passenger]:
        result = await self.db.execute(select(Passenger).where(Passenger.passenger_id == passenger_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[Passenger]:
        result = await self.db.execute(select(Passenger).where(Passenger.email == email))
        return result.scalar_one_or_none()

    async def get_bookings(self, passenger_id: str) -> List[Booking]:
        result = await self.db.execute(select(Booking).where(Booking.passenger_id == passenger_id))
        return result.scalars().all()