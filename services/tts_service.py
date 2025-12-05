"""Text-to-Speech service using ElevenLabs"""
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from config import Config
import streamlit as st
from utils.logger import logger  # ✅ Import logger


class TTSService:
    """Handles text-to-speech conversion"""
    
    def __init__(self):
        logger.info("Initializing TTSService...")
        self.client = ElevenLabs(api_key=Config.ELEVENLABS_API_KEY)
        logger.info(f"ElevenLabs client initialized with voice: {Config.ELEVENLABS_VOICE_ID}")
    
    def synthesize_speech(self, text: str) -> bytes:
        """
        Convert text to speech audio
        Args: text - Text to convert
        Returns: Audio bytes (MP3 format)
        """
        logger.info(f"Synthesizing speech for text: {text[:100]}...")
        
        try:
            logger.debug(f"Using model: {Config.ELEVENLABS_MODEL}")
            
            # Generate audio using ElevenLabs
            audio_generator = self.client.generate(
                text=text,
                voice=Config.ELEVENLABS_VOICE_ID,
                model=Config.ELEVENLABS_MODEL,
                voice_settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                    style=0.0,
                    use_speaker_boost=True
                )
            )
            
            # Convert generator to bytes
            logger.debug("Converting audio generator to bytes...")
            audio_bytes = b"".join(audio_generator)
            
            logger.info(f"Speech synthesis successful. Audio size: {len(audio_bytes)} bytes")
            return audio_bytes
            
        except Exception as e:
            logger.error(f"Error in synthesize_speech: {type(e).__name__}: {str(e)}")
            logger.exception("Full traceback:")
            
            st.error(f"❌ TTS Error: {e}")
            return None
