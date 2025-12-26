# Flight Web Check-in API - Design Document

## 1. Overview
A FastAPI-based REST API that simulates airline web check-in functionality, allowing passengers to check in for flights, manage boarding passes, and retrieve flight information.

## 2. Architecture

### Technology Stack
- **Framework**: FastAPI (async Python web framework)
- **Package Manager**: uv (fast Python package installer)
- **Containerization**: Docker
- **Database**: In-memory (can be extended to PostgreSQL)
- **Validation**: Pydantic models

### Project Structure
```
flight-checkin-api/
├── Dockerfile
├── pyproject.toml
├── uv.lock
├── main.py
├── models.py
├── database.py
├── routes/
│   ├── __init__.py
│   ├── flights.py
│   ├── checkin.py
│   └── passengers.py
├── schemas.py
└── utils.py
```

## 3. Core Entities

### Flight
- **flight_id**: Unique identifier (e.g., "AA123")
- **departure_airport**: IATA code (e.g., "JFK")
- **arrival_airport**: IATA code (e.g., "LAX")
- **departure_time**: ISO 8601 datetime
- **arrival_time**: ISO 8601 datetime
- **aircraft_type**: Aircraft model
- **total_seats**: Total capacity
- **available_seats**: Remaining seats
- **status**: "scheduled", "boarding", "departed", "cancelled"

### Passenger
- **passenger_id**: Unique identifier
- **first_name**: First name
- **last_name**: Last name
- **email**: Email address
- **phone**: Phone number
- **date_of_birth**: DOB

### Booking
- **booking_id**: Unique identifier
- **flight_id**: Reference to flight
- **passenger_id**: Reference to passenger
- **seat_number**: Assigned seat
- **booking_status**: "confirmed", "checked_in", "cancelled"
- **booking_date**: When booking was made

### Check-in Record
- **checkin_id**: Unique identifier
- **booking_id**: Reference to booking
- **checkin_time**: When check-in occurred
- **boarding_pass_number**: Generated boarding pass ID
- **gate_number**: Assigned gate (if available)
- **boarding_group**: Boarding sequence group

## 4. API Endpoints

### Flight Management
- `GET /api/flights` - List all flights (with filters: date, airport, status)
- `GET /api/flights/{flight_id}` - Get flight details
- `POST /api/flights` - Create a new flight (admin only)

### Passenger Management
- `POST /api/passengers` - Register a new passenger
- `GET /api/passengers/{passenger_id}` - Get passenger details
- `PUT /api/passengers/{passenger_id}` - Update passenger info

### Booking Management
- `POST /api/bookings` - Create a new booking
- `GET /api/bookings/{booking_id}` - Get booking details
- `GET /api/passengers/{passenger_id}/bookings` - List passenger's bookings
- `DELETE /api/bookings/{booking_id}` - Cancel a booking

### Check-in Operations (Core Feature)
- `POST /api/checkin` - Perform web check-in
  - Input: booking_id, passenger_id (verification)
  - Output: boarding_pass with gate and group info
- `GET /api/checkin/{checkin_id}` - Retrieve boarding pass
- `GET /api/bookings/{booking_id}/checkin-status` - Check if already checked in
- `POST /api/checkin/{checkin_id}/cancel` - Cancel check-in

### Health & Status
- `GET /health` - Health check endpoint

## 5. Business Logic

### Check-in Rules
1. Check-in opens 24 hours before departure
2. Check-in closes 1 hour before departure
3. Passenger must have a confirmed booking
4. Only one check-in per booking
5. Cannot check in if flight is cancelled or departed
6. Automatic seat assignment if not pre-assigned

### Boarding Pass Generation
- Format: `{FLIGHT_ID}-{BOOKING_ID}-{TIMESTAMP}`
- Includes: flight info, seat, boarding group, gate (if assigned)
- Boarding groups: A (first class), B (business), C (economy)

### Seat Management
- Seats format: Row (1-50) + Letter (A-F)
- Track available vs. occupied seats
- Prevent double-booking

## 6. Data Models (Pydantic Schemas)

### Request/Response Models
- `FlightCreate`, `FlightResponse`
- `PassengerCreate`, `PassengerResponse`
- `BookingCreate`, `BookingResponse`
- `CheckinRequest`, `CheckinResponse`
- `BoardingPassResponse`
- `ErrorResponse`

## 7. Error Handling

### HTTP Status Codes
- `200 OK` - Successful operation
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `409 Conflict` - Business logic violation (e.g., already checked in)
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

### Custom Exceptions
- `FlightNotFoundError`
- `PassengerNotFoundError`
- `BookingNotFoundError`
- `CheckinWindowClosedError`
- `AlreadyCheckedInError`
- `InvalidBookingError`

## 8. Docker Configuration

### Dockerfile Strategy
- Base image: `python:3.11-slim`
- Multi-stage build (optional for optimization)
- Install uv in container
- Copy project files
- Install dependencies via uv
- Expose port 8000
- Run with uvicorn

### Environment Variables
- `ENVIRONMENT`: dev/prod
- `LOG_LEVEL`: debug/info/warning
- `API_PORT`: 8000 (default)

## 9. Database Strategy

### Phase 1 (MVP)
- In-memory storage using Python dictionaries
- Data persists only during container runtime
- Suitable for testing and demo

### Phase 2 (Future)
- PostgreSQL with SQLAlchemy ORM
- Persistent storage
- Connection pooling

## 10. Testing Strategy

### Unit Tests
- Model validation
- Business logic (check-in rules, seat assignment)
- Error handling

### Integration Tests
- API endpoint testing
- End-to-end check-in flow
- Concurrent check-in scenarios

### Test Data
- Pre-populated flights
- Sample passengers and bookings
- Fixtures for common scenarios

## 11. Logging & Monitoring

### Logging
- Structured logging with timestamps
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request/response logging middleware

### Metrics (Future)
- Check-in success rate
- API response times
- Concurrent users

## 12. Security Considerations

### Authentication (Future)
- JWT tokens for passenger verification
- API key for admin endpoints

### Validation
- Input sanitization
- Rate limiting on check-in endpoint
- CORS configuration

### Data Protection
- Passenger PII handling
- Secure error messages (no sensitive data leakage)

## 13. Deployment

### Local Development
```bash
uv run uvicorn main:app --reload
```

### Docker Deployment
```bash
docker build -t flight-checkin-api .
docker run -p 8000:8000 flight-checkin-api
```

### Environment Setup
- Development: SQLite/in-memory
- Production: PostgreSQL, environment variables for secrets

## 14. API Response Format

### Success Response
```json
{
  "status": "success",
  "data": { /* resource data */ },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Response
```json
{
  "status": "error",
  "error_code": "CHECKIN_WINDOW_CLOSED",
  "message": "Check-in window has closed",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 15. Implementation Phases

### Phase 1: MVP
- Basic flight and passenger management
- Booking creation
- Web check-in with boarding pass generation
- In-memory database

### Phase 2: Enhancement
- Seat selection and management
- Boarding group assignment logic
- Check-in history and analytics

### Phase 3: Production Ready
- Database persistence
- Authentication & authorization
- Rate limiting
- Comprehensive logging
- Monitoring and alerting

---

This design provides a solid foundation for building a scalable flight web check-in API with FastAPI and uv.