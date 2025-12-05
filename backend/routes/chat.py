"""Chat endpoints with INSTANT VOICE (TTS Turbo)"""
from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse
from services import LLMService, TTSService
import uuid
import base64
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send message → AI Text → INSTANT VOICE (300ms!)"""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Step 1: AI Text Response
        llm_service = LLMService()
        ai_response = llm_service.get_response(request.message, session_id)
        
        # Step 2: FAST VOICE (Turbo model)
        tts_service = TTSService()
        audio_bytes = tts_service.synthesize_speech(ai_response)
        
        # Step 3: Base64 for browser playback
        audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
        audio_url = f"data:audio/mp3;base64,{audio_b64}"
        
        logger.info(f"⚡ Chat+Voice COMPLETE! Session: {session_id[:8]} | Audio: {len(audio_bytes)} bytes")
        
        return ChatResponse(
            response=ai_response,
            session_id=session_id,
            audio_url=audio_url  # 🎤 Ready to play!
        )
        
    except Exception as e:
        logger.error(f"❌ Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear chat history"""
    llm_service = LLMService()
    llm_service.clear_session(session_id)
    return {"status": "cleared"}
