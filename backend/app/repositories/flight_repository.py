from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List, Optional

from app.core.models import Flight
from app.core.schemas import FlightCreate

class FlightRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, flight_data: FlightCreate) -> Flight:
        flight = Flight(
            flight_id=flight_data.flight_id,
            departure_airport=flight_data.departure_airport,
            arrival_airport=flight_data.arrival_airport,
            departure_time=flight_data.departure_time,
            arrival_time=flight_data.arrival_time,
            aircraft_type=flight_data.aircraft_type,
            total_seats=flight_data.total_seats,
            available_seats=flight_data.total_seats
        )
        self.db.add(flight)
        await self.db.commit()
        await self.db.refresh(flight)
        return flight

    async def get_by_id(self, flight_id: str) -> Optional[Flight]:
        result = await self.db.execute(select(Flight).where(Flight.flight_id == flight_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Flight]:
        result = await self.db.execute(select(Flight))
        return result.scalars().all()

    async def update_available_seats(self, flight_id: str, change: int) -> None:
        await self.db.execute(
            update(Flight)
            .where(Flight.flight_id == flight_id)
            .values(available_seats=Flight.available_seats + change)
        )
        await self.db.commit()