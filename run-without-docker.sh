#!/bin/bash

# Run Iqra app without Docker
# This script starts both backend and frontend manually

# Don't exit on error, handle them gracefully
set +e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Iqra App (Without Docker)${NC}"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping services...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit
}

trap cleanup SIGINT SIGTERM

# Start Backend
echo -e "${BLUE}📦 Starting Backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

if [ ! -f ".env" ]; then
    cp .env.example .env 2>/dev/null || echo "USE_WHISPER=false" > .env
fi

echo "Installing/updating dependencies..."
pip install --upgrade pip setuptools wheel
echo "Installing Python packages (this may take a minute)..."
if ! pip install -r requirements.txt; then
    echo -e "${YELLOW}⚠️  Some dependencies failed to install, continuing anyway...${NC}"
    echo "Note: Whisper is optional and will use mock mode if not available"
fi

echo "Starting FastAPI server on http://localhost:8000"
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"
echo ""

# Wait a moment for backend to start
sleep 3

# Start Frontend
echo -e "${BLUE}📱 Starting Frontend...${NC}"
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

if [ ! -f ".env" ]; then
    echo "API_BASE_URL=http://localhost:8000" > .env
fi

echo "Starting Expo development server..."
npm start &
FRONTEND_PID=$!

echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"
echo ""

echo "═══════════════════════════════════════════════════════"
echo -e "${GREEN}✨ Iqra App is running!${NC}"
echo ""
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Frontend: Check terminal for QR code"
echo ""
echo "Press Ctrl+C to stop all services"
echo "═══════════════════════════════════════════════════════"

# Wait for both processes
wait

