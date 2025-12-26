import pytest
from datetime import datetime, timedelta
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_complete_flight_booking_flow(client: AsyncClient):
    """Test complete flow from flight creation to check-in."""
    
    # Step 1: Create flight
    flight_data = {
        "flight_id": "INTEGRATION001",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": (datetime.utcnow() + timedelta(hours=6)).isoformat(),
        "arrival_time": (datetime.utcnow() + timedelta(hours=12)).isoformat(),
        "aircraft_type": "Boeing 737",
        "total_seats": 180
    }
    
    flight_response = await client.post("/api/flights", json=flight_data)
    assert flight_response.status_code == 201
    flight_result = flight_response.json()
    assert flight_result["available_seats"] == 180
    
    # Step 2: Create passenger
    passenger_data = {
        "first_name": "Integration",
        "last_name": "Test",
        "email": "integration.test@example.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    
    passenger_response = await client.post("/api/passengers", json=passenger_data)
    assert passenger_response.status_code == 201
    passenger_result = passenger_response.json()
    passenger_id = passenger_result["passenger_id"]
    
    # Step 3: Create booking
    booking_data = {
        "flight_id": "INTEGRATION001",
        "passenger_id": passenger_id,
        "seat_number": "15C"
    }
    
    booking_response = await client.post("/api/bookings", json=booking_data)
    assert booking_response.status_code == 201
    booking_result = booking_response.json()
    booking_id = booking_result["booking_id"]
    
    # Verify flight seats decreased
    flight_check = await client.get("/api/flights/INTEGRATION001")
    assert flight_check.json()["available_seats"] == 179
    
    # Step 4: Check booking status before check-in
    checkin_status = await client.get(f"/api/bookings/{booking_id}/checkin-status")
    assert checkin_status.status_code == 200
    status_result = checkin_status.json()
    assert status_result["checked_in"] is False
    
    # Step 5: Perform check-in
    checkin_data = {
        "booking_id": booking_id,
        "passenger_id": passenger_id
    }
    
    checkin_response = await client.post("/api/checkin", json=checkin_data)
    assert checkin_response.status_code == 201
    boarding_pass = checkin_response.json()
    
    assert boarding_pass["flight_id"] == "INTEGRATION001"
    assert boarding_pass["seat_number"] == "15C"
    assert boarding_pass["passenger_name"] == "Integration Test"
    assert boarding_pass["boarding_group"] in ["A", "B", "C"]
    
    # Step 6: Verify check-in status changed
    checkin_status_after = await client.get(f"/api/bookings/{booking_id}/checkin-status")
    status_after = checkin_status_after.json()
    assert status_after["checked_in"] is True
    
    # Step 7: Get boarding pass by checkin ID
    checkin_id = boarding_pass["checkin_id"]
    boarding_pass_get = await client.get(f"/api/checkin/{checkin_id}")
    assert boarding_pass_get.status_code == 200
    assert boarding_pass_get.json()["checkin_id"] == checkin_id

@pytest.mark.asyncio
async def test_multiple_passengers_same_flight(client: AsyncClient):
    """Test multiple passengers booking the same flight."""
    
    # Create flight
    flight_data = {
        "flight_id": "MULTI001",
        "departure_airport": "SFO",
        "arrival_airport": "NYC",
        "departure_time": (datetime.utcnow() + timedelta(hours=8)).isoformat(),
        "arrival_time": (datetime.utcnow() + timedelta(hours=14)).isoformat(),
        "aircraft_type": "Airbus A320",
        "total_seats": 150
    }
    
    await client.post("/api/flights", json=flight_data)
    
    passengers = []
    bookings = []
    
    # Create 3 passengers and bookings
    for i in range(3):
        passenger_data = {
            "first_name": f"Passenger{i}",
            "last_name": "Multi",
            "email": f"passenger{i}@multi.com",
            "phone": f"+123456789{i}",
            "date_of_birth": "1985-05-20"
        }
        
        passenger_response = await client.post("/api/passengers", json=passenger_data)
        passenger = passenger_response.json()
        passengers.append(passenger)
        
        booking_data = {
            "flight_id": "MULTI001",
            "passenger_id": passenger["passenger_id"],
            "seat_number": f"{10+i}A"
        }
        
        booking_response = await client.post("/api/bookings", json=booking_data)
        booking = booking_response.json()
        bookings.append(booking)
    
    # Verify flight has correct available seats
    flight_check = await client.get("/api/flights/MULTI001")
    assert flight_check.json()["available_seats"] == 147  # 150 - 3
    
    # Check-in all passengers
    for i, (passenger, booking) in enumerate(zip(passengers, bookings)):
        checkin_data = {
            "booking_id": booking["booking_id"],
            "passenger_id": passenger["passenger_id"]
        }
        
        checkin_response = await client.post("/api/checkin", json=checkin_data)
        assert checkin_response.status_code == 201
        
        boarding_pass = checkin_response.json()
        assert boarding_pass["seat_number"] == f"{10+i}A"

@pytest.mark.asyncio
async def test_booking_cancellation_flow(client: AsyncClient):
    """Test booking cancellation and seat restoration."""
    
    # Create flight
    flight_data = {
        "flight_id": "CANCEL001",
        "departure_airport": "LAX",
        "arrival_airport": "JFK",
        "departure_time": (datetime.utcnow() + timedelta(hours=10)).isoformat(),
        "arrival_time": (datetime.utcnow() + timedelta(hours=16)).isoformat(),
        "aircraft_type": "Boeing 777",
        "total_seats": 300
    }
    
    await client.post("/api/flights", json=flight_data)
    
    # Create passenger
    passenger_data = {
        "first_name": "Cancel",
        "last_name": "Test",
        "email": "cancel.test@example.com",
        "phone": "+9876543210",
        "date_of_birth": "1988-12-10"
    }
    
    passenger_response = await client.post("/api/passengers", json=passenger_data)
    passenger = passenger_response.json()
    
    # Create booking
    booking_data = {
        "flight_id": "CANCEL001",
        "passenger_id": passenger["passenger_id"],
        "seat_number": "25F"
    }
    
    booking_response = await client.post("/api/bookings", json=booking_data)
    booking = booking_response.json()
    
    # Verify seat was taken
    flight_check = await client.get("/api/flights/CANCEL001")
    assert flight_check.json()["available_seats"] == 299
    
    # Cancel booking
    cancel_response = await client.delete(f"/api/bookings/{booking['booking_id']}")
    assert cancel_response.status_code == 204
    
    # Verify seat was restored
    flight_check_after = await client.get("/api/flights/CANCEL001")
    assert flight_check_after.json()["available_seats"] == 300
    
    # Verify booking is cancelled
    booking_check = await client.get(f"/api/bookings/{booking['booking_id']}")
    assert booking_check.json()["booking_status"] == "cancelled"

@pytest.mark.asyncio
async def test_passenger_multiple_bookings(client: AsyncClient):
    """Test passenger with multiple flight bookings."""
    
    # Create multiple flights
    flights = []
    for i in range(2):
        flight_data = {
            "flight_id": f"MULTI_FLIGHT_{i}",
            "departure_airport": "CHI" if i == 0 else "NYC",
            "arrival_airport": "MIA" if i == 0 else "LAX",
            "departure_time": (datetime.utcnow() + timedelta(hours=6+i*12)).isoformat(),
            "arrival_time": (datetime.utcnow() + timedelta(hours=10+i*12)).isoformat(),
            "aircraft_type": "Boeing 737",
            "total_seats": 160
        }
        
        flight_response = await client.post("/api/flights", json=flight_data)
        flights.append(flight_response.json())
    
    # Create passenger
    passenger_data = {
        "first_name": "Multi",
        "last_name": "Booking",
        "email": "multi.booking@example.com",
        "phone": "+5555555555",
        "date_of_birth": "1992-03-25"
    }
    
    passenger_response = await client.post("/api/passengers", json=passenger_data)
    passenger = passenger_response.json()
    
    # Create bookings for both flights
    bookings = []
    for i, flight in enumerate(flights):
        booking_data = {
            "flight_id": flight["flight_id"],
            "passenger_id": passenger["passenger_id"],
            "seat_number": f"{20+i}B"
        }
        
        booking_response = await client.post("/api/bookings", json=booking_data)
        bookings.append(booking_response.json())
    
    # Get passenger bookings
    passenger_bookings = await client.get(f"/api/passengers/{passenger['passenger_id']}/bookings")
    assert passenger_bookings.status_code == 200
    
    bookings_list = passenger_bookings.json()
    assert len(bookings_list) == 2
    
    flight_ids = [b["flight_id"] for b in bookings_list]
    assert "MULTI_FLIGHT_0" in flight_ids
    assert "MULTI_FLIGHT_1" in flight_ids

@pytest.mark.asyncio
async def test_error_handling_scenarios(client: AsyncClient):
    """Test various error scenarios."""
    
    # Test duplicate flight creation
    flight_data = {
        "flight_id": "ERROR001",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": (datetime.utcnow() + timedelta(hours=6)).isoformat(),
        "arrival_time": (datetime.utcnow() + timedelta(hours=12)).isoformat(),
        "aircraft_type": "Boeing 737",
        "total_seats": 180
    }
    
    # First creation should succeed
    response1 = await client.post("/api/flights", json=flight_data)
    assert response1.status_code == 201
    
    # Second creation should fail
    response2 = await client.post("/api/flights", json=flight_data)
    assert response2.status_code == 409
    
    # Test booking non-existent flight
    passenger_data = {
        "first_name": "Error",
        "last_name": "Test",
        "email": "error.test@example.com",
        "phone": "+1111111111",
        "date_of_birth": "1990-01-01"
    }
    
    passenger_response = await client.post("/api/passengers", json=passenger_data)
    passenger = passenger_response.json()
    
    booking_data = {
        "flight_id": "NONEXISTENT",
        "passenger_id": passenger["passenger_id"],
        "seat_number": "1A"
    }
    
    booking_response = await client.post("/api/bookings", json=booking_data)
    assert booking_response.status_code == 404
    
    # Test booking with non-existent passenger
    booking_data_bad_passenger = {
        "flight_id": "ERROR001",
        "passenger_id": "NONEXISTENT",
        "seat_number": "1A"
    }
    
    booking_response_bad = await client.post("/api/bookings", json=booking_data_bad_passenger)
    assert booking_response_bad.status_code == 404
    
    # Test duplicate passenger email
    duplicate_passenger = {
        "first_name": "Duplicate",
        "last_name": "Email",
        "email": "error.test@example.com",  # Same email as above
        "phone": "+2222222222",
        "date_of_birth": "1985-05-15"
    }
    
    duplicate_response = await client.post("/api/passengers", json=duplicate_passenger)
    assert duplicate_response.status_code == 409

@pytest.mark.asyncio
async def test_api_health_and_root_endpoints(client: AsyncClient):
    """Test health check and root endpoints."""
    
    # Test root endpoint
    root_response = await client.get("/")
    assert root_response.status_code == 200
    
    root_data = root_response.json()
    assert "message" in root_data
    assert "version" in root_data
    assert root_data["status"] == "running"
    
    # Test health endpoint
    health_response = await client.get("/health")
    assert health_response.status_code == 200
    
    health_data = health_response.json()
    assert health_data["status"] == "healthy"
    assert "timestamp" in health_data
    assert "version" in health_data

@pytest.mark.asyncio
async def test_full_capacity_booking(client: AsyncClient):
    """Test booking when flight reaches full capacity."""
    
    # Create small flight
    flight_data = {
        "flight_id": "SMALL001",
        "departure_airport": "BOS",
        "arrival_airport": "DC",
        "departure_time": (datetime.utcnow() + timedelta(hours=4)).isoformat(),
        "arrival_time": (datetime.utcnow() + timedelta(hours=6)).isoformat(),
        "aircraft_type": "Small Jet",
        "total_seats": 2  # Very small capacity
    }
    
    await client.post("/api/flights", json=flight_data)
    
    # Create passengers and fill the flight
    passengers = []
    for i in range(3):  # Try to book 3 seats on 2-seat flight
        passenger_data = {
            "first_name": f"Full{i}",
            "last_name": "Capacity",
            "email": f"full{i}@capacity.com",
            "phone": f"+111111111{i}",
            "date_of_birth": "1990-01-01"
        }
        
        passenger_response = await client.post("/api/passengers", json=passenger_data)
        passengers.append(passenger_response.json())
    
    # Book first two seats (should succeed)
    for i in range(2):
        booking_data = {
            "flight_id": "SMALL001",
            "passenger_id": passengers[i]["passenger_id"],
            "seat_number": f"{i+1}A"
        }
        
        booking_response = await client.post("/api/bookings", json=booking_data)
        assert booking_response.status_code == 201
    
    # Try to book third seat (should fail)
    booking_data_fail = {
        "flight_id": "SMALL001",
        "passenger_id": passengers[2]["passenger_id"],
        "seat_number": "3A"
    }
    
    booking_response_fail = await client.post("/api/bookings", json=booking_data_fail)
    assert booking_response_fail.status_code == 409  # No available seats
    
    # Verify flight is at capacity
    flight_check = await client.get("/api/flights/SMALL001")
    assert flight_check.json()["available_seats"] == 0