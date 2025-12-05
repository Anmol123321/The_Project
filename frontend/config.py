"""Configuration for Streamlit frontend"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    
    # Model Settings
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")
    
    # App Settings
    APP_TITLE = "🎓 AI Voice Tutor"
    APP_ICON = "🎓"
    
    @classmethod
    def validate(cls):
        """Validate required environment variables"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("❌ GOOGLE_API_KEY not found in .env file!")
        if not cls.ELEVENLABS_API_KEY:
            raise ValueError("❌ ELEVENLABS_API_KEY not found in .env file!")
