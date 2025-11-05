# Test Data

This directory contains test audio files and verse samples for testing.

## Audio Files

Place test audio files here (e.g., `test_verse.wav`, `sample_recitation.m4a`).

## Verse Samples

Example verse text for testing:
- **Al-Fatiha 1:1:** `بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ`
- **Al-Fatiha 1:2:** `الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ`
- **Al-Fatiha 1:3:** `الرَّحْمَٰنِ الرَّحِيمِ`

## Usage in Tests

```python
from pathlib import Path

TEST_DATA_DIR = Path(__file__).parent / "data"
audio_file = TEST_DATA_DIR / "test_audio.wav"
```

