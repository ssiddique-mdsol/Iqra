# How to Run Iqra Locally

## Quick Setup Guide

### Prerequisites Check
First, verify you have the required tools:
```bash
python3 --version  # Should be 3.10+
node --version     # Should be 18+
docker --version   # Optional, for Docker setup
```

---

## Option 1: Docker Compose (Recommended - Easiest)

### Step 1: Start Both Services
```bash
cd ~/code/iqra
docker-compose up
```

This will:
- ✅ Build and start the FastAPI backend on `http://localhost:8000`
- ✅ Build and start the Expo frontend
- ✅ Show QR code to scan with Expo Go app

### Step 2: Access the App
- **Backend API:** Open `http://localhost:8000/docs` in your browser
- **Frontend:** Scan the QR code with Expo Go app (iOS/Android)

### Step 3: Stop Services
Press `Ctrl+C` in the terminal

---

## Option 2: Manual Setup (For Development)

### Part A: Backend Setup

#### 1. Navigate to backend
```bash
cd ~/code/iqra/backend
```

#### 2. Create Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set up environment (optional)
```bash
cp .env.example .env
# Edit .env if you want to enable Whisper (USE_WHISPER=true)
```

#### 5. Start the backend server
```bash
uvicorn app.main:app --reload --port 8000
```

✅ **Backend is now running!**
- API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

#### 6. Test the backend (in another terminal)
```bash
cd ~/code/iqra/backend
source venv/bin/activate
pytest
```

---

### Part B: Frontend Setup

#### 1. Open a NEW terminal window/tab

#### 2. Navigate to frontend
```bash
cd ~/code/iqra/frontend
```

#### 3. Install dependencies
```bash
npm install
```

#### 4. Verify environment configuration
```bash
cat .env
# Should show: API_BASE_URL=http://localhost:8000
```

#### 5. Start Expo development server
```bash
npm start
# or
expo start
```

#### 6. Access the app
You'll see options:
- **Press `i`** - Open iOS Simulator (requires Xcode)
- **Press `a`** - Open Android Emulator (requires Android Studio)
- **Scan QR code** - Use Expo Go app on your phone
  - iOS: Camera app → Scan QR code
  - Android: Expo Go app → Scan QR code

✅ **Frontend is now running!**

---

## Testing the Full Flow

### 1. Test Backend API

Open another terminal and test the endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Test transcription (requires an audio file)
curl -X POST http://localhost:8000/transcribe_audio \
  -F "audio_file=@path/to/your/audio.wav"

# Test comparison
curl -X POST http://localhost:8000/compare_verse \
  -H "Content-Type: application/json" \
  -d '{
    "recognized_text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
    "verse_text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
    "verse_reference": "1:1"
  }'
```

### 2. Test Frontend App

1. Open the app on your phone/simulator
2. Tap "Start Recording"
3. Record some audio
4. Tap "Stop Recording"
5. Wait for transcription
6. View comparison results

---

## Common Issues & Solutions

### Backend Issues

**Port 8000 already in use:**
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

**Python dependencies not installing:**
```bash
# Upgrade pip first
pip install --upgrade pip
pip install -r requirements.txt
```

**Module not found errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Issues

**npm install fails:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Expo Go can't connect to backend:**
- Make sure backend is running on port 8000
- For physical device, update `.env` with your Mac's local IP:
  ```bash
  # Find your Mac's IP
  ifconfig | grep "inet " | grep -v 127.0.0.1
  
  # Update frontend/.env
  API_BASE_URL=http://YOUR_MAC_IP:8000
  ```

**Audio recording permissions:**
- Grant microphone permissions when prompted in the app

---

## Development Workflow

1. **Terminal 1 - Backend:**
   ```bash
   cd ~/code/iqra/backend
   source venv/bin/activate
   uvicorn app.main:app --reload --port 8000
   ```

2. **Terminal 2 - Frontend:**
   ```bash
   cd ~/code/iqra/frontend
   npm start
   ```

3. **Terminal 3 - Running Tests:**
   ```bash
   # Backend tests
   cd ~/code/iqra/backend
   source venv/bin/activate
   pytest
   
   # Frontend tests
   cd ~/code/iqra/frontend
   npm test
   ```

---

## Quick Command Reference

```bash
# Backend
cd ~/code/iqra/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Frontend
cd ~/code/iqra/frontend
npm start

# Tests
cd ~/code/iqra/backend && source venv/bin/activate && pytest
cd ~/code/iqra/frontend && npm test

# Docker
cd ~/code/iqra
docker-compose up
```

---

## Need Help?

- Check API docs: `http://localhost:8000/docs`
- Check backend health: `http://localhost:8000/health`
- View logs in terminal for errors
- Make sure both services are running before testing

