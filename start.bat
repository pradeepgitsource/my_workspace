@echo off
echo 🚀 Starting Flight Check-in Application...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker first.
    exit /b 1
)

if "%1"=="dev" (
    echo 🔧 Starting Development Environment...
    docker-compose down
    docker-compose up --build
) else if "%1"=="prod" (
    echo 🏭 Starting Production Environment...
    docker-compose -f docker-compose.prod.yml down
    docker-compose -f docker-compose.prod.yml up --build -d
    echo ✅ Production environment started!
    echo 🌐 Frontend: http://localhost
    echo 🔧 Backend API: http://localhost/api
    echo 📚 API Docs: http://localhost/docs
) else if "%1"=="stop" (
    echo 🛑 Stopping all services...
    docker-compose down
    docker-compose -f docker-compose.prod.yml down
    echo ✅ All services stopped!
) else if "%1"=="logs" (
    echo 📋 Showing logs...
    docker-compose logs -f
) else if "%1"=="status" (
    echo 📊 Service Status:
    docker-compose ps
) else (
    echo Usage: %0 {dev^|prod^|stop^|logs^|status}
    echo.
    echo Commands:
    echo   dev     - Start development environment
    echo   prod    - Start production environment with nginx
    echo   stop    - Stop all services
    echo   logs    - Show service logs
    echo   status  - Show service status
    echo.
    echo Examples:
    echo   %0 dev     # Start development
    echo   %0 prod    # Start production
    echo   %0 stop    # Stop all services
)