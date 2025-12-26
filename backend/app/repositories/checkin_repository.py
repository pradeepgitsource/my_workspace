from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.core.models import CheckinRecord, Booking, Flight

class CheckinRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, booking_id: str, boarding_pass_number: str, 
                    gate_number: str, boarding_group: str) -> CheckinRecord:
        checkin = CheckinRecord(
            booking_id=booking_id,
            boarding_pass_number=boarding_pass_number,
            gate_number=gate_number,
            boarding_group=boarding_group
        )
        self.db.add(checkin)
        await self.db.commit()
        await self.db.refresh(checkin)
        return checkin

    async def get_by_id(self, checkin_id: str) -> Optional[CheckinRecord]:
        result = await self.db.execute(select(CheckinRecord).where(CheckinRecord.checkin_id == checkin_id))
        return result.scalar_one_or_none()

    async def get_by_booking_id(self, booking_id: str) -> Optional[CheckinRecord]:
        result = await self.db.execute(select(CheckinRecord).where(CheckinRecord.booking_id == booking_id))
        return result.scalar_one_or_none()

    async def get_with_booking_and_flight(self, checkin_id: str) -> Optional[tuple[CheckinRecord, Booking, Flight]]:
        result = await self.db.execute(
            select(CheckinRecord, Booking, Flight)
            .join(Booking)
            .join(Flight)
            .where(CheckinRecord.checkin_id == checkin_id)
        )
        return result.first()