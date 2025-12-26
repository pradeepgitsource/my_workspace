from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database import get_db
from models import Passenger, Booking
from schemas import PassengerCreate, PassengerResponse, BookingResponse

router = APIRouter(prefix="/api/passengers", tags=["passengers"])

@router.post("", response_model=PassengerResponse, status_code=status.HTTP_201_CREATED)
async def create_passenger(
    passenger_data: PassengerCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new passenger"""
    # Check if email already exists
    result = await db.execute(select(Passenger).where(Passenger.email == passenger_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    passenger = Passenger(
        first_name=passenger_data.first_name,
        last_name=passenger_data.last_name,
        email=str(passenger_data.email),
        phone=passenger_data.phone,
        date_of_birth=passenger_data.date_of_birth
    )
    
    db.add(passenger)
    await db.commit()
    await db.refresh(passenger)
    
    return passenger

@router.get("/{passenger_id}", response_model=PassengerResponse)
async def get_passenger(passenger_id: str, db: AsyncSession = Depends(get_db)):
    """Get passenger by ID"""
    result = await db.execute(select(Passenger).where(Passenger.passenger_id == passenger_id))
    passenger = result.scalar_one_or_none()
    
    if not passenger:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Passenger not found"
        )
    
    return passenger

@router.get("/{passenger_id}/bookings", response_model=List[BookingResponse])
async def get_passenger_bookings(passenger_id: str, db: AsyncSession = Depends(get_db)):
    """Get all bookings for a passenger"""
    result = await db.execute(select(Booking).where(Booking.passenger_id == passenger_id))
    bookings = result.scalars().all()
    return bookings