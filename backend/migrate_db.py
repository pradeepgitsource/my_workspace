from sqlalchemy.ext.asyncio import create_async_engine
from app.core.models import Base
from app.core.user_models import User
import asyncio
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://postgres:password@localhost:5432/flight_checkin"
)

async def migrate_database():
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        # Drop users table if exists
        await conn.execute("DROP TABLE IF EXISTS users CASCADE")
        
        # Recreate all tables
        await conn.run_sync(Base.metadata.create_all)
    
    await engine.dispose()
    print("Database migration completed successfully!")

if __name__ == "__main__":
    asyncio.run(migrate_database())