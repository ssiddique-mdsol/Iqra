# Transcription Service Information

## Current Status: Mock Mode (Limited Database)

The backend is currently using **mock transcription** which only returns one of **3 predefined phrases**:

1. `بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ` (Bismillah)
2. `الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ` (Alhamdulillah)
3. `الرَّحْمَٰنِ الرَّحِيمِ` (Ar-Rahman)

**This is why it's not recognizing what you're actually recording!** It just picks one of these 3 phrases randomly based on the audio file hash.

## Options to Get Real Transcription

### Option 1: Enable Whisper (Recommended for Real Transcription)

Whisper is OpenAI's speech recognition model that can transcribe actual audio.

**Steps:**

1. **Install Whisper dependencies:**
   ```bash
   cd ~/code/iqra/backend
   source venv/bin/activate
   pip install openai-whisper torch
   ```

2. **Enable Whisper in backend:**
   ```bash
   # Edit .env file
   echo "USE_WHISPER=true" > ~/code/iqra/backend/.env
   ```

3. **Restart the backend:**
   ```bash
   # Stop current backend (Ctrl+C)
   # Then restart:
   uvicorn app.main:app --reload --port 8000
   ```

**Note:** First time using Whisper will download the model (~500MB) which may take a few minutes.

### Option 2: Add More Mock Phrases (For Testing)

If you want to test with more variety without installing Whisper, we can add more phrases to the mock database.

### Option 3: Use External Speech Recognition API

You could integrate with:
- Google Cloud Speech-to-Text
- Azure Speech Services
- AWS Transcribe
- AssemblyAI

## Current Limitations

- ✅ **Mock mode:** Fast, no dependencies, but limited to 3 phrases
- ⚠️ **No real transcription:** Doesn't actually recognize what you say
- ⚠️ **Random selection:** Picks phrase based on file hash, not content

## Recommendation

For a real Quran recitation app, you should:
1. Enable Whisper for local transcription (free, works offline)
2. Or use a cloud API for better Arabic recognition
3. Or use a specialized Arabic speech recognition service

Would you like me to:
- Enable Whisper for real transcription?
- Add more mock phrases for testing?
- Set up a cloud speech recognition API?

