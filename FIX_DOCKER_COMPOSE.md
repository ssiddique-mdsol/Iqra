# Fix: docker-compose command not found

## ✅ Issue Fixed!

`docker-compose` has been installed via Homebrew and added to your PATH.

## Current Status

- ✅ **docker-compose installed:** v2.40.3
- ✅ **PATH configured:** `/opt/homebrew/bin/docker-compose`
- ⚠️ **Docker Desktop required:** docker-compose needs Docker daemon to run

## Important Note

Even though `docker-compose` is installed, it **requires Docker Desktop** to actually work. The `docker-compose` command is just a tool that communicates with Docker.

## Options

### Option 1: Use Without Docker (Recommended for Now)

Run the app without Docker using the provided script:

```bash
cd ~/code/iqra
./run-without-docker.sh
```

This will:
- Start the backend on port 8000
- Start the frontend with Expo
- Show you the QR code

### Option 2: Install Docker Desktop

To use `docker-compose up`, you need Docker Desktop:

1. **Download Docker Desktop:**
   ```bash
   open https://www.docker.com/products/docker-desktop/
   ```

2. **Install and launch Docker Desktop**

3. **Verify:**
   ```bash
   docker --version
   docker-compose --version
   ```

4. **Then run:**
   ```bash
   cd ~/code/iqra
   docker-compose up
   ```

### Option 3: Manual Start (Two Terminals)

**Terminal 1 - Backend:**
```bash
cd ~/code/iqra/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd ~/code/iqra/frontend
npm install
npm start
```

## Verify Installation

```bash
# Check docker-compose is available
docker-compose --version
# Should show: Docker Compose version 2.40.3

# Check it's in PATH
which docker-compose
# Should show: /opt/homebrew/bin/docker-compose
```

## Quick Start

**Easiest way (no Docker needed):**
```bash
cd ~/code/iqra
./run-without-docker.sh
```

This script handles everything automatically!

## Troubleshooting

**If docker-compose still not found:**
```bash
# Reload shell configuration
source ~/.zshrc

# Or restart your terminal
```

**If you get "Cannot connect to Docker daemon":**
- Docker Desktop is not running
- Install and launch Docker Desktop first
- Or use `./run-without-docker.sh` instead

