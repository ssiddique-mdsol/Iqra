# Web Frontend for Iqra

This is a simple HTML/JavaScript web interface that works with the Iqra backend API.

## How to Use

1. **Make sure the backend is running:**
   ```bash
   cd ~/code/iqra/backend
   source venv/bin/activate
   uvicorn app.main:app --reload --port 8000
   ```

2. **Open the web interface:**
   - Simply open `index.html` in your browser
   - Or use a simple HTTP server:
     ```bash
     cd ~/code/iqra/frontend/web
     python3 -m http.server 3000
     ```
     Then open: http://localhost:3000

3. **Use the app:**
   - Click "Start Recording" to record audio
   - Click "Stop Recording" when done
   - The text will be transcribed automatically
   - Enter a verse text and click "Compare" to see word-by-word comparison

## Features

- ✅ Audio recording (uses browser MediaRecorder API)
- ✅ Audio transcription via backend API
- ✅ Verse comparison with word-by-word highlighting
- ✅ Visual match/mismatch indicators
- ✅ Statistics display (match percentage, word counts)

## Note

This is a simplified web version. For the full mobile experience with React Native, use the Expo Go app on your phone.

