from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from database import get_db
from schemas import BookingCreate, BookingResponse
from app.shared.auth import get_current_active_user
from app.core.user_models import User
from app.booking.booking_service import BookingService

# Security and logging setup
security = HTTPBearer()
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/bookings", 
    tags=["bookings"],
    dependencies=[Depends(security)]
)

# Dependency injection
def get_booking_service(db: AsyncSession = Depends(get_db)) -> BookingService:
    return BookingService(db)

@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_active_user),
    booking_service: BookingService = Depends(get_booking_service)
) -> BookingResponse:
    """Create a new booking"""
    return await booking_service.create_booking(booking_data, current_user.username)

@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: str,
    current_user: User = Depends(get_current_active_user),
    booking_service: BookingService = Depends(get_booking_service)
) -> BookingResponse:
    """Get booking by ID"""
    return await booking_service.get_booking_by_id(booking_id)

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_booking(
    booking_id: str,
    current_user: User = Depends(get_current_active_user),
    booking_service: BookingService = Depends(get_booking_service)
) -> None:
    """Cancel a booking"""
    await booking_service.cancel_booking(booking_id, current_user.username)