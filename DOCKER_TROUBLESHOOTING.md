# Docker Build Troubleshooting - Fix Common Issues

Having trouble with `docker build`? This guide covers the most common problems.

---

## 🔴 Error: "docker build requires 1 argument"

### Symptom
```bash
$ docker build -t rag-system:latest
Error: "docker build" requires 1 argument
```

### Cause
Missing the context directory (usually `.` for current directory)

### Fix - Add the dot (.)

```bash
# ❌ WRONG
docker build -t rag-system:latest

# ✅ CORRECT
docker build -t rag-system:latest .
```

The `.` at the end means "use current directory as build context"

### Full Command
```bash
docker build -t rag-system:latest .
```

---

## 🔴 Error: "Cannot connect to Docker daemon"

### Symptom
```
ERROR: Cannot connect to the Docker daemon at unix:///var/run/docker.sock.
Is the docker daemon running?
```

### Cause
Docker service is not running

### Fix - Start Docker

#### macOS
```bash
# Open Docker Desktop application
# Or use:
open /Applications/Docker.app

# Wait 30 seconds for Docker to start
sleep 30

# Verify it started
docker ps
```

#### Linux
```bash
# Start Docker service
sudo systemctl start docker

# Verify it started
docker ps
```

#### Windows
```bash
# Open Docker Desktop from Start Menu
# Or use PowerShell:
Start-Process "Docker"

# Wait 30 seconds
Start-Sleep -Seconds 30

# Verify it started
docker ps
```

### Then Try Build Again
```bash
docker build -t rag-system:latest .
```

---

## 🔴 Error: "Cannot find Dockerfile"

### Symptom
```
ERROR: unable to prepare context: unable to evaluate symlinks in Dockerfile path:
lstat /path/to/Dockerfile: no such file or directory
```

### Cause
Not in the correct directory (where Dockerfile is located)

### Fix - Navigate to Repository Root

```bash
# First, find where Dockerfile is
find . -name Dockerfile

# Navigate there
cd /path/to/clrag  # Replace with actual path

# Verify Dockerfile exists
ls -la Dockerfile

# Now build
docker build -t rag-system:latest .
```

### Check Current Location
```bash
# Show current directory
pwd

# List files in current directory
ls

# Should see: Dockerfile, requirements.txt, src/, etc.
```

---

## 🔴 Error: "buildx: Docker engine not available"

### Symptom
```
ERROR: buildx: Docker engine not available
```

### Cause
Docker buildx is enabled but Docker daemon isn't running, OR you have a shell alias/function

### Fix Option 1: Check for Alias

```bash
# Check if docker is aliased
alias docker

# If you see an alias, unalias it temporarily
unalias docker

# Then try:
docker build -t rag-system:latest .
```

### Fix Option 2: Disable buildx

```bash
# Check docker version
docker version

# Use plain docker build
docker build --progress=plain -t rag-system:latest .
```

### Fix Option 3: Start Docker First

```bash
# macOS - Start Docker
open /Applications/Docker.app
sleep 30

# Then build
docker build -t rag-system:latest .
```

---

## 🔴 Error: "permission denied while trying to connect"

### Symptom
```
ERROR: permission denied while trying to connect to the Docker daemon socket
at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/":
dial unix /var/run/docker.sock: permission denied
```

### Cause
User not in docker group (Linux only)

### Fix - Add User to Docker Group

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply group changes (choose one)
newgrp docker           # Start new session
# OR
exec bash               # Restart bash
# OR log out and log back in

# Verify it works
docker ps
```

### Temporary Workaround
```bash
# Use sudo for this command only
sudo docker build -t rag-system:latest .
```

---

## 🟡 Error: "Build context too large"

### Symptom
```
ERROR: build context is too large, ...
Sending build context to Docker daemon...
```

### Cause
Sending too many files to Docker (git history, cache, venv, etc.)

### Fix - Create .dockerignore

```bash
# Create .dockerignore file
cat > .dockerignore <<EOF
.git
.gitignore
__pycache__
.pytest_cache
.venv
venv
env
*.pyc
*.pyo
.DS_Store
.env
logs/
data/
*.log
.vscode
.idea
EOF

# Now rebuild
docker build -t rag-system:latest .
```

---

## 🟡 Error: "Step X/Y failed"

### Symptom
```
Step 5/8 : RUN pip install -r requirements.txt
...
ERROR: could not install packages due to an error ...
```

### Common Causes & Fixes

#### Missing Dependencies
```bash
# Rebuild with more verbose output
docker build --progress=plain -t rag-system:latest .

