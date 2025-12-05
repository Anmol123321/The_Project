"""Voice Input (STT)"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from models.schemas import TranscribeResponse
from services import LLMService
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/voice", tags=["Voice"])

llm_service = LLMService()

@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(audio: UploadFile = File(...)):
    """🎙️ Voice → Text"""
    try:
        audio_bytes = await audio.read()
        logger.info(f"🎙️ Transcribing {len(audio_bytes)} bytes")
        
        transcription = llm_service.transcribe_audio(audio_bytes)
        logger.info(f"✅ Transcribed: '{transcription}'")
        
        return TranscribeResponse(transcription=transcription)
    except Exception as e:
        logger.error(f"❌ Transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
