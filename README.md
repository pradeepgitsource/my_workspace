# Flight Web Check-in Application - Enterprise Architecture

Complete enterprise-grade containerized solution with Frontend (React), Backend (FastAPI), and Database (PostgreSQL) following Domain-Driven Design principles.

## 🏗️ Enterprise Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   PostgreSQL    │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   Database      │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
│                 │    │                 │    │                 │
│ • Auth Service  │    │ • JWT Auth      │    │ • User Storage  │
│ • Token Storage │    │ • Protected API │    │ • Hashed Passwords │
│ • Auto Logout   │    │ • OAuth2 Flow   │    │ • Session Data  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │     Nginx       │
                    │  Load Balancer  │
                    │   Port: 80      │
                    └─────────────────┘
```

## 🏢 Domain-Driven Design Structure

```
backend/
├── app/
│   ├── booking/              # Booking Domain
│   │   ├── booking_repository.py
│   │   ├── booking_service.py
│   │   └── booking_controller.py
│   ├── checkin/              # Check-in Domain
│   │   ├── checkin_repository.py
│   │   ├── checkin_service.py
│   │   └── checkin_controller.py
│   ├── flight/               # Flight Domain
│   │   └── flight_repository.py
│   ├── passenger/            # Passenger Domain
│   │   └── passenger_repository.py
│   ├── shared/               # Cross-cutting Concerns
│   │   ├── exceptions.py
│   │   └── auth.py
│   └── core/                 # Infrastructure
│       ├── database.py
│       ├── dependencies.py
│       └── exception_handlers.py
└── tests/                    # Domain-aligned Tests
    ├── booking/
    ├── checkin/
    ├── flight/
    └── shared/
```

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AUTHENTICATION FLOW                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. REGISTRATION                                                │
│  ┌─────────────┐    POST /auth/register    ┌─────────────────┐  │
│  │   Client    │──────────────────────────►│    Backend      │  │
│  │             │◄──────────────────────────│                 │  │
│  └─────────────┘    User Created (200)     └─────────────────┘  │
│                                                                 │
│  2. LOGIN                                                       │
│  ┌─────────────┐    POST /auth/token       ┌─────────────────┐  │
│  │   Client    │──────────────────────────►│    Backend      │  │
│  │             │◄──────────────────────────│                 │  │
│  └─────────────┘    JWT Token (200)        └─────────────────┘  │
│                                                                 │
│  3. PROTECTED REQUESTS                                          │
│  ┌─────────────┐    Authorization: Bearer  ┌─────────────────┐  │
│  │   Client    │──────────────────────────►│    Backend      │  │
│  │             │◄──────────────────────────│                 │  │
│  └─────────────┘    Protected Data (200)   └─────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        SECURITY LAYERS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Frontend Security:                                             │
│  • Token stored in localStorage                                 │
│  • Automatic token attachment via axios interceptors           │
│  • Auto-logout on 401 responses                                │
│  • Route protection based on auth state                        │
│                                                                 │
│  Backend Security:                                              │
│  • bcrypt password hashing with salt                           │
│  • JWT tokens with 30-minute expiry                            │
│  • OAuth2 Bearer token authentication                          │
│  • Protected endpoints with dependency injection               │
│                                                                 │
│  Database Security:                                             │
│  • No plain text passwords stored                              │
│  • SQLAlchemy ORM prevents SQL injection                       │
│  • Async operations with proper error handling                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git (to clone the repository)

### Development Environment
```bash
# Clone and start
git clone <repository>
cd flight-checkin-app

# Windows
start.bat dev

# Linux/Mac
chmod +x start.sh
./start.sh dev
```

### Production Environment
```bash
# Windows
start.bat prod

# Linux/Mac
./start.sh prod
```

## 🔐 Authentication Setup

### Register Users
```bash
# Method 1: Using Python script
python register_users.py

# Method 2: Using curl
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

