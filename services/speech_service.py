"""Speech-to-Text service using Streamlit audio input"""
import streamlit as st
import io
import wave

class SpeechService:
    """Handles voice input using Streamlit's native audio recorder"""
    
    def __init__(self):
        pass
    
    def get_audio_input_widget(self):
        """
        Display Streamlit audio input widget
        Returns: Audio bytes from microphone or None
        """
        audio_bytes = st.audio_input("🎤 Click to record your voice")
        return audio_bytes
    
    def transcribe_with_gemini(self, audio_bytes: bytes, gemini_model) -> str:
        """
        Transcribe audio using Gemini's built-in audio understanding
        Args: 
            audio_bytes - Audio file bytes
            gemini_model - Gemini model instance
        Returns: Transcribed text
        """
        if not audio_bytes:
            return None
            
        try:
            # Gemini can process audio directly!
            response = gemini_model.generate_content([
                "Transcribe this audio to text. Only return the exact spoken words, nothing else.",
                {"mime_type": "audio/wav", "data": audio_bytes}
            ])
            return response.text.strip()
            
        except Exception as e:
            st.error(f"❌ Transcription error: {e}")
            return None
