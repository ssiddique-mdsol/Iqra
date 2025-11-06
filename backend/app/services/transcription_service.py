import os
from typing import Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
        # HARDCODED FOR TESTING - force Whisper to be used
        self.use_whisper = True  # HARDCODED: os.getenv("USE_WHISPER", "false").lower() == "true"
        self.add_tajweed = os.getenv("ADD_TAJWEED", "true").lower() == "true"
        print(f"[TranscriptionService.__init__] HARDCODED use_whisper=True")
        self.model = None
        self.tajweed_service = TajweedService()
        
        if self.use_whisper and WHISPER_AVAILABLE:
            try:
                # Load Whisper model - using "small" for better balance
                # Options: tiny, base, small, medium, large
                # Start with "small" - can upgrade to "medium" later if needed
                model_name = os.getenv("WHISPER_MODEL", "small")  # Allow override via env
                print(f"[Whisper] ========================================")
                print(f"[Whisper] Attempting to load Whisper model: {model_name}")
                print(f"[Whisper] USE_WHISPER env: {os.getenv('USE_WHISPER', 'NOT SET')}")
                try:
                    self.model = whisper.load_model(model_name)
                    print(f"[Whisper] ✅ Model '{model_name}' loaded successfully!")
                    print(f"[Whisper] ========================================")
                except Exception as load_error:
                    print(f"[Whisper] ❌ ERROR loading model '{model_name}': {load_error}")
                    print(f"[Whisper] Trying 'small' model as fallback...")
                    try:
                        self.model = whisper.load_model("small")
                        print(f"[Whisper] ✅ Fallback to 'small' model successful!")
                        print(f"[Whisper] ========================================")
                    except Exception as fallback_error:
                        print(f"[Whisper] ❌ Fallback also failed: {fallback_error}")
                        print(f"[Whisper] Falling back to mock transcription")
                        print(f"[Whisper] ========================================")
                        raise load_error
            except Exception as e:
                print(f"[Whisper] ❌ CRITICAL: Could not load Whisper model: {e}")
                print(f"[Whisper] Error type: {type(e).__name__}")
                import traceback
                traceback.print_exc()
                print("[Whisper] Falling back to mock transcription")
                self.use_whisper = False
                self.model = None
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
        print(f"[TranscriptionService] ========================================")
        print(f"[TranscriptionService] use_whisper={self.use_whisper}, model={self.model is not None}")
        if self.use_whisper and self.model:
            print("[TranscriptionService] ✅ Using Whisper for transcription")
            result = await self._transcribe_with_whisper(audio_bytes, filename)
        else:
            print("[TranscriptionService] ⚠️  Using MOCK transcription (Whisper not available)")
            if not self.use_whisper:
                print("[TranscriptionService] Reason: use_whisper is False")
            if not self.model:
                print("[TranscriptionService] Reason: model is None")
            result = await self._transcribe_mock(audio_bytes, filename)
        print(f"[TranscriptionService] ========================================")
        
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
        
        # Determine file extension from filename or content
        file_ext = ".wav"
        if filename:
            if filename.endswith('.m4a'):
                file_ext = ".m4a"
            elif filename.endswith('.mp3'):
                file_ext = ".mp3"
            elif filename.endswith('.wav'):
                file_ext = ".wav"
        
        # If no extension, try to detect from content
        if not filename or '.' not in filename:
            # Check for common audio file signatures
            if audio_bytes[:4] == b'ftyp' or (len(audio_bytes) > 4 and audio_bytes[4:8] == b'ftyp'):
                file_ext = ".m4a"  # MP4/M4A container
                print(f"[Whisper] Detected M4A format from content")
            elif audio_bytes[:4] == b'RIFF':
                file_ext = ".wav"
                print(f"[Whisper] Detected WAV format from content")
            elif audio_bytes[:3] == b'ID3' or (len(audio_bytes) > 1 and audio_bytes[:2] == b'\xff\xfb'):
                file_ext = ".mp3"
                print(f"[Whisper] Detected MP3 format from content")
        
        print(f"[Whisper] Using file extension: {file_ext}")
        
        # Save audio bytes to temporary file with correct extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name
            print(f"[Whisper] Wrote {len(audio_bytes)} bytes to {tmp_path}")
        
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
            # Use temperature=0 for more deterministic results
            # Use beam_size=5 for better accuracy (default is 5)
            # Use condition_on_previous_text=True for better context
            result = self.model.transcribe(
                tmp_path, 
                language="ar",  # Arabic language
                task="transcribe",  # Transcribe, not translate
                fp16=False,  # Use float32 for better compatibility
                verbose=True,  # More verbose for debugging
                temperature=0.0,  # More deterministic (less random)
                beam_size=5,  # Beam search for better accuracy
                best_of=5,  # Try multiple decodings, pick best
                condition_on_previous_text=True,  # Use previous text for context
                initial_prompt="بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ الرَّحْمَٰنِ الرَّحِيمِ مَالِكِ يَوْمِ الدِّينِ"  # Longer prompt with more Arabic context
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

