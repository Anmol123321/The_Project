"""Perfect TTS Settings - No Skips"""
from elevenlabs.client import ElevenLabs
from config import Config
import logging

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        self.client = ElevenLabs(api_key=Config.ELEVENLABS_API_KEY)
        self.voice_id = Config.ELEVENLABS_VOICE_ID

    def synthesize_speech(self, text: str) -> bytes:
        try:
            # Generate audio with STABLE settings to prevent skipping
            audio = self.client.text_to_speech.convert(
                voice_id=self.voice_id,
                text=text,
                model_id="eleven_multilingual_v2",
                voice_settings={
                    "stability": 0.5,        # Balanced stability
                    "similarity_boost": 0.75, # Clear voice
                    "style": 0.0,            # Neutral style (faster processing)
                    "use_speaker_boost": True
                }
            )
            return b"".join(audio)
        except Exception as e:
            logger.error(f"TTS Error: {e}")
            return b""
