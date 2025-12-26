from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database import get_db
from models import Flight
from schemas import FlightCreate, FlightResponse

router = APIRouter(prefix="/api/flights", tags=["flights"])

@router.post("", response_model=FlightResponse, status_code=status.HTTP_201_CREATED)
async def create_flight(
    flight_data: FlightCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new flight"""
    # Check if flight already exists
    result = await db.execute(select(Flight).where(Flight.flight_id == flight_data.flight_id))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Flight already exists"
        )
    
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
    
    db.add(flight)
    await db.commit()
    await db.refresh(flight)
    
    return flight

@router.get("", response_model=List[FlightResponse])
async def get_flights(db: AsyncSession = Depends(get_db)):
    """Get all flights"""
    result = await db.execute(select(Flight))
    flights = result.scalars().all()
    return flights

@router.get("/{flight_id}", response_model=FlightResponse)
async def get_flight(flight_id: str, db: AsyncSession = Depends(get_db)):
    """Get flight by ID"""
    result = await db.execute(select(Flight).where(Flight.flight_id == flight_id))
    flight = result.scalar_one_or_none()
    
    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flight not found"
        )
    
    return flight