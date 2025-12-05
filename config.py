"""Configuration and API key management"""
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv(encoding='utf-8-sig')

class Config:
    """Application configuration"""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    
    # Model settings
    GEMINI_MODEL = "gemini-2.5-flash"  # ✅ Updated to 2.0
    ELEVENLABS_VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam voice
    ELEVENLABS_MODEL = "eleven_flash_v2_5"
    
    # App settings
    APP_TITLE = "🎓 AI Tutor Voice Assistant"
    APP_ICON = "🎓"
    
    @classmethod
    def validate(cls):
        """Validate required API keys"""
        if not cls.GOOGLE_API_KEY:
            st.error("❌ GOOGLE_API_KEY missing from .env file")
            st.stop()
        if not cls.ELEVENLABS_API_KEY:
            st.error("❌ ELEVENLABS_API_KEY missing from .env file")
            st.stop()
