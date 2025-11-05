import os
from typing import Dict

# Try to import whisper, but make it optional
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    whisper = None

class TranscriptionService:
    """
    Service for transcribing audio to text.
    Can use OpenAI Whisper or mock implementation.
    """
    
    def __init__(self):
        self.use_whisper = os.getenv("USE_WHISPER", "false").lower() == "true"
        self.model = None
        
        if self.use_whisper and WHISPER_AVAILABLE:
            try:
                # Load Whisper model (base model for faster testing)
                self.model = whisper.load_model("base")
            except Exception as e:
                print(f"Warning: Could not load Whisper model: {e}")
                print("Falling back to mock transcription")
                self.use_whisper = False
        elif self.use_whisper and not WHISPER_AVAILABLE:
            print("Warning: Whisper is not available (not installed or incompatible)")
            print("Falling back to mock transcription")
            self.use_whisper = False
    
    async def transcribe(self, audio_bytes: bytes, filename: str = None) -> Dict:
        """
        Transcribe audio bytes to text.
        
        Args:
            audio_bytes: Audio file content as bytes
            filename: Optional filename for reference
            
        Returns:
            Dict with 'text' and optional 'confidence'
        """
        if self.use_whisper and self.model:
            return await self._transcribe_with_whisper(audio_bytes, filename)
        else:
            return await self._transcribe_mock(audio_bytes, filename)
    
    async def _transcribe_with_whisper(self, audio_bytes: bytes, filename: str) -> Dict:
        """Transcribe using OpenAI Whisper."""
        import tempfile
        import io
        
        # Save audio bytes to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name
        
        try:
            result = self.model.transcribe(tmp_path)
            return {
                "text": result["text"].strip(),
                "confidence": 0.95  # Whisper doesn't provide confidence, using placeholder
            }
        finally:
            os.unlink(tmp_path)
    
    async def _transcribe_mock(self, audio_bytes: bytes, filename: str) -> Dict:
        """
        Mock transcription for testing.
        Returns a sample Arabic text from Quran.
        NOTE: This is MOCK - it doesn't actually transcribe your audio!
        It just picks randomly from this list based on file hash.
        """
        # Extended sample verses from Quran for testing
        mock_texts = [
            # Al-Fatiha
            "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
            "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
            "الرَّحْمَٰنِ الرَّحِيمِ",
            "مَالِكِ يَوْمِ الدِّينِ",
            "إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ",
            "اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ",
            "صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ",
            # Al-Baqarah
            "الَّذِينَ آمَنُوا وَهُمْ لَا يُرَاءُونَ",
            "وَمَا تَفْقُدُ مِنْ شَيْءٍ إِلَّا وَهُوَ مَعَهُ",
            "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ",
            # Al-Ikhlas
            "قُلْ هُوَ اللَّهُ أَحَدٌ",
            "اللَّهُ الصَّمَدُ",
            "لَمْ يَلِدْ وَلَمْ يُولَدْ",
            "وَلَمْ يَكُن لَّهُ كُفُوًا أَحَدٌ",
            # Al-Falaq
            "قُلْ أَعُوذُ بِرَبِّ الْفَلَقِ",
            "مِن شَرِّ مَا خَلَقَ",
            # An-Nas
            "قُلْ أَعُوذُ بِرَبِّ النَّاسِ",
            "مَلِكِ النَّاسِ",
            "إِلَٰهِ النَّاسِ",
            # Common phrases
            "سُبْحَانَ اللَّهِ",
            "اللَّهُ أَكْبَرُ",
            "لَا إِلَٰهَ إِلَّا اللَّهُ",
            "مُحَمَّدٌ رَسُولُ اللَّهِ",
        ]
        
        # Simple hash-based selection for variety
        import hashlib
        hash_val = int(hashlib.md5(audio_bytes[:100] if len(audio_bytes) >= 100 else audio_bytes).hexdigest(), 16)
        selected_text = mock_texts[hash_val % len(mock_texts)]
        
        return {
            "text": selected_text,
            "confidence": 0.85
        }

