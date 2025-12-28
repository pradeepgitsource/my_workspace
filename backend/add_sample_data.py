import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from app.core.database import AsyncSessionLocal, create_tables
from app.core.models import Flight, Passenger, Booking

async def add_sample_data():
    """Add sample data to the database"""
    
    # Create tables first
    await create_tables()
    
    async with AsyncSessionLocal() as db:
        try:
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
                    available_seats=179,
                    status="scheduled"
                ),
                Flight(
                    flight_id="UA456",
                    departure_airport="ORD",
                    arrival_airport="SFO",
                    departure_time=datetime.utcnow() + timedelta(hours=8),
                    arrival_time=datetime.utcnow() + timedelta(hours=12),
                    aircraft_type="Airbus A320",
                    total_seats=150,
                    available_seats=150,
                    status="scheduled"
                ),
                Flight(
                    flight_id="DL789",
                    departure_airport="ATL",
                    arrival_airport="MIA",
                    departure_time=datetime.utcnow() + timedelta(hours=4),
                    arrival_time=datetime.utcnow() + timedelta(hours=6),
                    aircraft_type="Boeing 757-200",
                    total_seats=200,
                    available_seats=200,
                    status="scheduled"
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
                seat_number="12A",
                booking_status="confirmed"
            )
            db.add(booking)
            
            await db.commit()
            print("✅ Sample data added successfully!")
            print("📊 Added:")
            print("   - 3 flights (AA123, UA456, DL789)")
            print("   - 1 passenger (P001)")
            print("   - 1 booking (B001)")
            
        except Exception as e:
            print(f"❌ Error adding sample data: {e}")
            await db.rollback()

if __name__ == "__main__":
    asyncio.run(add_sample_data())