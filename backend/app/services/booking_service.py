from fastapi import HTTPException, status
from datetime import datetime

from app.repositories.booking_repository import BookingRepository
from app.repositories.flight_repository import FlightRepository
from app.repositories.passenger_repository import PassengerRepository
from app.repositories.checkin_repository import CheckinRepository
from app.core.schemas import BookingCreate, BookingResponse, CheckinRequest, BoardingPassResponse
from app.core.utils import assign_seat, generate_boarding_pass_number, get_boarding_group, validate_checkin_window

class BookingService:
    def __init__(self, booking_repo: BookingRepository, flight_repo: FlightRepository, 
                 passenger_repo: PassengerRepository, checkin_repo: CheckinRepository):
        self.booking_repo = booking_repo
        self.flight_repo = flight_repo
        self.passenger_repo = passenger_repo
        self.checkin_repo = checkin_repo

    async def create_booking(self, booking_data: BookingCreate) -> BookingResponse:
        # Validate flight exists
        flight = await self.flight_repo.get_by_id(booking_data.flight_id)
        if not flight:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found")
        
        # Validate passenger exists
        passenger = await self.passenger_repo.get_by_id(booking_data.passenger_id)
        if not passenger:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Passenger not found")
        
        # Check seat availability
        if flight.available_seats <= 0:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No seats available")
        
        # Assign seat if not provided
        seat_number = booking_data.seat_number or assign_seat(flight.total_seats, flight.available_seats)
        
        # Create booking
        booking = await self.booking_repo.create(booking_data, seat_number)
        
        # Update available seats
        await self.flight_repo.update_available_seats(booking_data.flight_id, -1)
        
        return BookingResponse.model_validate(booking)

    async def get_booking(self, booking_id: str) -> BookingResponse:
        booking = await self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        return BookingResponse.model_validate(booking)

    async def cancel_booking(self, booking_id: str) -> None:
        booking = await self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        
        # Update booking status
        await self.booking_repo.update_status(booking_id, "cancelled")
        
        # Restore seat availability
        await self.flight_repo.update_available_seats(booking.flight_id, 1)

    async def checkin(self, checkin_data: CheckinRequest) -> BoardingPassResponse:
        # Get booking with flight info
        booking_flight = await self.booking_repo.get_with_flight(checkin_data.booking_id)
        if not booking_flight:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        
        booking, flight = booking_flight
        
        # Validate passenger ID
        if booking.passenger_id != checkin_data.passenger_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passenger ID mismatch")
        
        # Check if already checked in
        existing_checkin = await self.checkin_repo.get_by_booking_id(checkin_data.booking_id)
        if existing_checkin:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already checked in")
        
        # Validate check-in window
        is_valid, error_msg = validate_checkin_window(flight.departure_time)
        if not is_valid:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error_msg)
        
        # Create check-in record
        boarding_pass_number = generate_boarding_pass_number(flight.flight_id, booking.booking_id)
        boarding_group = get_boarding_group(booking.seat_number)
        
        checkin_record = await self.checkin_repo.create(
            checkin_data.booking_id, boarding_pass_number, "A1", boarding_group
        )
        
        # Update booking status
        await self.booking_repo.update_status(checkin_data.booking_id, "checked_in")
        
        return BoardingPassResponse(
            checkin_id=checkin_record.checkin_id,
            boarding_pass_number=checkin_record.boarding_pass_number,
            flight_id=flight.flight_id,
            seat_number=booking.seat_number,
            boarding_group=checkin_record.boarding_group,
            gate_number=checkin_record.gate_number,
            checkin_time=checkin_record.checkin_time
        )

    async def get_boarding_pass(self, checkin_id: str) -> BoardingPassResponse:
        checkin_data = await self.checkin_repo.get_with_booking_and_flight(checkin_id)
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

    async def get_checkin_status(self, booking_id: str) -> dict:
        checkin = await self.checkin_repo.get_by_booking_id(booking_id)
        return {
            "booking_id": booking_id,
            "checked_in": checkin is not None,
            "checkin_id": checkin.checkin_id if checkin else None,
            "timestamp": datetime.utcnow()
        }