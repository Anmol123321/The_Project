"""Service exports with graceful fallback when optional deps missing."""

__all__ = ["LLMService", "TTSService"]

try:
	from .llm_service import LLMService  # type: ignore
except Exception as _err:  # pragma: no cover - fallback for missing deps
	class LLMService:  # type: ignore
		def __init__(self, *args, **kwargs):
			raise RuntimeError(
				f"LLMService unavailable: {_err}. Install optional dependency 'google-generativeai' or configure accordingly."
			)

try:
	from .tts_service import TTSService  # type: ignore
except Exception as _err:  # pragma: no cover - fallback for missing deps
	class TTSService:  # type: ignore
		def __init__(self, *args, **kwargs):
			raise RuntimeError(
				f"TTSService unavailable: {_err}. Install optional dependency 'elevenlabs' or configure accordingly."
			)