### Default Test Credentials
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`

### Login Flow
1. **Register**: Create account via `/auth/register`
2. **Login**: Get JWT token via `/auth/token`
3. **Access**: Use token for protected endpoints

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

The application includes automated CI/CD pipelines:

#### 1. **Main CI/CD Pipeline** (`.github/workflows/ci-cd.yml`)
- **Triggers**: Push to `main`/`develop`, PRs to `main`
- **Jobs**:
  - **Test**: Backend/Frontend tests with PostgreSQL
  - **Build**: Docker image builds and testing
  - **Deploy**: Production deployment (main branch only)

#### 2. **Docker Build & Push** (`.github/workflows/docker.yml`)
- **Triggers**: Git tags (`v*`)
- **Builds**: Backend and frontend Docker images
- **Pushes**: To GitHub Container Registry

### Setting Up CI/CD

#### 1. **Enable GitHub Actions**
```bash
# Push to GitHub repository
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/flight-checkin-app.git
git push -u origin main
```

#### 2. **Configure Repository**
- GitHub Actions are enabled by default for public repos
- For private repos: **Settings** → **Actions** → **General** → Enable

#### 3. **Add Secrets (Optional)**
Go to **Settings** → **Secrets and variables** → **Actions**:
```
CODECOV_TOKEN    # For coverage reports
DEPLOY_KEY       # For deployment
```

#### 4. **Trigger Workflows**
```bash
# Trigger CI/CD pipeline
git push origin main

# Trigger Docker build & push
git tag v1.0.0
git push --tags
```

### Pipeline Features
- ✅ **Automated Testing**: Backend (pytest) + Frontend (Jest)
- ✅ **Code Coverage**: 50%+ requirement with reports
- ✅ **Docker Builds**: Multi-stage optimized builds
- ✅ **Health Checks**: Service availability testing
- ✅ **Container Registry**: Automatic image publishing
- ✅ **Branch Protection**: Main branch deployment only

## 📦 Services

### Frontend (React)
- **Port**: 3000 (dev) / 80 (prod via nginx)
- **Technology**: React 18, Tailwind CSS
- **Features**: Light/Dark theme, Responsive design
- **Build**: Multi-stage Docker build for optimization

### Backend (FastAPI)
- **Port**: 8000
- **Technology**: FastAPI, SQLAlchemy, PostgreSQL
- **Features**: Async operations, Auto-documentation
- **Architecture**: Repository pattern, Dependency injection

### Database (PostgreSQL)
- **Port**: 5432
- **Version**: PostgreSQL 15
- **Features**: Persistent storage, Health checks
- **Data**: Automatic schema creation

### Load Balancer (Nginx) - Production Only
- **Port**: 80
- **Features**: Reverse proxy, Static file serving
- **Routes**: Frontend (/) and Backend (/api)

## 🛠️ Commands

### Start Services
```bash
# Development (with hot reload)
start.bat dev

# Production (optimized builds)
start.bat prod
```

### Manage Services
```bash
# Stop all services
start.bat stop

# View logs
start.bat logs

# Check status
start.bat status
```

### Manual Docker Commands
```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up --build -d

# Stop all
docker-compose down
```

## 🌐 Access Points

### Development
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432
- **Auth Endpoints**:
  - Register: `POST /auth/register`
  - Login: `POST /auth/token`

### Production
- **Application**: http://localhost
- **API**: http://localhost/api
- **API Docs**: http://localhost/docs
- **Auth Endpoints**:
  - Register: `POST /auth/register`
  - Login: `POST /auth/token`

## 🧪 Enterprise Testing

### Test Architecture
```bash
# Domain-aligned test structure
tests/
├── booking/                  # Booking Domain Tests
│   ├── test_booking_repository.py
│   ├── test_booking_service.py
│   └── test_booking_controller.py
├── checkin/                  # Check-in Domain Tests
│   └── test_checkin_service.py
├── flight/                   # Flight Domain Tests
│   └── test_flight_passenger_repositories.py
└── shared/                   # Shared Component Tests
    └── test_exceptions.py
