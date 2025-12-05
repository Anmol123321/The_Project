"""
AI Tutor Voice Assistant - Streamlit App
Main application file
"""
import streamlit as st
from config import Config
from services import SpeechService, LLMService, TTSService
from utils.helpers import init_session_state, display_chat_history, add_message, clear_chat
from utils.logger import logger
import hashlib
import time

# Page configuration
st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon=Config.APP_ICON,
    layout="centered",
    initial_sidebar_state="expanded"
)

logger.info("="*50)
logger.info("Application started")
logger.info("="*50)

# Validate API keys
Config.validate()
logger.info("API keys validated")

# Initialize session state
init_session_state()
logger.info("Session state initialized")

# Add audio processing flag to session state
if 'processing_audio' not in st.session_state:
    st.session_state.processing_audio = False
if 'last_audio_id' not in st.session_state:
    st.session_state.last_audio_id = None
if 'last_audio_response' not in st.session_state:
    st.session_state.last_audio_response = None

# Initialize services (cached)
@st.cache_resource
def get_services():
    """Initialize and cache service instances"""
    logger.info("Initializing services...")
    return {
        'speech': SpeechService(),
        'llm': LLMService(),
        'tts': TTSService()
    }

services = get_services()
logger.info("All services initialized successfully")

# App Header
st.title(Config.APP_TITLE)
st.markdown("**Your friendly AI learning companion** 🚀")
st.divider()

# Sidebar
with st.sidebar:
    st.header("⚙️ Controls")
    
    # Voice input using Streamlit's audio_input
    st.subheader("🎤 Voice Input")
    audio_bytes = st.audio_input("Record your question")
    
    # Only process if we have new audio and not already processing
    if audio_bytes and not st.session_state.processing_audio:
        # Create unique ID for this audio to prevent reprocessing
        audio_id = hashlib.md5(audio_bytes.getvalue()).hexdigest()
        
        # Check if this is new audio
        if audio_id != st.session_state.last_audio_id:
            logger.info(f"New audio input detected (ID: {audio_id[:8]}...)")
            st.session_state.processing_audio = True
            st.session_state.last_audio_id = audio_id
            
            with st.spinner("🎧 Transcribing your voice..."):
                # Transcribe using Gemini
                user_text = services['llm'].transcribe_audio(audio_bytes)
            
            if user_text:
                logger.info(f"Transcription complete: {user_text}")
                st.success(f"✅ You said: *{user_text}*")
                
                # Add to chat
                add_message("user", user_text)
                logger.debug("User message added to chat history")
                
                # Get AI response
                with st.spinner("🤔 Thinking..."):
                    ai_response = services['llm'].get_response(user_text)
                
                logger.info(f"AI response generated: {ai_response[:100]}...")
                add_message("assistant", ai_response)
                logger.debug("Assistant message added to chat history")
                
                # Convert to speech and store in session state
                with st.spinner("🔊 Generating voice..."):
                    audio_response = services['tts'].synthesize_speech(ai_response)
                    
                    if audio_response:
                        logger.info("TTS generation successful")
                        # Store in session state to play after rerun
                        st.session_state.last_audio_response = audio_response
                    else:
                        logger.warning("TTS generation failed - no audio returned")
                
                st.session_state.conversation_count += 1
                logger.info(f"Conversation count: {st.session_state.conversation_count}")
                
                # Reset processing flag
                st.session_state.processing_audio = False
                
                # Force rerun to update UI
                st.rerun()
            else:
                logger.warning("Transcription returned None - no text extracted from audio")
                st.session_state.processing_audio = False
        else:
            logger.debug(f"Skipping already processed audio (ID: {audio_id[:8]}...)")
    
    st.divider()
    
    # Text input alternative
    st.subheader("💬 Or Type Instead")
    text_input = st.text_input("Type your message:", key="text_input_sidebar")
    
    if st.button("Send Text", use_container_width=True):
        if text_input.strip():
            logger.info(f"Text input received: {text_input}")
            
            # Display user message
            add_message("user", text_input)
            logger.debug("User text message added to chat")
            
            # Get AI response
            with st.spinner("🤔 Thinking..."):
                ai_response = services['llm'].get_response(text_input)
            
            logger.info(f"AI response for text input: {ai_response[:100]}...")
            add_message("assistant", ai_response)
            
            # Convert to speech and store
            with st.spinner("🔊 Generating voice..."):
                audio_bytes_response = services['tts'].synthesize_speech(ai_response)
                
                if audio_bytes_response:
                    logger.info("TTS for text input successful")
                    st.session_state.last_audio_response = audio_bytes_response
                else:
                    logger.warning("TTS for text input failed")
            
            st.session_state.conversation_count += 1
            logger.info(f"Conversation count: {st.session_state.conversation_count}")
            st.rerun()
        else:
            logger.warning("Empty text input submitted")
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        logger.info("Clear chat button clicked")
        clear_chat()
        services['llm'].clear_history()
        st.session_state.last_audio_id = None  # Reset audio tracking
        st.session_state.last_audio_response = None  # Clear audio
        logger.info("Chat history cleared")
        st.rerun()
    
    # Stats
    st.divider()
    st.metric("💬 Messages", len(st.session_state.messages))
    st.metric("🔄 Conversations", st.session_state.conversation_count)
    
    # Debug: Show logs location
    st.divider()
    st.caption("📝 Logs saved to: `logs/` folder")

# Play last audio response if available (BEFORE chat display)
if st.session_state.last_audio_response:
    logger.info("Playing stored audio response")
    st.success("🔊 **AI Response (Audio):**")
    st.audio(st.session_state.last_audio_response, format="audio/mp3", autoplay=True)
    # Clear after displaying once
    st.session_state.last_audio_response = None
    logger.debug("Audio response cleared from session state")

st.divider()

# Main chat display
if st.session_state.messages:
    logger.debug(f"Displaying {len(st.session_state.messages)} messages")
    display_chat_history()
else:
    logger.debug("No messages in history - showing welcome message")
    # Welcome message
    st.info("""
    👋 **Welcome to your AI Tutor!**
    
    Click **🎤 Record** in the sidebar to speak with me, or type your questions below.
    
    **Try asking:**
    - "Explain photosynthesis"
    - "Help me with algebra"
    - "What is Newton's first law?"
    """)

# Footer
st.divider()
st.caption("Powered by Google Gemini 🧠 + ElevenLabs 🔊")

logger.debug("App render complete")
