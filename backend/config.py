"""Configuration for FastAPI backend"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    
    # Model Settings
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")
    
    # App Settings
    APP_NAME = "AI Tutor Voice Assistant API"
    VERSION = "1.0.0"
    
    @classmethod
    def validate(cls):
        """Validate required environment variables"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment")
        if not cls.ELEVENLABS_API_KEY:
            raise ValueError("ELEVENLABS_API_KEY not found in environment")
