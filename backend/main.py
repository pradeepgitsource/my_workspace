from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging
import time

from database import create_tables
from routes import flights, passengers, checkin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Flight Web Check-in API",
    description="Production-grade flight check-in system with PostgreSQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"{request.method} {request.url.path} - {request.client.host}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
    
    return response

# Include routers
app.include_router(flights.router)
app.include_router(passengers.router)
app.include_router(checkin.router)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Creating database tables...")
    await create_tables()
    logger.info("Database tables created successfully")

@app.get("/")
async def root():
    """API information"""
    return {
        "message": "Flight Web Check-in API",
        "version": "1.0.0",
        "status": "running",
        "database": "PostgreSQL",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "flights": "/api/flights",
            "passengers": "/api/passengers",
            "bookings": "/api/bookings",
            "checkin": "/api/checkin"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0",
        "database": "PostgreSQL"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Flight Check-in API with PostgreSQL...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")