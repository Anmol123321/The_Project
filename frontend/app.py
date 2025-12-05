"""
🎓 FULL VOICE TUTOR - AUTO SPEAK
Correct Logic: Process -> Store Audio -> Rerun -> Auto-Play at Top
"""
import streamlit as st
import requests
import hashlib
from config import Config
from utils.helpers import init_session_state, display_chat_history, add_message, clear_chat
from utils.logger import logger

API_URL = "http://localhost:8000"

st.set_page_config(page_title="🎓 Voice Tutor", page_icon="🎤", layout="wide")
init_session_state()

# Initialize processing flags
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'last_audio_id' not in st.session_state:
    st.session_state.last_audio_id = None
if 'play_audio_url' not in st.session_state:
    st.session_state.play_audio_url = None

# ---------------------------------------------------------
# 🔊 AUTO-PLAY LOGIC (MUST BE AT THE TOP)
# ---------------------------------------------------------
if st.session_state.play_audio_url:
    logger.info("🔊 Auto-playing audio response...")
    st.audio(st.session_state.play_audio_url, format="audio/mp3", autoplay=True)
    st.success("🔊 AI Speaking...")
    st.session_state.play_audio_url = None  # Clear so it plays only once

# ---------------------------------------------------------
# MAIN UI
# ---------------------------------------------------------
st.title("🎤 **Voice Tutor** - Speak → AI Speaks! 🔊")
st.markdown("**🎙️ Record → AI Thinks → 🔊 Auto Speaks!**")
st.divider()

# Status Check
try:
    requests.get(f"{API_URL}/health", timeout=2)
    st.sidebar.success("✅ Backend LIVE")
except:
    st.error("❌ Backend OFF! Run `python main.py` in backend folder.")
    st.stop()

# ---------------------------------------------------------
# 🎙️ VOICE RECORDING & PROCESSING
# ---------------------------------------------------------
st.markdown("### 🎙️ **Record Your Question**")

# Try to use the new audio_input if available (Streamlit 1.40+)
try:
    audio_bytes = st.audio_input("Click to record")
except AttributeError:
    st.error("⚠️ Please run `pip install streamlit --upgrade` to use st.audio_input")
    st.stop()

# Process Logic
if audio_bytes and not st.session_state.processing:
    # Detect new audio
    audio_id = hashlib.md5(audio_bytes.getvalue()).hexdigest()[:8]
    
    if audio_id != st.session_state.last_audio_id:
        st.session_state.processing = True
        st.session_state.last_audio_id = audio_id
        
        with st.spinner("🎧 Transcribing... 🤖 Thinking..."):
            try:
                # 1. Transcribe
                files = {"audio": audio_bytes.getvalue()}
                transcribe_resp = requests.post(f"{API_URL}/api/voice/transcribe", files=files)
                
                if transcribe_resp.status_code == 200:
                    user_text = transcribe_resp.json()['transcription']
                    add_message("user", user_text)
                    
                    # 2. Get AI Response + Audio
                    chat_resp = requests.post(f"{API_URL}/api/chat/", json={"message": user_text})
                    
                    if chat_resp.status_code == 200:
                        data = chat_resp.json()
                        ai_text = data['response']
                        audio_url = data.get('audio_url')
                        
                        add_message("assistant", ai_text)
                        
                        # 3. STORE AUDIO FOR AUTO-PLAY
                        if audio_url:
                            st.session_state.play_audio_url = audio_url
                        
                        st.session_state.processing = False
                        st.rerun()  # Refresh page to trigger Auto-Play at top
                    else:
                        st.error(f"Chat Error: {chat_resp.text}")
                else:
                    st.error("Transcription Failed")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                st.session_state.processing = False

# ---------------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------------
st.divider()
if st.session_state.messages:
    display_chat_history()

# Sidebar Controls
if st.sidebar.button("🗑️ Clear Chat"):
    clear_chat()
    st.session_state.last_audio_id = None
    st.session_state.play_audio_url = None
    st.rerun()
