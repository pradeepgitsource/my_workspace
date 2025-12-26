from typing import List
from fastapi import HTTPException, status

from app.repositories.flight_repository import FlightRepository
from app.core.schemas import FlightCreate, FlightResponse
from app.core.models import Flight

class FlightService:
    def __init__(self, flight_repo: FlightRepository):
        self.flight_repo = flight_repo

    async def create_flight(self, flight_data: FlightCreate) -> FlightResponse:
        # Check if flight already exists
        existing_flight = await self.flight_repo.get_by_id(flight_data.flight_id)
        if existing_flight:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Flight already exists"
            )
        
        flight = await self.flight_repo.create(flight_data)
        return FlightResponse.model_validate(flight)

    async def get_flight(self, flight_id: str) -> FlightResponse:
        flight = await self.flight_repo.get_by_id(flight_id)
        if not flight:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flight not found"
            )
        return FlightResponse.model_validate(flight)

    async def get_all_flights(self) -> List[FlightResponse]:
        flights = await self.flight_repo.get_all()
        return [FlightResponse.model_validate(flight) for flight in flights]