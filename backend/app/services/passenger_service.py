from typing import List
from fastapi import HTTPException, status

from app.repositories.passenger_repository import PassengerRepository
from app.core.schemas import PassengerCreate, PassengerResponse, BookingResponse

class PassengerService:
    def __init__(self, passenger_repo: PassengerRepository):
        self.passenger_repo = passenger_repo

    async def create_passenger(self, passenger_data: PassengerCreate) -> PassengerResponse:
        # Check if email already exists
        existing_passenger = await self.passenger_repo.get_by_email(str(passenger_data.email))
        if existing_passenger:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        
        passenger = await self.passenger_repo.create(passenger_data)
        return PassengerResponse.model_validate(passenger)

    async def get_passenger(self, passenger_id: str) -> PassengerResponse:
        passenger = await self.passenger_repo.get_by_id(passenger_id)
        if not passenger:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Passenger not found"
            )
        return PassengerResponse.model_validate(passenger)

    async def get_passenger_bookings(self, passenger_id: str) -> List[BookingResponse]:
        # Verify passenger exists
        passenger = await self.passenger_repo.get_by_id(passenger_id)
        if not passenger:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Passenger not found"
            )
        
        bookings = await self.passenger_repo.get_bookings(passenger_id)
        return [BookingResponse.model_validate(booking) for booking in bookings]