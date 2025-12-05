"""Health check endpoints"""
from fastapi import APIRouter
from models.schemas import HealthResponse              # ✅ Fixed
from config import Config

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health and service status"""
    return HealthResponse(
        status="healthy",
        version=Config.VERSION,
        services={
            "llm": "operational",
            "tts": "operational",
            "database": "not_configured"
        }
    )

@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Tutor Voice Assistant API",
        "version": Config.VERSION,
        "docs": "/docs",
        "health": "/health"
    }
