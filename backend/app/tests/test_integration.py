import pytest
import httpx
from fastapi.testclient import TestClient
from app.main import app
import os

# Test client
client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_endpoint():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_transcribe_audio_endpoint():
    """Test transcribe audio endpoint with mock audio file."""
    # Create a dummy audio file
    audio_content = b"fake audio content for testing"
    
    files = {
        "audio_file": ("test_audio.wav", audio_content, "audio/wav")
    }
    
    response = client.post("/transcribe_audio", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "text" in data
    assert "confidence" in data

def test_compare_verse_endpoint():
    """Test compare verse endpoint."""
    payload = {
        "recognized_text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "verse_text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "verse_reference": "1:1"
    }
    
    response = client.post("/compare_verse", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "match_percentage" in data
    assert "word_comparisons" in data
    assert "total_words" in data

@pytest.mark.asyncio
async def test_full_workflow():
    """Integration test: transcribe audio then compare with verse."""
    # Step 1: Transcribe audio
    audio_content = b"fake audio content"
    files = {
        "audio_file": ("test_audio.wav", audio_content, "audio/wav")
    }
    
    transcribe_response = client.post("/transcribe_audio", files=files)
    assert transcribe_response.status_code == 200
    transcription_data = transcribe_response.json()
    recognized_text = transcription_data["text"]
    
    # Step 2: Compare with verse
    payload = {
        "recognized_text": recognized_text,
        "verse_text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "verse_reference": "1:1"
    }
    
    compare_response = client.post("/compare_verse", json=payload)
    assert compare_response.status_code == 200
    compare_data = compare_response.json()
    assert "match_percentage" in compare_data

