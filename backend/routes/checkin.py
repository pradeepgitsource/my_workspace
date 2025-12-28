from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime
from typing import Optional
import logging

# Import the new controller
from app.controllers.booking_checkin_controller import router as booking_checkin_router

# Security and logging setup
security = HTTPBearer()
logger = logging.getLogger(__name__)

# Use the new SOLID architecture controller
router = booking_checkin_router

ss(
    checkin_id: str, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> BoardingPassResponse:
    """Get boarding pass by check-in ID"""
    logger.info(f"Fetching boarding pass {checkin_id}")
    
    result = await db.execute(
        select(CheckinRecord, Booking, Flight)
        .join(Booking)
        .join(Flight)
        .where(CheckinRecord.checkin_id == checkin_id)
    )
    checkin_data = result.first()
    
    if not checkin_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Check-in not found")
    
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

@router.get("/bookings/{booking_id}/checkin-status")
async def get_checkin_status(
    booking_id: str, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """Check if booking is already checked in"""
    logger.info(f"Checking status for booking {booking_id}")
    
    result = await db.execute(select(CheckinRecord).where(CheckinRecord.booking_id == booking_id))
    checkin = result.scalar_one_or_none()
    
    return {
        "booking_id": booking_id,
        "checked_in": checkin is not None,
        "checkin_id": checkin.checkin_id if checkin else None,
        "timestamp": datetime.utcnow()
    }