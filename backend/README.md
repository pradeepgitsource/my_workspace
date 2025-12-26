# Flight Web Check-in API - Backend

Production-grade FastAPI application with PostgreSQL database for flight web check-in system.

## Features

- **FastAPI**: Modern async web framework
- **PostgreSQL**: Production database with SQLAlchemy ORM
- **uv**: Fast Python package manager
- **Docker**: Containerized deployment
- **Async Operations**: High-performance database operations
- **Comprehensive API**: Full CRUD operations for flights, passengers, bookings, and check-ins

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
cd backend
docker-compose up --build
```

This will start:
- PostgreSQL database on port 5432
- FastAPI application on port 8000

### Option 2: Local Development

1. **Install PostgreSQL** and create database:
```sql
CREATE DATABASE flight_checkin;
```

2. **Install dependencies**:
```bash
cd backend
pip install uv
uv pip install -e .
```

3. **Set environment variable**:
```bash
export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost:5432/flight_checkin"
```

4. **Initialize sample data**:
```bash
python init_data.py
```

5. **Run the application**:
```bash
python main.py
```

## API Endpoints

### Access Points
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Core Endpoints

#### Flights
- `POST /api/flights` - Create flight
- `GET /api/flights` - List all flights
- `GET /api/flights/{flight_id}` - Get flight details

#### Passengers
- `POST /api/passengers` - Register passenger
- `GET /api/passengers/{passenger_id}` - Get passenger details
- `GET /api/passengers/{passenger_id}/bookings` - Get passenger bookings

#### Bookings
- `POST /api/bookings` - Create booking
- `GET /api/bookings/{booking_id}` - Get booking details
- `DELETE /api/bookings/{booking_id}` - Cancel booking

#### Check-in
- `POST /api/checkin` - Perform web check-in
- `GET /api/checkin/{checkin_id}` - Get boarding pass
- `GET /api/bookings/{booking_id}/checkin-status` - Check status

## Database Schema

### Tables
- **flights**: Flight information and seat availability
- **passengers**: Passenger personal information
- **bookings**: Flight bookings with seat assignments
- **checkin_records**: Check-in records with boarding passes

### Relationships
- Flight → Bookings (One-to-Many)
- Passenger → Bookings (One-to-Many)
- Booking → CheckinRecord (One-to-One)

## Business Logic

### Check-in Rules
- Opens 24 hours before departure
- Closes 1 hour before departure
- One check-in per booking
- Automatic boarding group assignment

### Boarding Groups
- **Group A**: Rows 1-10 (First Class)
- **Group B**: Rows 11-30 (Business)
- **Group C**: Rows 31+ (Economy)

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `LOG_LEVEL`: Logging level (default: INFO)

## Sample Data

The `init_data.py` script creates:
- 3 sample flights (AA123, UA456, DL789)
- 1 sample passenger (John Doe)
- 1 sample booking

## Testing

Use the interactive documentation at `/docs` to test all endpoints with a user-friendly interface.

## Production Deployment

### Docker
```bash
docker build -t flight-checkin-api .
docker run -p 8000:8000 -e DATABASE_URL="your_db_url" flight-checkin-api
```

### Health Monitoring
The `/health` endpoint provides system status for load balancers and monitoring tools.

## Architecture

- **Async/Await**: Non-blocking database operations
- **SQLAlchemy ORM**: Type-safe database operations
- **Pydantic Validation**: Request/response validation
- **CORS Enabled**: Frontend integration ready
- **Structured Logging**: Request/response tracking