# Or check requirements.txt is in repo root
ls -la requirements.txt
```

#### Network Issues
```bash
# Try building again (temporary network issue)
docker build -t rag-system:latest .

# If persistent, check internet connection
ping 8.8.8.8
```

#### Out of Disk Space
```bash
# Check disk space
df -h

# Clean Docker
docker system prune -a

# Try again
docker build -t rag-system:latest .
```

---

## 🟡 Error: "Tag is invalid"

### Symptom
```
Error response from daemon: invalid reference format
```

### Cause
Invalid tag name (special characters, uppercase, etc.)

### Fix - Use Lowercase

```bash
# ❌ WRONG (uppercase, special chars)
docker build -t RAG-SYSTEM:latest .
docker build -t "Rag System":latest .

# ✅ CORRECT (lowercase, no spaces)
docker build -t rag-system:latest .
docker build -t my-rag-system:v1.0 .
```

---

## ✅ Verification Steps

### Step 1: Verify Docker is Running

```bash
docker ps
```

**Expected output:**
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
(empty or list of containers)
```

If you see error, Docker isn't running → Start it

### Step 2: Verify You're in Right Directory

```bash
pwd
ls Dockerfile
```

**Expected output:**
```
/path/to/clrag
Dockerfile
```

### Step 3: Verify File Permissions

```bash
ls -la Dockerfile requirements.txt
```

**Expected output:**
```
-rw-r--r--  1 user  group  1234 Oct 20 12:00 Dockerfile
-rw-r--r--  1 user  group  5678 Oct 20 12:00 requirements.txt
```

### Step 4: Try Simple Build

```bash
# Use most explicit form
docker build -t rag-system:latest --no-cache .
```

---

## 🔧 Complete Fix Checklist

Copy-paste this to fix most issues:

```bash
# 1. Make sure Docker is running
echo "Is Docker running?"
docker ps

# 2. Go to correct directory
cd ~/path/to/clrag  # Replace with your path
pwd
ls Dockerfile

# 3. Clean build (ignore cache)
docker build --no-cache -t rag-system:latest .

# 4. Verify it worked
docker images | grep rag-system
```

---

## 🚨 Nuclear Option (Last Resort)

If nothing else works:

```bash
# 1. Stop Docker Desktop completely
# macOS: Quit Docker app (Cmd+Q)
# Windows: Exit Docker (right-click tray icon → Exit)
# Linux: sudo systemctl stop docker

# 2. Clean everything
docker system prune -a --volumes

# 3. Restart Docker
# macOS: open /Applications/Docker.app
# Windows: Start-Process Docker
# Linux: sudo systemctl start docker

# 4. Wait 30 seconds
sleep 30

# 5. Try again
cd ~/path/to/clrag
docker build -t rag-system:latest .
```

---

## 📋 Quick Reference

| Error | Fix |
|-------|-----|
| "requires 1 argument" | Add `.` at end: `docker build -t rag-system:latest .` |
| "Cannot connect to daemon" | Start Docker Desktop/service |
| "Cannot find Dockerfile" | Navigate to repo root: `cd clrag` |
| "permission denied" | Add user to docker group: `sudo usermod -aG docker $USER` |
| "context too large" | Create `.dockerignore` file |
| "Step X failed" | Check `requirements.txt` exists |
| "Tag is invalid" | Use lowercase: `rag-system:latest` |

---

## 🎯 The Correct Command

For your laptop, the correct full command is:

```bash
docker build -t rag-system:latest .
```

Breaking it down:
- `docker build` = build an image
- `-t rag-system:latest` = tag it as "rag-system" with version "latest"
- `.` = **from current directory** (REQUIRED!)

---

## 💬 Still Having Issues?

### Share this info when asking for help:

```bash
# What's your OS?
uname -a

# Is Docker running?
docker ps

# Are you in the right directory?
pwd
ls Dockerfile

# What's the exact error?
docker build -t rag-system:latest .
```

---

## ✅ Success Check

When it works, you'll see:

```
Sending build context to Docker daemon  45.09MB
Step 1/8 : FROM python:3.11-slim
Step 2/8 : WORKDIR /app
...
Step 8/8 : CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "7000"]
...
Successfully tagged rag-system:latest
```

**If you see "Successfully tagged", you're done!** ✅

---

Happy building! 🐳
