"""
AI Tutor Voice Assistant - FastAPI Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Config
from routes import chat_router, voice_router, health_router
from utils.logger import get_logger  # ✅ Updated import

# Get logger for this module
logger = get_logger(__name__)

# Validate configuration
Config.validate()
logger.info("Configuration validated")

# Create FastAPI app
app = FastAPI(
    title=Config.APP_NAME,
    version=Config.VERSION,
    description="Backend API for AI Voice Tutor",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(voice_router)

logger.info("FastAPI app initialized")

@app.on_event("startup")
async def startup_event():
    logger.info("="*50)
    logger.info(f"{Config.APP_NAME} started")
    logger.info(f"Version: {Config.VERSION}")
    logger.info(f"Logs location: logs/api.log")
    logger.info("="*50)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None  # Use our custom logging
    )
