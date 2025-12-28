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

### Production
- **Application**: http://localhost
- **API**: http://localhost/api
- **API Docs**: http://localhost/docs

## 🧪 Testing

### Backend Tests
```bash
# Run tests in container
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=app

# Local testing
cd backend
pytest --cov=app --cov-report=html
```

### Frontend Tests
```bash
# Run tests in container
docker-compose exec frontend npm test

# Local testing
cd frontend
npm test -- --coverage
```

### Test Coverage
- **Backend**: 78%+ coverage achieved with comprehensive test suite
- **Frontend**: Component testing with React Testing Library
- **Integration**: End-to-end workflow testing with mocked dependencies
- **Reports**: HTML coverage reports generated
- **Dependencies**: All required packages including email-validator for validation

## 🔧 Configuration

### Dependencies
```bash
# Backend
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
asyncpg==0.29.0
pydantic[email]==2.5.0
email-validator==2.1.0
alembic==1.13.1
python-multipart==0.0.6

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2

# Frontend
react==18.2.0
react-dom==18.2.0
axios==1.6.2
lucide-react==0.294.0
tailwindcss==3.3.6
```

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
├── .github/
│   └── workflows/           # CI/CD pipelines
│       ├── ci-cd.yml       # Main CI/CD workflow
│       └── docker.yml      # Docker build & push
├── frontend/                # React application
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── core/           # Models, schemas, database
│   │   ├── repositories/   # Data access layer
│   │   └── services/       # Business logic
│   ├── tests/
│   ├── main_refactored.py
│   └── Dockerfile
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

## 🎯 Getting Started with CI/CD

1. **Fork/Clone** this repository
2. **Push** to your GitHub repository
3. **Enable** GitHub Actions (automatic for public repos)
4. **Add secrets** if needed for deployment
5. **Push changes** to trigger the pipeline
6. **Create tags** for releases: `git tag v1.0.0 && git push --tags`
7. **Monitor** workflows in the Actions tab

The application is now fully containerized and production-ready with automated CI/CD! 🎉