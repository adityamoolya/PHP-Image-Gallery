from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
import models
from database import engine, SessionLocal
from routers import blog, auth, comment
import logging
import os
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_uploads_directory():
    """Create uploads directory if it doesn't exist"""
    try:
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
            logger.info("Created uploads directory")
        return True
    except Exception as e:
        logger.error(f"Failed to create uploads directory: {e}")
        return False

def setup_database():
    """Set up database tables"""
    try:
        models.Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified")
        return True
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        return False

def test_db_connection():
    """Test database connection"""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {str(e)}")
        return False

# Initialize components
try:
    create_uploads_directory()
    setup_database()
    db_connected = test_db_connection()
except Exception as e:
    logger.critical(f"Failed to initialize application: {e}")
    # Don't crash immediately, let the app start but log the error

# Initialize FastAPI app
app = FastAPI(
    title="Chyrp",
    description="backend of chryp",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
try:
    app.include_router(auth.router)
    app.include_router(blog.router)
    app.include_router(comment.router)
    logger.info("Routers registered successfully")
except Exception as e:
    logger.error(f"Failed to register routers: {e}")

# Serve uploaded files only if directory exists
try:
    if os.path.exists("uploads"):
        app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
        logger.info("Serving uploads from filesystem")
    else:
        logger.warning("Uploads directory does not exist, file serving disabled")
except Exception as e:
    logger.error(f"Failed to setup static files: {e}")

# Health check endpoint
@app.get("/")
def read_root():
    return {
        "message": "Modern Chyrp API is running",
        "status": "healthy",
        "docs": "/docs"
    }

# Health check endpoint with database status
@app.get("/health")
def health_check():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)