# Iqra - Quran Recitation App

A full-stack AI mobile application for Quran recitation practice, similar to Tarteel.ai. The app allows users to record their recitation, transcribe it using AI, and compare it with Quran verses word-by-word.

## Project Structure

```
iqra/
├── backend/          # FastAPI backend service
│   ├── app/
│   │   ├── main.py           # FastAPI application entry point
│   │   ├── routes/           # API route handlers
│   │   ├── services/         # Business logic services
│   │   └── tests/            # Test files
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/         # React Native (Expo) mobile app
│   ├── src/
│   │   ├── screens/          # App screens
│   │   ├── services/         # API service layer
│   │   └── __tests__/        # Test files
│   ├── package.json
│   └── .env
│
└── docker-compose.yml # Docker orchestration
```

## Prerequisites

- **macOS** (this setup is optimized for macOS)
- **Python 3.10+** (`brew install python@3.10`)
- **Node.js 18+** (`brew install node`)
- **Docker & Docker Compose** (`brew install docker docker-compose`)

## Quick Start with Docker

The easiest way to get started is using Docker Compose:

```bash
# Clone and navigate to project
cd ~/code/iqra

# Start both backend and frontend services
docker-compose up

# Backend will be available at http://localhost:8000
# Frontend Expo will start and show QR code in terminal
```

## Manual Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd ~/code/iqra/backend
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env if needed (optional: set USE_WHISPER=true to use OpenAI Whisper)
   ```

5. **Run the backend server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   The API will be available at `http://localhost:8000`
   - API docs: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/health`

6. **Run backend tests:**
   ```bash
   pytest
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd ~/code/iqra/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   # .env file should already exist with API_BASE_URL=http://localhost:8000
   ```

4. **Start the Expo development server:**
   ```bash
   npm start
   # or
   expo start
   ```

   This will:
   - Start Metro bundler
   - Show QR code to scan with Expo Go app (iOS/Android)
   - Optionally open iOS simulator: `npm run ios`
   - Optionally open Android emulator: `npm run android`

5. **Run frontend tests:**
   ```bash
   npm test
   ```

## API Endpoints

### POST `/transcribe_audio`
Transcribe audio file to text.

**Request:**
- `audio_file` (multipart/form-data): Audio file to transcribe

**Response:**
```json
{
  "success": true,
  "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
  "confidence": 0.85
}
```

### POST `/compare_verse`
Compare recognized text with Quran verse.

**Request:**
```json
{
  "recognized_text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
  "verse_text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
  "verse_reference": "1:1"
}
```

**Response:**
```json
{
  "success": true,
  "match_percentage": 100.0,
  "word_comparisons": [
    {
      "position": 0,
      "recognized": "بِسْمِ",
      "verse": "بِسْمِ",
      "match": true
    }
  ],
  "total_words": 4,
  "matched_words": 4,
  "mismatched_words": 0
}
```

## Testing

### Backend Tests

```bash
cd ~/code/iqra/backend
pytest                    # Run all tests
pytest -v                # Verbose output
pytest app/tests/test_transcription_service.py  # Run specific test file
```

### Frontend Tests

```bash
cd ~/code/iqra/frontend
npm test                  # Run all tests
npm test -- --watch       # Watch mode
```

## Development Workflow

1. **Start backend:**
   ```bash
   cd ~/code/iqra/backend
   source venv/bin/activate
   uvicorn app.main:app --reload --port 8000
   ```

2. **Start frontend (in another terminal):**
   ```bash
   cd ~/code/iqra/frontend
   npm start
   ```

3. **Access:**
   - Backend API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Frontend: Scan QR code with Expo Go app

## Docker Development

### Build and run with Docker Compose

```bash
docker-compose up --build
```

### Run individual services

**Backend only:**
```bash
cd ~/code/iqra/backend
docker build -t iqra-backend .
docker run -p 8000:8000 iqra-backend
```

**Frontend only:**
```bash
cd ~/code/iqra/frontend
docker build -t iqra-frontend .
docker run -p 19000:19000 iqra-frontend
```

## Configuration

### Backend Configuration

Edit `backend/.env`:
- `USE_WHISPER=false` - Set to `true` to use OpenAI Whisper (requires model download on first use)

### Frontend Configuration

Edit `frontend/.env`:
- `API_BASE_URL=http://localhost:8000` - Backend API URL

For physical device testing, update `API_BASE_URL` to your Mac's local IP:
- `API_BASE_URL=http://192.168.1.X:8000` (replace X with your Mac's IP)

## Project Features

✅ **Backend:**
- FastAPI REST API
- Audio transcription (mock + optional Whisper support)
- Word-by-word verse comparison
- Comprehensive unit and integration tests
- Docker support

✅ **Frontend:**
- React Native with Expo
- Audio recording interface
- Real-time transcription
- Visual word-by-word comparison
- Jest + React Testing Library tests

## Troubleshooting

### Backend Issues

- **Port 8000 already in use:** Change port in `uvicorn` command or kill existing process
- **Whisper model download slow:** First-time Whisper use downloads model (~500MB). Use mock mode by default.

### Frontend Issues

- **Expo Go not connecting:** Ensure backend is running and `API_BASE_URL` is correct
- **Audio recording permissions:** Grant microphone permissions when prompted
- **Module not found:** Run `npm install` again

### Docker Issues

- **Port conflicts:** Ensure ports 8000 and 19000 are available
- **Build fails:** Check Docker is running and has sufficient resources

## Next Steps

- [ ] Integrate real OpenAI Whisper API or local model
- [ ] Add verse database/API integration
- [ ] Implement user authentication
- [ ] Add progress tracking and statistics
- [ ] Improve Arabic text handling and normalization
- [ ] Add offline mode support

## License

MIT
