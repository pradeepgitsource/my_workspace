from fastapi import FastAPI, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import List
import logging
import time

from app.core.database import create_tables, get_db
from app.repositories.flight_repository import FlightRepository
from app.repositories.passenger_repository import PassengerRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.checkin_repository import CheckinRepository
from app.services.flight_service import FlightService
from app.services.passenger_service import PassengerService
from app.services.booking_service import BookingService
from app.core.schemas import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Flight Web Check-in API",
    description="Modular flight check-in system with PostgreSQL",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"{request.method} {request.url.path} - {request.client.host}")
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
    return response

# Dependency injection
def get_flight_service(db: AsyncSession = Depends(get_db)) -> FlightService:
    return FlightService(FlightRepository(db))

def get_passenger_service(db: AsyncSession = Depends(get_db)) -> PassengerService:
    return PassengerService(PassengerRepository(db))

def get_booking_service(db: AsyncSession = Depends(get_db)) -> BookingService:
    return BookingService(
        BookingRepository(db),
        FlightRepository(db),
        PassengerRepository(db),
        CheckinRepository(db)
    )

# Routes
@app.post("/api/flights", response_model=FlightResponse, status_code=status.HTTP_201_CREATED, tags=["flights"])
async def create_flight(flight_data: FlightCreate, service: FlightService = Depends(get_flight_service)):
    return await service.create_flight(flight_data)

@app.get("/api/flights", response_model=List[FlightResponse], tags=["flights"])
async def get_flights(service: FlightService = Depends(get_flight_service)):
    return await service.get_all_flights()

@app.get("/api/flights/{flight_id}", response_model=FlightResponse, tags=["flights"])
async def get_flight(flight_id: str, service: FlightService = Depends(get_flight_service)):
    return await service.get_flight(flight_id)

@app.post("/api/passengers", response_model=PassengerResponse, status_code=status.HTTP_201_CREATED, tags=["passengers"])
async def create_passenger(passenger_data: PassengerCreate, service: PassengerService = Depends(get_passenger_service)):
    return await service.create_passenger(passenger_data)

@app.get("/api/passengers/{passenger_id}", response_model=PassengerResponse, tags=["passengers"])
async def get_passenger(passenger_id: str, service: PassengerService = Depends(get_passenger_service)):
    return await service.get_passenger(passenger_id)

@app.get("/api/passengers/{passenger_id}/bookings", response_model=List[BookingResponse], tags=["passengers"])
async def get_passenger_bookings(passenger_id: str, service: PassengerService = Depends(get_passenger_service)):
    return await service.get_passenger_bookings(passenger_id)

@app.post("/api/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED, tags=["bookings"])
async def create_booking(booking_data: BookingCreate, service: BookingService = Depends(get_booking_service)):
    return await service.create_booking(booking_data)

@app.get("/api/bookings/{booking_id}", response_model=BookingResponse, tags=["bookings"])
async def get_booking(booking_id: str, service: BookingService = Depends(get_booking_service)):
    return await service.get_booking(booking_id)

@app.delete("/api/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["bookings"])
async def cancel_booking(booking_id: str, service: BookingService = Depends(get_booking_service)):
    await service.cancel_booking(booking_id)

@app.post("/api/checkin", response_model=BoardingPassResponse, status_code=status.HTTP_201_CREATED, tags=["checkin"])
async def checkin(checkin_data: CheckinRequest, service: BookingService = Depends(get_booking_service)):
    return await service.checkin(checkin_data)

@app.get("/api/checkin/{checkin_id}", response_model=BoardingPassResponse, tags=["checkin"])
async def get_boarding_pass(checkin_id: str, service: BookingService = Depends(get_booking_service)):
    return await service.get_boarding_pass(checkin_id)

@app.get("/api/bookings/{booking_id}/checkin-status", tags=["checkin"])
async def get_checkin_status(booking_id: str, service: BookingService = Depends(get_booking_service)):
    return await service.get_checkin_status(booking_id)

@app.on_event("startup")
async def startup_event():
    logger.info("Creating database tables...")
    await create_tables()
    logger.info("Database tables created successfully")

@app.get("/")
async def root():
    return {
        "message": "Flight Web Check-in API",
        "version": "2.0.0",
        "status": "running",
        "architecture": "Modular with Repository Pattern",
        "database": "PostgreSQL",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "2.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting modular Flight Check-in API...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")