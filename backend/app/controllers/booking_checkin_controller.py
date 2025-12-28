from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict
import logging

from database import get_db
from schemas import BookingCreate, BookingResponse, CheckinRequest, BoardingPassResponse
from app.core.dependencies import get_current_active_user
from app.core.user_models import User
from app.services.booking_checkin_service import BookingService, CheckinService

# Security and logging setup
security = HTTPBearer()
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api", 
    tags=["bookings", "checkin"],
    dependencies=[Depends(security)]
)

# Dependency injection
def get_booking_service(db: AsyncSession = Depends(get_db)) -> BookingService:
    return BookingService(db)

def get_checkin_service(db: AsyncSession = Depends(get_db)) -> CheckinService:
    return CheckinService(db)

# Booking Controller
@router.post("/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_active_user),
    booking_service: BookingService = Depends(get_booking_service)
) -> BookingResponse:
    """Create a new booking"""
    return await booking_service.create_booking(booking_data, current_user.username)

@router.get("/bookings/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: str,
    current_user: User = Depends(get_current_active_user),
    booking_service: BookingService = Depends(get_booking_service)
) -> BookingResponse:
    """Get booking by ID"""
    return await booking_service.get_booking(booking_id)

@router.delete("/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_booking(
    booking_id: str,
    current_user: User = Depends(get_current_active_user),
    booking_service: BookingService = Depends(get_booking_service)
) -> None:
    """Cancel a booking"""
    await booking_service.cancel_booking(booking_id, current_user.username)

# Checkin Controller
@router.post("/checkin", response_model=BoardingPassResponse, status_code=status.HTTP_201_CREATED)
async def checkin(
    checkin_data: CheckinRequest,
    current_user: User = Depends(get_current_active_user),
    checkin_service: CheckinService = Depends(get_checkin_service)
) -> BoardingPassResponse:
    """Perform web check-in"""
    return await checkin_service.checkin(checkin_data, current_user.username)

@router.get("/checkin/{checkin_id}", response_model=BoardingPassResponse)
async def get_boarding_pass(
    checkin_id: str,
    current_user: User = Depends(get_current_active_user),
    checkin_service: CheckinService = Depends(get_checkin_service)
) -> BoardingPassResponse:
    """Get boarding pass by check-in ID"""
    return await checkin_service.get_boarding_pass(checkin_id)

@router.get("/bookings/{booking_id}/checkin-status")
async def get_checkin_status(
    booking_id: str,
    current_user: User = Depends(get_current_active_user),
    checkin_service: CheckinService = Depends(get_checkin_service)
) -> Dict:
    """Check if booking is already checked in"""
    return await checkin_service.get_checkin_status(booking_id)