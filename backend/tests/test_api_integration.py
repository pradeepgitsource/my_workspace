import pytest
from datetime import datetime, timedelta
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test root endpoint."""
    response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Flight Web Check-in API"
    assert data["version"] == "2.0.0"

@pytest.mark.asyncio
async def test_create_flight_success(client: AsyncClient):
    """Test successful flight creation."""
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
    assert data["status"] == "scheduled"

@pytest.mark.asyncio
async def test_create_flight_duplicate(client: AsyncClient):
    """Test flight creation with duplicate ID."""
    flight_data = {
        "flight_id": "TEST123",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "departure_time": (datetime.utcnow() + timedelta(hours=6)).isoformat(),
        "arrival_time": (datetime.utcnow() + timedelta(hours=12)).isoformat(),
        "aircraft_type": "Boeing 737",
        "total_seats": 180
    }
    
    # Create first flight
    await client.post("/api/flights", json=flight_data)
    
    # Try to create duplicate
    response = await client.post("/api/flights", json=flight_data)
    
    assert response.status_code == 409
    data = response.json()
    assert "already exists" in data["detail"]

@pytest.mark.asyncio
async def test_get_flight_success(client: AsyncClient):
    """Test getting existing flight."""
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
    
    response = await client.get("/api/flights/TEST123")
    
    assert response.status_code == 200
    data = response.json()
    assert data["flight_id"] == "TEST123"

@pytest.mark.asyncio
async def test_get_flight_not_found(client: AsyncClient):
    """Test getting non-existent flight."""
    response = await client.get("/api/flights/NONEXISTENT")
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]

@pytest.mark.asyncio
async def test_get_all_flights(client: AsyncClient):
    """Test getting all flights."""
    # Create multiple flights
    for i in range(3):
        flight_data = {
            "flight_id": f"TEST{i}",
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
    assert len(data) == 3

@pytest.mark.asyncio
async def test_create_passenger_success(client: AsyncClient):
    """Test successful passenger creation."""
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
    assert "passenger_id" in data

@pytest.mark.asyncio
async def test_create_passenger_duplicate_email(client: AsyncClient):
    """Test passenger creation with duplicate email."""
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    
    # Create first passenger
    await client.post("/api/passengers", json=passenger_data)
    
    # Try to create duplicate
    response = await client.post("/api/passengers", json=passenger_data)
    
    assert response.status_code == 409
    data = response.json()
    assert "already registered" in data["detail"]

@pytest.mark.asyncio
async def test_create_passenger_invalid_email(client: AsyncClient):
    """Test passenger creation with invalid email."""
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "invalid-email",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    
    response = await client.post("/api/passengers", json=passenger_data)
    
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_passenger_success(client: AsyncClient):
    """Test getting existing passenger."""
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    
    create_response = await client.post("/api/passengers", json=passenger_data)
    passenger_id = create_response.json()["passenger_id"]
    
    response = await client.get(f"/api/passengers/{passenger_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["passenger_id"] == passenger_id

@pytest.mark.asyncio
async def test_get_passenger_not_found(client: AsyncClient):
    """Test getting non-existent passenger."""
    response = await client.get("/api/passengers/NONEXISTENT")
    
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_booking_success(client: AsyncClient):
    """Test successful booking creation."""
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
    await client.post("/api/flights", json=flight_data)
    
    # Create passenger
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    passenger_response = await client.post("/api/passengers", json=passenger_data)
    passenger_id = passenger_response.json()["passenger_id"]
    
    # Create booking
    booking_data = {
        "flight_id": "TEST123",
        "passenger_id": passenger_id,
        "seat_number": "12A"
    }
    
    response = await client.post("/api/bookings", json=booking_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["flight_id"] == "TEST123"
    assert data["seat_number"] == "12A"

@pytest.mark.asyncio
async def test_create_booking_flight_not_found(client: AsyncClient):
    """Test booking creation with non-existent flight."""
    booking_data = {
        "flight_id": "NONEXISTENT",
        "passenger_id": "P123",
        "seat_number": "12A"
    }
    
    response = await client.post("/api/bookings", json=booking_data)
    
    assert response.status_code == 404
    data = response.json()
    assert "Flight not found" in data["detail"]

@pytest.mark.asyncio
async def test_full_checkin_flow(client: AsyncClient):
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
    
    # Get boarding pass
    checkin_id = boarding_pass["checkin_id"]
    boarding_pass_response = await client.get(f"/api/checkin/{checkin_id}")
    assert boarding_pass_response.status_code == 200
    
    # Check status
    status_response = await client.get(f"/api/bookings/{booking_id}/checkin-status")
    assert status_response.status_code == 200
    status_data = status_response.json()
    assert status_data["checked_in"] is True

@pytest.mark.asyncio
async def test_checkin_already_checked_in(client: AsyncClient):
    """Test check-in when already checked in."""
    # Setup flight, passenger, booking
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
    
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    passenger_response = await client.post("/api/passengers", json=passenger_data)
    passenger_id = passenger_response.json()["passenger_id"]
    
    booking_data = {
        "flight_id": "TEST123",
        "passenger_id": passenger_id,
        "seat_number": "12A"
    }
    booking_response = await client.post("/api/bookings", json=booking_data)
    booking_id = booking_response.json()["booking_id"]
    
    # First check-in
    checkin_data = {
        "booking_id": booking_id,
        "passenger_id": passenger_id
    }
    await client.post("/api/checkin", json=checkin_data)
    
    # Try to check-in again
    response = await client.post("/api/checkin", json=checkin_data)
    
    assert response.status_code == 409
    data = response.json()
    assert "Already checked in" in data["detail"]

@pytest.mark.asyncio
async def test_checkin_passenger_mismatch(client: AsyncClient):
    """Test check-in with wrong passenger ID."""
    # Setup flight, passenger, booking
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
    
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    passenger_response = await client.post("/api/passengers", json=passenger_data)
    passenger_id = passenger_response.json()["passenger_id"]
    
    booking_data = {
        "flight_id": "TEST123",
        "passenger_id": passenger_id,
        "seat_number": "12A"
    }
    booking_response = await client.post("/api/bookings", json=booking_data)
    booking_id = booking_response.json()["booking_id"]
    
    # Try check-in with wrong passenger ID
    checkin_data = {
        "booking_id": booking_id,
        "passenger_id": "WRONG_ID"
    }
    response = await client.post("/api/checkin", json=checkin_data)
    
    assert response.status_code == 400
    data = response.json()
    assert "mismatch" in data["detail"]

@pytest.mark.asyncio
async def test_cancel_booking(client: AsyncClient):
    """Test booking cancellation."""
    # Setup flight, passenger, booking
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
    
    passenger_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-15"
    }
    passenger_response = await client.post("/api/passengers", json=passenger_data)
    passenger_id = passenger_response.json()["passenger_id"]
    
    booking_data = {
        "flight_id": "TEST123",
        "passenger_id": passenger_id,
        "seat_number": "12A"
    }
    booking_response = await client.post("/api/bookings", json=booking_data)
    booking_id = booking_response.json()["booking_id"]
    
    # Cancel booking
    response = await client.delete(f"/api/bookings/{booking_id}")
    
    assert response.status_code == 204