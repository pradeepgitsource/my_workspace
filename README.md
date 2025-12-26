# Flight Web Check-in Application - Containerized

Complete containerized solution with Frontend (React), Backend (FastAPI), and Database (PostgreSQL).

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   PostgreSQL    │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   Database      │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
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

### Production
- **Application**: http://localhost
- **API**: http://localhost/api
- **API Docs**: http://localhost/docs

## 🔧 Configuration

### Environment Variables
```bash
# Backend
DATABASE_URL=postgresql+asyncpg://postgres:password@postgres:5432/flight_checkin
LOG_LEVEL=info

# Frontend
REACT_APP_API_URL=http://localhost:8000/api

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
├── frontend/                 # React application
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── core/            # Models, schemas, database
│   │   ├── repositories/    # Data access layer
│   │   └── services/        # Business logic
│   ├── tests/
│   ├── main_refactored.py
│   └── Dockerfile
├── docker-compose.yml        # Development setup
├── docker-compose.prod.yml   # Production setup
├── nginx.conf               # Load balancer config
├── start.sh                 # Linux/Mac startup script
└── start.bat                # Windows startup script
```

## 🧪 Testing

### Backend Tests
```bash
# Run tests in container
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=app
```

### Frontend Tests
```bash
# Run tests in container
docker-compose exec frontend npm test
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

### Production Optimizations
- Non-root users in containers
- Multi-stage builds for smaller images
- Resource limits and health checks
- Nginx reverse proxy
- Environment variable security

### Development Features
- Hot reload for development
- Debug logging
- Development-friendly configurations

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

## 🛠️ Troubleshooting

### Common Issues
1. **Docker not running**: Start Docker Desktop
2. **Port conflicts**: Stop services using ports 3000, 8000, 5432, 80
3. **Database connection**: Wait for PostgreSQL health check to pass
4. **Build failures**: Clear Docker cache with `docker system prune`

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

The application is now fully containerized and production-ready! 🎉