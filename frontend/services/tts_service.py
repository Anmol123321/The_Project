"""Text-to-Speech service using ElevenLabs"""
from elevenlabs import ElevenLabs
from config import Config
import streamlit as st
from utils.logger import logger


class TTSService:
    """Handles text-to-speech conversion"""
    
    def __init__(self):
        logger.info("Initializing TTSService...")
        self.client = ElevenLabs(api_key=Config.ELEVENLABS_API_KEY)
        self.voice_id = Config.ELEVENLABS_VOICE_ID
        logger.info(f"ElevenLabs client initialized with voice: {self.voice_id}")
    
    def synthesize_speech(self, text: str) -> bytes:
        """
        Convert text to speech
        Args: text - Text to convert to speech
        Returns: Audio bytes (MP3 format)
        """
        logger.info(f"Synthesizing speech for text: {text[:100]}...")
        
        try:
            # Generate audio using ElevenLabs
            audio_generator = self.client.text_to_speech.convert(
                voice_id=self.voice_id,
                text=text,
                model_id="eleven_multilingual_v2"
            )
            
            # Collect all audio chunks
            audio_bytes = b"".join(audio_generator)
            
            logger.info(f"Speech synthesis successful. Audio size: {len(audio_bytes)} bytes")
            return audio_bytes
            
        except Exception as e:
            logger.error(f"Error in synthesize_speech: {type(e).__name__}: {str(e)}")
            logger.exception("Full traceback:")
            
            st.error(f"❌ TTS Error: {e}")
            return None
