import pytest

# Pytest configuration and fixtures

@pytest.fixture
def sample_audio_bytes():
    """Fixture providing sample audio bytes for testing."""
    return b"fake audio content for testing purposes"

@pytest.fixture
def sample_verse():
    """Fixture providing sample Quran verse for testing."""
    return "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"

