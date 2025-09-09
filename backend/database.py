import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)

# Use environment variable for database URL with SQLite as fallback
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db")

# Fix for PostgreSQL URL format
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

logger.info(f"Using database URL: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL}")

# Create database engine with appropriate connection arguments
try:
    if DATABASE_URL.startswith("sqlite"):
        engine = create_engine(
            DATABASE_URL, 
            connect_args={"check_same_thread": False},
            pool_pre_ping=True
        )
    else:
        # For PostgreSQL
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,  # Check connection before using
            pool_recycle=300,    # Recycle connections after 5 minutes
            pool_size=5,         # Maximum number of connections
            max_overflow=10      # Maximum overflow connections
        )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    
    logger.info("Database engine created successfully")
    
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    # Fallback to SQLite if PostgreSQL fails
    DATABASE_URL = "sqlite:///./blog.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.warning(f"Falling back to SQLite: {DATABASE_URL}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()