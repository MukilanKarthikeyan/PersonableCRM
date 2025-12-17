# backend/app/main.py

"""
PersonableCRM - FastAPI Backend
A personal CRM powered by Lux AI for intelligent people research.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import Base, engine
from app.routes import contacts, research
from app.config import APP_NAME, APP_VERSION, CORS_ORIGINS, DEBUG
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
logger.info("Creating database tables...")
Base.metadata.create_all(bind=engine)
logger.info("Database tables created successfully")

# Initialize FastAPI app
app = FastAPI(
    title=APP_NAME,
    description="Personal CRM with AI-powered people research using Lux",
    version=APP_VERSION,
    debug=DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(contacts.router, prefix="/api", tags=["Contacts"])
app.include_router(research.router, prefix="/api", tags=["Research"])

logger.info("API routes registered")


@app.get("/")
def root():
    """
    Root endpoint - API information
    """
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "description": "Personal CRM with AI-powered people research",
        "endpoints": {
            "docs": "/docs",
            "contacts": "/api/contacts",
            "research": "/api/research",
            "health": "/health"
        }
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": APP_NAME,
        "version": APP_VERSION
    }


@app.on_event("startup")
async def startup_event():
    """
    Run on application startup
    """
    logger.info(f"{APP_NAME} v{APP_VERSION} starting up...")
    logger.info(f"Debug mode: {DEBUG}")
    logger.info(f"Allowed CORS origins: {CORS_ORIGINS}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown
    """
    logger.info(f"{APP_NAME} shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=DEBUG
    )