```

### Run Enterprise Tests
```bash
# Run all enterprise domain tests with coverage
cd backend
python tests/test_enterprise_coverage.py

# Run specific domain tests
pytest tests/booking/ --cov=app.booking -v
pytest tests/checkin/ --cov=app.checkin -v

# Generate coverage reports
pytest tests/ --cov=app --cov-report=html --cov-report=term-missing
```

### Test Coverage Metrics
- **Total Test Cases**: 57 comprehensive tests
- **Coverage Target**: 95%+ for all enterprise modules
- **Domain Coverage**:
  - Booking Domain: 21 tests (repository, service, controller)
  - Check-in Domain: 10 tests (service with business scenarios)
  - Flight/Passenger: 9 tests (repository operations)
  - Shared Components: 17 tests (exception handling)

### Enterprise Test Features
- **Domain Isolation**: Tests organized by business domain
- **Comprehensive Scenarios**: Success, failure, and edge cases
- **Mock Strategy**: Proper isolation using AsyncMock
- **Business Logic Testing**: Validation, transactions, error handling
- **Exception Coverage**: All custom business exceptions tested

## 🔧 Configuration

### Dependencies
```bash
# Backend - Enterprise Grade
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
asyncpg==0.29.0
pydantic[email]==2.5.0
email-validator==2.1.0
alembic==1.13.1
python-multipart==0.0.6

# Authentication & Security
PyJWT==2.8.0
bcrypt==4.0.1
passlib[bcrypt]==1.7.4

# Testing & Quality
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2

# Frontend - Modern Stack
react==18.2.0
react-dom==18.2.0
axios==1.6.2
lucide-react==0.294.0
tailwindcss==3.3.6
react-router-dom==6.8.0
```

### Environment Variables
```bash
# Backend
DATABASE_URL=postgresql+asyncpg://postgres:password@postgres:5432/flight_checkin
LOG_LEVEL=info

# Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend
REACT_APP_API_URL=http://localhost:8000

# Database
POSTGRES_DB=flight_checkin
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
```

### Docker Compose Files
- `docker-compose.yml` - Development environment
- `docker-compose.prod.yml` - Production with nginx
- `nginx.conf` - Load balancer configuration

## 📁 Project Structure
```
flight-checkin-app/
├── .github/
│   └── workflows/           # CI/CD pipelines
│       ├── ci-cd.yml       # Main CI/CD workflow
│       └── docker.yml      # Docker build & push
├── frontend/                # React application
│   ├── src/
│   │   ├── pages/          # Login, Register, Flights, Checkin
│   │   ├── services/       # AuthService, API calls
│   │   └── tests/          # Frontend test cases
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── core/           # Models, schemas, database
│   │   │   ├── auth.py     # JWT utilities
│   │   │   ├── user_models.py # User model
│   │   │   ├── auth_schemas.py # Pydantic schemas
│   │   │   └── dependencies.py # Auth dependencies
│   │   ├── routes/         # API endpoints
│   │   │   ├── auth.py     # Register/login routes
│   │   │   └── checkin.py  # Protected flight routes
│   │   ├── repositories/   # Data access layer
│   │   └── services/       # Business logic
│   ├── tests/              # Comprehensive test suite
│   │   ├── test_auth.py    # Authentication tests
│   │   ├── test_auth_routes.py # Route tests
│   │   ├── test_user_models.py # Model tests
│   │   └── test_protected_endpoints.py # Security tests
│   ├── main_refactored.py
│   └── Dockerfile
├── register_users.py        # User registration script
├── docker-compose.yml       # Development setup
├── docker-compose.prod.yml  # Production setup
├── nginx.conf              # Load balancer config
├── start.sh                # Linux/Mac startup script
├── start.bat               # Windows startup script
└── .gitignore              # Git ignore rules
```

## 📊 Monitoring

### Health Checks
- **Backend**: http://localhost:8000/health
- **Frontend**: http://localhost:3000 (responds with React app)
- **Database**: Built-in PostgreSQL health check

### Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

## 🔒 Security Features

### Authentication & Authorization
- **JWT Tokens**: 30-minute expiry with Bearer authentication
- **Password Security**: bcrypt hashing with salt
- **OAuth2 Flow**: Industry-standard authentication
- **Protected Endpoints**: All API routes require valid tokens
- **Auto-logout**: Frontend handles expired tokens
- **Input Validation**: Pydantic schemas with email validation

### Production Optimizations
- Non-root users in containers
- Multi-stage builds for smaller images
- Resource limits and health checks
- Nginx reverse proxy
- Environment variable security
- SQL injection protection via ORM

### Development Features
- Hot reload for development
- Debug logging
- Development-friendly configurations
- Test user creation scripts

## 🚀 Deployment

### Local Development
```bash
start.bat dev
```

### Production Deployment
```bash
start.bat prod
```

### Cloud Deployment
The Docker Compose files can be adapted for:
- Docker Swarm
- Kubernetes
- AWS ECS
- Google Cloud Run
- Azure Container Instances

### Automated Deployment
- **GitHub Actions**: Automatic deployment on main branch
- **Container Registry**: Images published to GHCR
- **Version Tags**: Semantic versioning with git tags

## 🛠️ Troubleshooting

### Common Issues
1. **Docker not running**: Start Docker Desktop
2. **Port conflicts**: Stop services using ports 3000, 8000, 5432, 80
3. **Database connection**: Wait for PostgreSQL health check to pass
4. **Build failures**: Clear Docker cache with `docker system prune`
5. **CI/CD failures**: Check GitHub Actions logs and secrets

### Reset Everything
```bash
# Stop all services and remove volumes
docker-compose down -v
docker-compose -f docker-compose.prod.yml down -v

