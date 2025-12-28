from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime

from database import get_db
from models import Booking, Flight, Passenger, CheckinRecord
from schemas import BookingCreate, BookingResponse, CheckinRequest, BoardingPassResponse
from utils import assign_seat, generate_boarding_pass_number, get_boarding_group, validate_checkin_window
from app.core.dependencies import get_current_active_user
from app.core.user_models import User

router = APIRouter(prefix="/api", tags=["bookings", "checkin"])

@router.post("/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new booking"""
    # Validate flight exists
    flight_result = await db.execute(select(Flight).where(Flight.flight_id == booking_data.flight_id))
    flight = flight_result.scalar_one_or_none()
    if not flight:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
    
    # Validate passenger exists
    passenger_result = await db.execute(select(Passenger).where(Passenger.passenger_id == booking_data.passenger_id))
    passenger = passenger_result.scalar_one_or_none()
    if not passenger:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Passenger not found")
    
    # Check seat availability
    if flight.available_seats <= 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No seats available")
    
    # Assign seat if not provided
    seat_number = booking_data.seat_number or assign_seat(flight.total_seats, flight.available_seats)
    
    booking = Booking(
        flight_id=booking_data.flight_id,
        passenger_id=booking_data.passenger_id,
        seat_number=seat_number
    )
    
    db.add(booking)
    
    # Update available seats
    await db.execute(
        update(Flight)
        .where(Flight.flight_id == booking_data.flight_id)
        .values(available_seats=Flight.available_seats - 1)
    )
    
    await db.commit()
    await db.refresh(booking)
    
    return booking

@router.get("/bookings/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: str, db: AsyncSession = Depends(get_db)):
    """Get booking by ID"""
    result = await db.execute(select(Booking).where(Booking.booking_id == booking_id))
    booking = result.scalar_one_or_none()
    
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    
    return booking

@router.delete("/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_booking(booking_id: str, db: AsyncSession = Depends(get_db)):
    """Cancel a booking"""
    result = await db.execute(select(Booking).where(Booking.booking_id == booking_id))
    booking = result.scalar_one_or_none()
    
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    
    # Update booking status
    await db.execute(
        update(Booking)
        .where(Booking.booking_id == booking_id)
        .values(booking_status="cancelled")
    )
    
    # Restore seat availability
    await db.execute(
        update(Flight)
        .where(Flight.flight_id == booking.flight_id)
        .values(available_seats=Flight.available_seats + 1)
    )
    
    await db.commit()

@router.post("/checkin", response_model=BoardingPassResponse, status_code=status.HTTP_201_CREATED)
async def checkin(
    checkin_data: CheckinRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Perform web check-in"""
    # Get booking with flight info
    result = await db.execute(
        select(Booking, Flight)
        .join(Flight)
        .where(Booking.booking_id == checkin_data.booking_id)
    )
    booking_flight = result.first()
    
    if not booking_flight:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    
    booking, flight = booking_flight
    
    # Validate passenger ID
    if booking.passenger_id != checkin_data.passenger_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passenger ID mismatch")
    
    # Check if already checked in
    checkin_result = await db.execute(select(CheckinRecord).where(CheckinRecord.booking_id == checkin_data.booking_id))
    if checkin_result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already checked in")
    
    # Validate check-in window
    is_valid, error_msg = validate_checkin_window(flight.departure_time)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error_msg)
    
    # Create check-in record
    boarding_pass_number = generate_boarding_pass_number(flight.flight_id, booking.booking_id)
    boarding_group = get_boarding_group(booking.seat_number)
    
    checkin_record = CheckinRecord(
        booking_id=checkin_data.booking_id,
        boarding_pass_number=boarding_pass_number,
        gate_number="A1",
        boarding_group=boarding_group
    )
    
    db.add(checkin_record)
    
    # Update booking status
    await db.execute(
        update(Booking)
        .where(Booking.booking_id == checkin_data.booking_id)
        .values(booking_status="checked_in")
    )
    
    await db.commit()
    await db.refresh(checkin_record)
    
    # Return boarding pass info
    return BoardingPassResponse(
        checkin_id=checkin_record.checkin_id,
        boarding_pass_number=checkin_record.boarding_pass_number,
        flight_id=flight.flight_id,
        seat_number=booking.seat_number,
        boarding_group=checkin_record.boarding_group,
        gate_number=checkin_record.gate_number,
        checkin_time=checkin_record.checkin_time
    )

@router.get("/checkin/{checkin_id}", response_model=BoardingPassResponse)
async def get_boarding_pass(checkin_id: str, db: AsyncSession = Depends(get_db)):
    """Get boarding pass by check-in ID"""
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
async def get_checkin_status(booking_id: str, db: AsyncSession = Depends(get_db)):
    """Check if booking is already checked in"""
    result = await db.execute(select(CheckinRecord).where(CheckinRecord.booking_id == booking_id))
    checkin = result.scalar_one_or_none()
    
    return {
        "booking_id": booking_id,
        "checked_in": checkin is not None,
        "checkin_id": checkin.checkin_id if checkin else None,
        "timestamp": datetime.utcnow()
    }