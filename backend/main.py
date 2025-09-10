# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# --- MODIFIED: Import our new models and async engine ---
import models
from database import engine, Base

# --- MODIFIED: Import all our new and refactored routers ---
from routers import auth, posts, comments, images, albums

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- MODIFIED: The startup event is now async ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup...")
    async with engine.begin() as conn:
        # This creates the database tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created/verified.")
    yield
    logger.info("Application shutdown...")


# Initialize FastAPI app with a new title and the async lifespan manager
app = FastAPI(
    title="CloneFest 2025 - Image Gallery API",
    description="A modern, extensible media platform API.",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware (no change needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODIFIED: Include all the new routers ---
logger.info("Registering routers...")
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(images.router)
app.include_router(albums.router)
logger.info("Routers registered successfully.")

# --- REMOVED: All code related to the local 'uploads' directory ---

# Health check endpoint
@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "message": "Image Gallery API is running",
        "status": "healthy",
        "docs_url": "/docs"
    }