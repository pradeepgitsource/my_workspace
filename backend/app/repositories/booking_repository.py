from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Optional

from app.core.models import Booking, Flight
from app.core.schemas import BookingCreate

class BookingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, booking_data: BookingCreate, seat_number: str) -> Booking:
        booking = Booking(
            flight_id=booking_data.flight_id,
            passenger_id=booking_data.passenger_id,
            seat_number=seat_number
        )
        self.db.add(booking)
        await self.db.commit()
        await self.db.refresh(booking)
        return booking

    async def get_by_id(self, booking_id: str) -> Optional[Booking]:
        result = await self.db.execute(select(Booking).where(Booking.booking_id == booking_id))
        return result.scalar_one_or_none()

    async def get_with_flight(self, booking_id: str) -> Optional[tuple[Booking, Flight]]:
        result = await self.db.execute(
            select(Booking, Flight)
            .join(Flight)
            .where(Booking.booking_id == booking_id)
        )
        return result.first()

    async def update_status(self, booking_id: str, status: str) -> None:
        await self.db.execute(
            update(Booking)
            .where(Booking.booking_id == booking_id)
            .values(booking_status=status)
        )
        await self.db.commit()