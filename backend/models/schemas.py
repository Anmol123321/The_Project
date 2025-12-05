from typing import Optional, Dict
from pydantic import BaseModel


class ChatRequest(BaseModel):
	message: str
	session_id: Optional[str] = None


class ChatResponse(BaseModel):
	response: str
	session_id: str
	audio_url: Optional[str] = None


class TranscribeRequest(BaseModel):
	# placeholder for possible future fields
	language: Optional[str] = None


class TranscribeResponse(BaseModel):
	transcription: str
	confidence: Optional[float] = None


class TTSRequest(BaseModel):
	text: str
	voice_id: Optional[str] = None


class TTSResponse(BaseModel):
	# We'll return either raw bytes encoded elsewhere or a URL
	audio_url: Optional[str] = None


class HealthResponse(BaseModel):
	status: str
	version: str
	services: Dict[str, str]


__all__ = [
	"ChatRequest",
	"ChatResponse",
	"TranscribeRequest",
	"TranscribeResponse",
	"TTSRequest",
	"TTSResponse",
	"HealthResponse",
]

