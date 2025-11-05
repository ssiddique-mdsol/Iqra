# Docker Installation Guide

Docker Desktop installation requires administrator privileges. Here's how to complete the installation:

## Option 1: Install Docker Desktop Manually (Recommended)

1. **Open Docker Desktop installer:**
   ```bash
   open /opt/homebrew/Caskroom/docker-desktop
   ```
   Or download directly from: https://www.docker.com/products/docker-desktop/

2. **Double-click the Docker.dmg file** in the Caskroom directory

3. **Drag Docker.app to Applications folder**

4. **Launch Docker Desktop** from Applications:
   - Open Finder → Applications → Docker
   - Or run: `open -a Docker`

5. **Start Docker Desktop** (it will appear in your menu bar)

6. **Verify installation:**
   ```bash
   docker --version
   docker-compose --version
   ```

## Option 2: Install via Command Line (Requires Sudo)

If you prefer command line, you can run:

```bash
brew install --cask docker
```

When prompted, enter your administrator password.

## After Installation

1. **Start Docker Desktop** - The Docker whale icon should appear in your menu bar

2. **Verify Docker is running:**
   ```bash
   docker ps
   ```

3. **Test Docker:**
   ```bash
   docker run hello-world
   ```

## Add Docker to PATH (if needed)

If `docker` command is not found after installation, add to your `~/.zshrc`:

```bash
# Docker paths (usually not needed as Docker Desktop handles this)
# But if docker command is not found, uncomment:
# export PATH="/usr/local/bin:$PATH"
```

Most of the time, Docker Desktop automatically configures paths when you launch it.

## Troubleshooting

**Docker Desktop won't start:**
- Check System Settings → Privacy & Security → Allow Docker Desktop
- Restart your Mac if needed

**Docker command not found:**
- Make sure Docker Desktop is running
- Check if `/usr/local/bin/docker` exists
- Restart your terminal

**Permission denied:**
- Docker Desktop needs to be running first
- Make sure you're in the `docker` group (usually automatic on macOS)

## Quick Test

Once Docker is installed and running:

```bash
cd ~/code/iqra
docker-compose up
```

This should start both backend and frontend services.