# Remove all containers and images
docker system prune -a
```

## 📈 Performance

### Development
- Hot reload for instant feedback
- Source maps for debugging
- Development server optimizations

### Production
- Optimized React build
- Multi-stage Docker builds
- Nginx static file serving
- Database connection pooling
- Resource limits and health checks

### CI/CD Performance
- Parallel job execution
- Docker layer caching
- Dependency caching (npm, pip)
- Optimized test execution

## 🎯 Getting Started Guide

### 1. Setup Application
```bash
# Clone and start services
git clone <repository>
cd flight-checkin-app
start.bat dev  # Windows
```

### 2. Register Users
```bash
# Create test users
python register_users.py
```

### 3. Access Application
- **Frontend**: http://localhost:3000
- **Login** with: `admin` / `admin123`
- **API Docs**: http://localhost:8000/docs

### 4. CI/CD Pipeline
1. **Fork/Clone** this repository
2. **Push** to your GitHub repository
3. **Enable** GitHub Actions (automatic for public repos)
4. **Add secrets** if needed for deployment
5. **Push changes** to trigger the pipeline
6. **Create tags** for releases: `git tag v1.0.0 && git push --tags`
7. **Monitor** workflows in the Actions tab

### 5. Authentication Flow
1. **Register**: Create account via registration form or API
2. **Login**: Authenticate to receive JWT token
3. **Access**: Browse flights and perform check-ins
4. **Logout**: Token cleared, redirected to login

The application is now fully containerized and production-ready with enterprise-grade architecture following Domain-Driven Design principles! 🎉

## 📚 Documentation

- **[Enterprise Architecture Guide](docs/ENTERPRISE_ARCHITECTURE.md)** - Domain-Driven Design implementation
- **[API Documentation](docs/API_DOCUMENTATION.md)** - Complete API reference
- **[Testing Guide](docs/TESTING_GUIDE.md)** - Enterprise test suite documentation

## 🏢 Enterprise Features

- **Domain-Driven Design**: Clear business domain separation
- **SOLID Principles**: Enterprise-grade architecture patterns
- **95%+ Test Coverage**: Comprehensive test suite with 57 test cases
- **Global Exception Handling**: Centralized error management
- **JWT Authentication**: Industry-standard security
- **Async Operations**: High-performance database operations
- **Container Ready**: Docker-based deployment