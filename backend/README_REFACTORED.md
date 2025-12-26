# Flight Web Check-in API - Refactored Backend

Modular, testable FastAPI application with PostgreSQL using Repository Pattern and Dependency Injection.

## Architecture

### Modular Structure
```
backend/
├── app/
│   ├── core/                 # Core components
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── database.py       # Database configuration
│   │   ├── schemas.py        # Pydantic schemas
│   │   └── utils.py          # Business logic utilities
│   ├── repositories/         # Data access layer
│   │   ├── flight_repository.py
│   │   ├── passenger_repository.py
│   │   ├── booking_repository.py
│   │   └── checkin_repository.py
│   └── services/             # Business logic layer
│       ├── flight_service.py
│       ├── passenger_service.py
│       └── booking_service.py
├── tests/                    # Test suite
│   ├── conftest.py          # Test configuration
│   ├── test_flight_service.py
│   └── test_api_endpoints.py
├── main_refactored.py       # FastAPI application
└── pyproject_refactored.toml
```

### Design Patterns
- **Repository Pattern**: Separates data access from business logic
- **Dependency Injection**: Loose coupling between components
- **Service Layer**: Encapsulates business logic
- **Clean Architecture**: Clear separation of concerns

## Features

### Testability
- **Unit Tests**: Service layer testing with mocked dependencies
- **Integration Tests**: End-to-end API testing
- **Test Coverage**: Comprehensive test coverage reporting
- **Test Database**: Isolated test environment

### Modularity
- **Separation of Concerns**: Each layer has a single responsibility
- **Dependency Injection**: Easy to mock and test
- **Interface-based Design**: Flexible and extensible
- **Clean Code**: Readable and maintainable

### Production Ready
- **Async Operations**: High-performance database operations
- **Error Handling**: Comprehensive exception handling
- **Logging**: Structured logging throughout
- **Health Checks**: Monitoring endpoints

## Quick Start

### Option 1: Docker Compose
```bash
cd backend
docker-compose up --build
```

### Option 2: Local Development
```bash
cd backend
pip install uv
uv pip install -e . --extra dev
python main_refactored.py
```

## Testing

### Run All Tests
```bash
cd backend
pytest
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

### Run Specific Tests
```bash
pytest tests/test_flight_service.py -v
```

## API Endpoints

### Access Points
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Core Endpoints
- `POST /api/flights` - Create flight
- `GET /api/flights` - List flights
- `POST /api/passengers` - Register passenger
- `POST /api/bookings` - Create booking
- `POST /api/checkin` - Web check-in

## Development

### Adding New Features
1. **Model**: Add database model in `app/core/models.py`
2. **Schema**: Add Pydantic schemas in `app/core/schemas.py`
3. **Repository**: Create repository in `app/repositories/`
4. **Service**: Implement business logic in `app/services/`
5. **Endpoint**: Add API endpoint in `main_refactored.py`
6. **Tests**: Write unit and integration tests

### Testing Strategy
- **Unit Tests**: Test services with mocked repositories
- **Integration Tests**: Test complete API flows
- **Database Tests**: Use test database for isolation
- **Coverage**: Maintain high test coverage

## Benefits of Refactored Architecture

### Testability
- Easy to mock dependencies
- Isolated unit tests
- Fast test execution
- High test coverage

### Maintainability
- Clear separation of concerns
- Single responsibility principle
- Easy to understand and modify
- Consistent patterns

### Scalability
- Modular components
- Easy to extend
- Flexible architecture
- Performance optimized

### Quality
- Type safety with Pydantic
- Comprehensive error handling
- Structured logging
- Production ready

## Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `LOG_LEVEL`: Logging level (default: INFO)

## Deployment
```bash
# Docker
docker build -t flight-checkin-api .
docker run -p 8000:8000 flight-checkin-api

# Local
python main_refactored.py
```

This refactored architecture provides a solid foundation for building scalable, testable, and maintainable applications.