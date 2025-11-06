import os
from typing import Dict

# Try to import whisper, but make it optional
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    whisper = None

# Import tajweed service
from app.services.tajweed_service import TajweedService

class TranscriptionService:
    """
    Service for transcribing audio to text.
    Can use OpenAI Whisper or mock implementation.
    """
    
    def __init__(self):
        self.use_whisper = os.getenv("USE_WHISPER", "false").lower() == "true"
        self.add_tajweed = os.getenv("ADD_TAJWEED", "true").lower() == "true"
        self.model = None
        self.tajweed_service = TajweedService()
        
        if self.use_whisper and WHISPER_AVAILABLE:
            try:
                # Load Whisper model - using "small" for better Arabic accuracy
                # Options: tiny, base, small, medium, large
                # "small" is a good balance of accuracy and speed
                print("[Whisper] Loading Whisper model: small")
                self.model = whisper.load_model("small")
                print("[Whisper] Model loaded successfully")
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
            result = await self._transcribe_with_whisper(audio_bytes, filename)
        else:
            result = await self._transcribe_mock(audio_bytes, filename)
        
        # Add tajweed if enabled
        if self.add_tajweed and result.get("text"):
            original_text = result["text"]
            tajweed_text = self.tajweed_service.add_tajweed(original_text)
            result["text"] = tajweed_text
            result["original_text"] = original_text  # Keep original for reference
        
        return result
    
    async def _transcribe_with_whisper(self, audio_bytes: bytes, filename: str) -> Dict:
        """Transcribe using OpenAI Whisper."""
        import tempfile
        
        # Determine file extension from filename or default to .wav
        file_ext = ".wav"
        if filename:
            if filename.endswith('.m4a'):
                file_ext = ".m4a"
            elif filename.endswith('.mp3'):
                file_ext = ".mp3"
            elif filename.endswith('.wav'):
                file_ext = ".wav"
        
        # Save audio bytes to temporary file with correct extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name
        
        try:
            print(f"[Whisper] ========================================")
            print(f"[Whisper] Starting transcription...")
            print(f"[Whisper] Audio file: {filename}")
            print(f"[Whisper] Audio size: {len(audio_bytes)} bytes")
            print(f"[Whisper] Temp file: {tmp_path}")
            
            # Whisper can handle various audio formats including m4a
            # Use task="transcribe" to ensure it transcribes (not translates)
            # Use language="ar" for Arabic
            # Use fp16=False for better compatibility
            # Use initial_prompt to help with Arabic recognition
            result = self.model.transcribe(
                tmp_path, 
                language="ar",  # Arabic language
                task="transcribe",  # Transcribe, not translate
                fp16=False,  # Use float32 for better compatibility
                verbose=True,  # More verbose for debugging
                initial_prompt="بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"  # Help Whisper recognize Arabic
            )
            transcribed_text = result["text"].strip()
            
            # Log for debugging
            print(f"[Whisper] ========================================")
            print(f"[Whisper] Transcription result: {transcribed_text}")
            print(f"[Whisper] Detected language: {result.get('language', 'unknown')}")
            print(f"[Whisper] Language probability: {result.get('language_probability', 'N/A')}")
            print(f"[Whisper] ========================================")
            
            # If transcription is empty or seems wrong, log warning
            if not transcribed_text or len(transcribed_text) < 2:
                print(f"[Whisper] ⚠️  WARNING: Transcription seems empty or too short")
                print(f"[Whisper] This might indicate audio quality issues")
            
            return {
                "text": transcribed_text,
                "confidence": 0.95  # Whisper doesn't provide confidence, using placeholder
            }
        except Exception as e:
            print(f"[Whisper] ERROR: Transcription failed: {e}")
            import traceback
            traceback.print_exc()
            # Fall back to mock if Whisper fails
            print(f"[Whisper] Falling back to mock transcription")
            return await self._transcribe_mock(audio_bytes, filename)
        finally:
            if os.path.exists(tmp_path):
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

