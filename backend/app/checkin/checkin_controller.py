from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict
import logging

from database import get_db
from schemas import CheckinRequest, BoardingPassResponse
from app.shared.auth import get_current_active_user
from app.core.user_models import User
from app.checkin.checkin_service import CheckinService

# Security and logging setup
security = HTTPBearer()
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/checkin", 
    tags=["checkin"],
    dependencies=[Depends(security)]
)

# Dependency injection
def get_checkin_service(db: AsyncSession = Depends(get_db)) -> CheckinService:
    return CheckinService(db)

@router.post("", response_model=BoardingPassResponse, status_code=status.HTTP_201_CREATED)
async def process_checkin(
    checkin_data: CheckinRequest,
    current_user: User = Depends(get_current_active_user),
    checkin_service: CheckinService = Depends(get_checkin_service)
) -> BoardingPassResponse:
    """Perform web check-in"""
    return await checkin_service.process_checkin(checkin_data, current_user.username)

@router.get("/{checkin_id}", response_model=BoardingPassResponse)
async def get_boarding_pass(
    checkin_id: str,
    current_user: User = Depends(get_current_active_user),
    checkin_service: CheckinService = Depends(get_checkin_service)
) -> BoardingPassResponse:
    """Get boarding pass by check-in ID"""
    return await checkin_service.get_boarding_pass(checkin_id)

@router.get("/status/{booking_id}")
async def get_checkin_status(
    booking_id: str,
    current_user: User = Depends(get_current_active_user),
    checkin_service: CheckinService = Depends(get_checkin_service)
) -> Dict:
    """Check if booking is already checked in"""
    return await checkin_service.get_checkin_status(booking_id)