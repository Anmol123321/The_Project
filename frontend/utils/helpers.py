"""Helper utilities for the app"""
import streamlit as st

def init_session_state():
    """Initialize Streamlit session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0
    
    if 'last_audio_response' not in st.session_state:
        st.session_state.last_audio_response = None
    
    if 'backend_connected' not in st.session_state:
        st.session_state.backend_connected = False

def display_chat_history():
    """Display chat message history"""
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        # Choose avatar based on role
        avatar = "🎓" if role == "assistant" else "👤"
        
        with st.chat_message(role, avatar=avatar):
            st.markdown(content)

def add_message(role: str, content: str):
    """Add message to chat history"""
    st.session_state.messages.append({
        "role": role,
        "content": content
    })

def clear_chat():
    """Clear all chat history"""
    st.session_state.messages = []
    st.session_state.conversation_count = 0
