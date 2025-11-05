import pytest
from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path
import io

client = TestClient(app)

@pytest.fixture
def sample_audio_bytes():
    """Create sample audio bytes for testing."""
    # Create a minimal WAV file header (just for testing, not a real audio file)
    # In real scenarios, you would load an actual audio file
    return b"RIFF" + b"\x00" * 40  # Minimal WAV-like bytes


def test_transcribe_with_mock_audio_file(sample_audio_bytes):
    """Test transcription endpoint with mock audio file."""
    # Create a mock audio file
    audio_file = io.BytesIO(sample_audio_bytes)
    audio_file.name = "test_recording.wav"
    
    files = {
        "audio_file": ("test_recording.wav", audio_file, "audio/wav")
    }
    
    response = client.post("/transcribe_audio", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "text" in data
    assert len(data["text"]) > 0
    assert "confidence" in data
    assert 0 <= data["confidence"] <= 1


def test_transcribe_invalid_file_type():
    """Test transcription endpoint with invalid file type."""
    files = {
        "audio_file": ("test.txt", io.BytesIO(b"not an audio file"), "text/plain")
    }
    
    response = client.post("/transcribe_audio", files=files)
    
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]


@pytest.mark.asyncio
async def test_transcribe_and_compare_workflow(sample_audio_bytes):
    """Integration test: Transcribe audio then compare with verse."""
    # Step 1: Transcribe audio
    audio_file = io.BytesIO(sample_audio_bytes)
    files = {
        "audio_file": ("test_recording.wav", audio_file, "audio/wav")
    }
    
    transcribe_response = client.post("/transcribe_audio", files=files)
    assert transcribe_response.status_code == 200
    transcription_data = transcribe_response.json()
    recognized_text = transcription_data["text"]
    
    # Step 2: Compare with a verse
    verse_text = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
    payload = {
        "recognized_text": recognized_text,
        "verse_text": verse_text,
        "verse_reference": "1:1"
    }
    
    compare_response = client.post("/compare_verse", json=payload)
    assert compare_response.status_code == 200
    compare_data = compare_response.json()
    
    # Verify comparison results
    assert "match_percentage" in compare_data
    assert "word_comparisons" in compare_data
    assert "total_words" in compare_data
    assert "matched_words" in compare_data
    assert "mismatched_words" in compare_data
    
    # The match percentage should be between 0 and 100
    assert 0 <= compare_data["match_percentage"] <= 100
    
    # Verify word comparisons structure
    if compare_data["word_comparisons"]:
        first_word = compare_data["word_comparisons"][0]
        assert "position" in first_word
        assert "recognized" in first_word
        assert "verse" in first_word
        assert "match" in first_word
        assert isinstance(first_word["match"], bool)


def test_transcribe_with_real_file_simulation():
    """Simulate sending a real audio file format."""
    # Simulate a more realistic audio file
    # In production, you would load from app/tests/data/
    test_data_dir = Path(__file__).parent / "data"
    test_data_dir.mkdir(exist_ok=True)
    
    # Create a mock WAV file structure (simplified)
    # Real implementation would load actual audio from test_data_dir
    mock_wav_header = b'RIFF' + b'\x24\x08\x00\x00' + b'WAVE' + b'fmt ' + b'\x10\x00\x00\x00'
    mock_wav_data = mock_wav_header + b'\x00' * 1000
    
    files = {
        "audio_file": ("sample_recitation.wav", io.BytesIO(mock_wav_data), "audio/wav")
    }
    
    response = client.post("/transcribe_audio", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["text"], str)
    # The mock transcription service should return Arabic text
    assert len(data["text"]) > 0

