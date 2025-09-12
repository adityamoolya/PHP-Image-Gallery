# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

import models
from database import engine, Base
from routers import auth, posts, comments, images, albums

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# The startup event is now async
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

# This is the CORS "guest list" configuration.
# For production, you should restrict this to your frontend's actual URL.
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173", # Default for Vite/React dev server
    "https://clonefest.up.railway.app/", # Default for Vite/React dev server
    # "https://your-vercel-frontend-url.vercel.app", # <-- ADD YOUR DEPLOYED FRONTEND URL HERE
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # The list of "guests" who are allowed to talk to the API
    allow_credentials=True, # Allows cookies to be included in requests
    allow_methods=["*"],    # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],    # Allows all headers
)

# Include all the new routers
logger.info("Registering routers...")
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(images.router)
app.include_router(albums.router)
logger.info("Routers registered successfully.")

# Health check endpoint
@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "message": "Image Gallery API is running",
        "status": "healthy",
        "docs_url": "/docs"
    }
