
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Column, String, Float, JSON
import os

# --- Database Configuration ---
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please set it to your PostgreSQL connection string.")

# Use 'postgresql+asyncpg://' for async operations
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

# --- ORM Model ---
class OpportunityORM(Base):
    """SQLAlchemy ORM Model for an Opportunity"""
    __tablename__ = "opportunities"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    asset: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    confidence: Mapped[float] = mapped_column(Float)
    rationale: Mapped[str] = mapped_column(String)
    sources: Mapped[list] = mapped_column(JSON)
    metrics: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[str] = mapped_column(String)
    expires_at: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="active")
    tags: Mapped[list] = mapped_column(JSON)

async def get_db():
    """Dependency to get a database session."""
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    """Initialize the database and create tables."""
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Optional: drop tables for a clean start
        await conn.run_sync(Base.metadata.create_all)
