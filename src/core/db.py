from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

# Create the SQLAlchemy async engine using the database URL from settings
engine = create_async_engine(
    settings.database_url,
    echo=False,  # Enable SQL logging for debugging; set to False in production
)

# Create a session factory for database interactions
async_session = sessionmaker(
    engine,
    expire_on_commit=False,  # Keeps objects "alive" after commit to prevent re-fetching
    class_=AsyncSession,  # Use the async session for asyncio compatibility
)

async def get_db():
    """
    Dependency for injecting database sessions into FastAPI routes.

    This function provides a scoped session for the lifecycle of a request,
    ensuring proper cleanup after use.

    Yields:
        AsyncSession: An SQLAlchemy AsyncSession instance.
    """
    async with async_session() as session:
        yield session
