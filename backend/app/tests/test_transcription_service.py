import pytest
from app.services.transcription_service import TranscriptionService

@pytest.mark.asyncio
async def test_transcribe_mock():
    """Test mock transcription service."""
    service = TranscriptionService()
    service.use_whisper = False  # Force mock mode
    
    # Create dummy audio bytes
    audio_bytes = b"fake audio content"
    
    result = await service.transcribe(audio_bytes, "test.wav")
    
    assert "text" in result
    assert "confidence" in result
    assert isinstance(result["text"], str)
    assert len(result["text"]) > 0
    assert 0 <= result["confidence"] <= 1

