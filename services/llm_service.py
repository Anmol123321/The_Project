"""LLM service using Google Gemini"""
import google.generativeai as genai
from google.genai import types
from config import Config
import streamlit as st
from utils.logger import logger


class LLMService:
    """Handles conversation with Gemini LLM"""
    
    def __init__(self):
        logger.info("Initializing LLMService...")
        
        # Configure Gemini
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        logger.info(f"Gemini configured with model: {Config.GEMINI_MODEL}")
        
        # Initialize model with tutor system prompt
        self.model = genai.GenerativeModel(
            model_name=Config.GEMINI_MODEL,
            system_instruction="""You are a friendly, patient AI tutor assistant. 
            Your role is to help students learn by:
            - Explaining concepts clearly in simple language
            - Being encouraging and supportive
            - Asking clarifying questions when needed
            - Breaking down complex topics into smaller parts
            - Providing examples when helpful
            
            Keep responses concise (2-3 sentences max for voice).
            Be conversational and natural."""
        )
        
        # Start chat session
        self.chat = self.model.start_chat(history=[])
        logger.info("Chat session started successfully")
    
    def get_response(self, user_message: str) -> str:
        """
        Get AI response from Gemini
        Args: user_message - User's text input
        Returns: AI response text
        """
        logger.info(f"User message received: {user_message[:100]}...")
        
        try:
            logger.debug("Sending message to Gemini...")
            response = self.chat.send_message(user_message)
            
            logger.info(f"AI response received: {response.text[:100]}...")
            logger.debug(f"Full response: {response.text}")
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error in get_response: {type(e).__name__}: {str(e)}")
            logger.exception("Full traceback:")
            
            st.error(f"❌ AI Error: {e}")
            return "😅 Sorry, I had trouble processing that. Could you try again?"
    
    def transcribe_audio(self, audio_data) -> str:
        """
        Transcribe audio using Gemini's multimodal capability
        Args: audio_data - Audio bytes or UploadedFile object
        Returns: Transcribed text
        """
        logger.info("Starting audio transcription...")
        
        try:
            # Handle both bytes and UploadedFile objects
            if hasattr(audio_data, 'read'):
                logger.debug("Reading audio from UploadedFile object")
                audio_bytes = audio_data.read()
            else:
                logger.debug("Using audio bytes directly")
                audio_bytes = audio_data
            
            logger.info(f"Audio data size: {len(audio_bytes)} bytes")
            
            # Create a temporary model instance for transcription
            transcription_model = genai.GenerativeModel(
                model_name=Config.GEMINI_MODEL,
            )
            
            logger.debug("Sending audio to Gemini for transcription...")
            
            # Use generate_content with explicit config for higher output tokens
            response = transcription_model.generate_content(
                [
                    "Transcribe this audio to text. Only return the exact spoken words, nothing else.",
                    {"mime_type": "audio/wav", "data": audio_bytes}
                ],
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2000,  # Increased limit to prevent MAX_TOKENS error
                    temperature=0.1,  # Low temperature for accurate transcription
                )
            )
            
            # Check if response has valid parts
            if not response.candidates or not response.candidates[0].content.parts:
                finish_reason = response.candidates[0].finish_reason if response.candidates else "N/A"
                logger.error(f"No valid response parts. Finish reason: {finish_reason}")
                st.error("❌ Audio transcription failed - no response from model")
                return None
            
            transcribed_text = response.text.strip()
            logger.info(f"Transcription successful: {transcribed_text}")
            
            return transcribed_text
            
        except ValueError as e:
            logger.error(f"ValueError in transcribe_audio: {str(e)}")
            if 'response' in locals() and response.candidates:
                logger.error(f"Response finish reason: {response.candidates[0].finish_reason}")
            st.error("❌ Transcription failed - please try recording again")
            return None
            
        except Exception as e:
            logger.error(f"Error in transcribe_audio: {type(e).__name__}: {str(e)}")
            logger.exception("Full traceback:")
            
            st.error(f"❌ Transcription error: {e}")
            return None
    
    def get_chat_history(self):
        """Return current chat history"""
        logger.debug("Retrieving chat history")
        return self.chat.history
    
    def clear_history(self):
        """Reset conversation history"""
        logger.info("Clearing chat history")
        self.chat = self.model.start_chat(history=[])
