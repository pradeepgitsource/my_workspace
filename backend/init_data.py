import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal, create_tables
from models import Flight, Passenger, Booking

async def init_sample_data():
    """Initialize sample data in PostgreSQL"""
    
    # Create tables first
    await create_tables()
    
    async with AsyncSessionLocal() as db:
        # Sample flights
        flights = [
            Flight(
                flight_id="AA123",
                departure_airport="JFK",
                arrival_airport="LAX",
                departure_time=datetime.utcnow() + timedelta(hours=6),
                arrival_time=datetime.utcnow() + timedelta(hours=12),
                aircraft_type="Boeing 737-800",
                total_seats=180,
                available_seats=179
            ),
            Flight(
                flight_id="UA456",
                departure_airport="ORD",
                arrival_airport="SFO",
                departure_time=datetime.utcnow() + timedelta(hours=8),
                arrival_time=datetime.utcnow() + timedelta(hours=12),
                aircraft_type="Airbus A320",
                total_seats=150,
                available_seats=150
            ),
            Flight(
                flight_id="DL789",
                departure_airport="ATL",
                arrival_airport="MIA",
                departure_time=datetime.utcnow() + timedelta(hours=4),
                arrival_time=datetime.utcnow() + timedelta(hours=6),
                aircraft_type="Boeing 757-200",
                total_seats=200,
                available_seats=200
            )
        ]
        
        for flight in flights:
            db.add(flight)
        
        # Sample passenger
        passenger = Passenger(
            passenger_id="P001",
            first_name="John",
            last_name="Doe",
            email="john.doe@email.com",
            phone="+1234567890",
            date_of_birth="1990-01-15"
        )
        db.add(passenger)
        
        # Sample booking
        booking = Booking(
            booking_id="B001",
            flight_id="AA123",
            passenger_id="P001",
            seat_number="12A"
        )
        db.add(booking)
        
        await db.commit()
        print("Sample data initialized successfully!")

if __name__ == "__main__":
    asyncio.run(init_sample_data())