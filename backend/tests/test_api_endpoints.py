import pytest
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_create_flight_endpoint(client):
    """Test flight creation endpoint."""
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": (datetime.utcnow() + timedelta(hours=6)).isoformat(),
        "arrival_time": (datetime.utcnow() + timedelta(hours=12)).isoformat(),
        "aircraft_type": "Boeing 737",
        "total_seats": 180
    }
    
    response = await client.post("/api/flights", json=flight_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["flight_id"] == "TEST123"
    assert data["available_seats"] == 180

@pytest.mark.asyncio
async def test_get_flights_endpoint(client):
    """Test get all flights endpoint."""
    # Create a flight first
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": (datetime.utcnow() + timedelta(hours=6)).isoformat(),
        "arrival_time": (datetime.utcnow() + timedelta(hours=12)).isoformat(),
        "aircraft_type": "Boeing 737",
        "total_seats": 180
    }
    
    await client.post("/api/flights", json=flight_data)
    
    response = await client.get("/api/flights")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["flight_id"] == "TEST123"

@pytest.mark.asyncio
async def test_create_passenger_endpoint(client):
    """Test passenger creation endpoint."""
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    
    response = await client.post("/api/passengers", json=passenger_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"
    assert data["email"] == "john.doe@test.com"

@pytest.mark.asyncio
async def test_full_checkin_flow(client):
    """Test complete check-in flow."""
    # Create flight
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": (datetime.utcnow() + timedelta(hours=6)).isoformat(),
        "arrival_time": (datetime.utcnow() + timedelta(hours=12)).isoformat(),
        "aircraft_type": "Boeing 737",
        "total_seats": 180
    }
    flight_response = await client.post("/api/flights", json=flight_data)
    assert flight_response.status_code == 201
    
    # Create passenger
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    passenger_response = await client.post("/api/passengers", json=passenger_data)
    assert passenger_response.status_code == 201
    passenger_id = passenger_response.json()["passenger_id"]
    
    # Create booking
    booking_data = {
        "flight_id": "TEST123",
        "passenger_id": passenger_id,
        "seat_number": "12A"
    }
    booking_response = await client.post("/api/bookings", json=booking_data)
    assert booking_response.status_code == 201
    booking_id = booking_response.json()["booking_id"]
    
    # Perform check-in
    checkin_data = {
        "booking_id": booking_id,
        "passenger_id": passenger_id
    }
    checkin_response = await client.post("/api/checkin", json=checkin_data)
    assert checkin_response.status_code == 201
    
    boarding_pass = checkin_response.json()
    assert boarding_pass["flight_id"] == "TEST123"
    assert boarding_pass["seat_number"] == "12A"
    assert boarding_pass["boarding_group"] in ["A", "B", "C"]