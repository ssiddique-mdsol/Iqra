#!/bin/bash

# Iqra Local Setup Script
# This script helps set up the backend and frontend for local development

set -e

echo "🚀 Iqra Local Setup"
echo "==================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Install with: brew install python@3.10"
    exit 1
else
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python: $PYTHON_VERSION"
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Install with: brew install node"
    exit 1
else
    NODE_VERSION=$(node --version)
    echo "✅ Node.js: $NODE_VERSION"
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed."
    exit 1
else
    NPM_VERSION=$(npm --version)
    echo "✅ npm: $NPM_VERSION"
fi

echo ""
echo "═══════════════════════════════════════════════"
echo ""

# Setup Backend
echo -e "${BLUE}📦 Setting up Backend...${NC}"
echo ""

cd "$(dirname "$0")/backend"

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

echo -e "${GREEN}✅ Backend setup complete!${NC}"
echo ""

# Setup Frontend
echo -e "${BLUE}📦 Setting up Frontend...${NC}"
echo ""

cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
else
    echo "Node modules already installed. Run 'npm install' manually to update."
fi

if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    echo "API_BASE_URL=http://localhost:8000" > .env
fi

echo -e "${GREEN}✅ Frontend setup complete!${NC}"
echo ""

# Summary
echo "═══════════════════════════════════════════════"
echo ""
echo -e "${GREEN}✨ Setup Complete!${NC}"
echo ""
echo "To run the app:"
echo ""
echo -e "${YELLOW}Backend (Terminal 1):${NC}"
echo "  cd ~/code/iqra/backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --port 8000"
echo ""
echo -e "${YELLOW}Frontend (Terminal 2):${NC}"
echo "  cd ~/code/iqra/frontend"
echo "  npm start"
echo ""
echo "Or use Docker:"
echo "  cd ~/code/iqra"
echo "  docker-compose up"
echo ""

