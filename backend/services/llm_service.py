"""LLM service using Google Gemini"""
import google.generativeai as genai
from config import Config
import logging

logger = logging.getLogger(__name__)

class LLMService:
    """Handles conversation with Gemini LLM"""
    
    def __init__(self):
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        
        self.model = genai.GenerativeModel(
            model_name=Config.GEMINI_MODEL,
            system_instruction="""You are a friendly, patient AI tutor assistant. 
            Your role is to help students learn by:
            - Explaining concepts clearly in simple language
            - Being encouraging and supportive
            - Asking clarifying questions when needed
            - Breaking down complex topics into smaller parts
            - Providing examples when helpful
            
            Keep responses concise (2-3 sentences for voice).
            Be conversational and natural."""
        )
        
        # Store sessions in memory (will add DB later)
        self.sessions = {}
        
        logger.info("LLMService initialized")
    
    def get_response(self, message: str, session_id: str = "default") -> str:
        """
        Get AI response from Gemini
        Args:
            message: User's text input
            session_id: Unique session identifier
        Returns:
            AI response text
        """
        try:
            # Get or create session
            if session_id not in self.sessions:
                self.sessions[session_id] = self.model.start_chat(history=[])
                logger.info(f"New session created: {session_id}")
            
            chat = self.sessions[session_id]
            
            # Get response
            response = chat.send_message(message)
            logger.info(f"Response generated for session {session_id}")
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error in get_response: {e}")
            raise
    
    def transcribe_audio(self, audio_bytes: bytes) -> str:
        """
        Transcribe audio using Gemini
        Args:
            audio_bytes: Audio data in bytes
        Returns:
            Transcribed text
        """
        try:
            transcription_model = genai.GenerativeModel(
                model_name=Config.GEMINI_MODEL,
            )
            
            response = transcription_model.generate_content(
                [
                    "Transcribe this audio to text. Only return the exact spoken words.",
                    {"mime_type": "audio/wav", "data": audio_bytes}
                ],
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,
                    temperature=0.1,
                )
            )
            
            transcription = response.text.strip()
            logger.info(f"Transcription successful: {transcription[:50]}...")
            
            return transcription
            
        except Exception as e:
            logger.error(f"Error in transcribe_audio: {e}")
            raise
    
    def clear_session(self, session_id: str):
        """Clear specific session history"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Session cleared: {session_id}")
