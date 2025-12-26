#!/bin/bash

# Flight Check-in Application Startup Script

echo "🚀 Starting Flight Check-in Application..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Function to start development environment
start_dev() {
    echo "🔧 Starting Development Environment..."
    docker-compose down
    docker-compose up --build
}

# Function to start production environment
start_prod() {
    echo "🏭 Starting Production Environment..."
    docker-compose -f docker-compose.prod.yml down
    docker-compose -f docker-compose.prod.yml up --build -d
    echo "✅ Production environment started!"
    echo "🌐 Frontend: http://localhost"
    echo "🔧 Backend API: http://localhost/api"
    echo "📚 API Docs: http://localhost/docs"
}

# Function to stop all services
stop_all() {
    echo "🛑 Stopping all services..."
    docker-compose down
    docker-compose -f docker-compose.prod.yml down
    echo "✅ All services stopped!"
}

# Function to show logs
show_logs() {
    echo "📋 Showing logs..."
    docker-compose logs -f
}

# Function to show status
show_status() {
    echo "📊 Service Status:"
    docker-compose ps
}

# Main menu
case "$1" in
    "dev")
        start_dev
        ;;
    "prod")
        start_prod
        ;;
    "stop")
        stop_all
        ;;
    "logs")
        show_logs
        ;;
    "status")
        show_status
        ;;
    *)
        echo "Usage: $0 {dev|prod|stop|logs|status}"
        echo ""
        echo "Commands:"
        echo "  dev     - Start development environment"
        echo "  prod    - Start production environment with nginx"
        echo "  stop    - Stop all services"
        echo "  logs    - Show service logs"
        echo "  status  - Show service status"
        echo ""
        echo "Examples:"
        echo "  $0 dev     # Start development"
        echo "  $0 prod    # Start production"
        echo "  $0 stop    # Stop all services"
        exit 1
        ;;
esac