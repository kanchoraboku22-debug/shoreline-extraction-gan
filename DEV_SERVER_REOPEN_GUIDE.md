# 🔄 Dev Server Reopen Guide

**Quickly restart your development environment with one click!**

---

## 📋 Quick Reference

| Task | Windows | Linux/macOS |
|------|---------|------------|
| **Reopen Dev Server** | `REOPEN_DEV_SERVER.bat` | `bash reopen_dev_server.sh` |
| **Check Container Status** | `docker ps -a` | `docker ps -a` |
| **View Container Logs** | `docker logs shoreline_gan_gui` | `docker logs shoreline_gan_gui` |
| **Stop Container** | `docker stop shoreline_gan_gui` | `docker stop shoreline_gan_gui` |
| **Remove Container** | `docker rm shoreline_gan_gui` | `docker rm shoreline_gan_gui` |
| **Rebuild Image** | `docker build -t shoreline_gan:latest .` | `docker build -t shoreline_gan:latest .` |

---

## 🚀 Fastest Way to Reopen

### Windows
```batch
REOPEN_DEV_SERVER.bat
```

### Linux/macOS
```bash
bash reopen_dev_server.sh
```

That's it! The script will:
1. ✅ Check if Docker is running
2. ✅ Find your existing container
3. ✅ Restart it if stopped
4. ✅ Create a new one if needed
5. ✅ Attach automatically

---

## 🔍 What the Script Does

### On First Run
```
1. Detects no existing container
2. Pulls the latest shoreline-gan image
3. Creates new container named "shoreline_gan_gui"
4. Mounts data directories
5. Enables GPU support
6. Attaches to container
```

### On Subsequent Runs
```
1. Finds existing container
2. If running → Attaches immediately
3. If stopped → Restarts and attaches
4. All data is preserved
```

---

## 💡 Use Cases

### After Closing Terminal
```bash
bash reopen_dev_server.sh
# Container restarts automatically
# Everything is where you left it
```

### After Restarting Computer
```bash
bash reopen_dev_server.sh
# Creates new container with same name
# Mounts same data directories
# Environment is identical
```

### After Docker Restart
```bash
bash reopen_dev_server.sh
# Finds and restarts your container
# No data loss
```

### Clean Restart Needed
```bash
# First, stop and remove old container
docker stop shoreline_gan_gui
docker rm shoreline_gan_gui

# Then run reopen script
bash reopen_dev_server.sh
```

---

## 🔧 Troubleshooting

### Docker Not Running
**Error:** `Cannot connect to Docker daemon`

**Solution:**
1. Start Docker Desktop
2. Wait for it to fully load
3. Run reopen script again

### Container Won't Start
**Error:** `docker: error response from daemon`

**Solution:**
```bash
# Check logs
docker logs shoreline_gan_gui

# Remove and retry
docker rm shoreline_gan_gui
bash reopen_dev_server.sh
```

### Port Already in Use
**Error:** `bind: address already in use`

**Solution:**
```bash
# Find what's using port 8000
netstat -tlnp | grep 8000  # Linux
lsof -i :8000              # macOS

# Stop the conflicting container
docker stop <container_id>

# Or change port in script
docker run -p 8001:8000 ...  # Use different port
```

### GPU Not Detected
**Error:** `WARNING: NVIDIA Docker support not detected`

**Solution:**
1. Install NVIDIA Docker runtime
2. Or continue without GPU (CPU fallback)
3. GPU support is optional

### Image Pull Failed
**Error:** `Error pulling image`

**Solution:**
```bash
# Rebuild locally
docker build -t shoreline_gan:latest .
bash reopen_dev_server.sh
```

---

## 🎯 Inside the Dev Server

Once the container is running, you can:

### Launch GUI Applications
```bash
# PyQt6 Professional GUI
python shoreline_gan_professional.py

# Alternative GUI
python shoreline_gui.py

# Pipeline GUI
python shoreline_gui_pipeline.py
```

### Run Pipeline Commands
```bash
# Phase 1: Preprocessing
python PHASE_1_QUICK_START.py

# Phase 2: GAN Training
python PHASE_2_QUICK_START.py

# Phase 3: Temporal Analysis
python PHASE_3_QUICK_START.py
```

### Access Interactive Menu
```bash
# Windows (inside container with WSL)
python LAUNCH_QUICK_MENU.bat

# Linux/macOS
bash launch_quick_menu.sh
```

### Run Tests
```bash
python -m pytest test_docker_gui_integration.py -v
```

---

## 📊 Container Management

### View All Containers
```bash
docker ps -a
```

### View Container Logs (Real-Time)
```bash
docker logs -f shoreline_gan_gui
```

### Execute Command Inside Container
```bash
docker exec shoreline_gan_gui python --version
docker exec shoreline_gan_gui ls -la data/
```

### Copy Files From Container
```bash
docker cp shoreline_gan_gui:/app/model_outputs ./local_outputs
```

### Stop Container (Keep Data)
```bash
docker stop shoreline_gan_gui
# Later: REOPEN_DEV_SERVER.bat to restart
```

### Delete Container (Remove Data)
```bash
docker rm shoreline_gan_gui
# Creates fresh container when reopening
```

---

## ⚙️ Advanced Options

### Custom Port Mapping
Edit the reopen script and change:
```bash
-p 8000:8000  →  -p 9000:8000  # Access on port 9000
```

### Add Volume Mounts
Edit the script to add:
```bash
-v "$SCRIPT_DIR/custom_dir:/app/custom_dir" \
```

### Custom GPU Configuration
```bash
# Use specific GPU
docker run --gpus '"device=0"' ...

# Limit GPU memory
docker run --gpus all -e CUDA_VISIBLE_DEVICES=0 ...

# CPU only
docker run ... kanchoraboku22/shoreline-gan:latest
# (remove --gpus all flag)
```

### Interactive Shell
```bash
# Instead of attaching, get a shell
docker run -it shoreline_gan:latest /bin/bash
```

---

## 📝 Environment Variables

Set inside the running container:

```bash
# Enable GPU
export CUDA_VISIBLE_DEVICES=0

# Set Python path
export PYTHONPATH=/app:/app/utils

# Set output directory
export OUTPUT_DIR=/app/model_outputs

# Set logging level
export LOG_LEVEL=INFO
```

---

## 🔐 Best Practices

✅ **Always reopen using the script** (preserves state)  
✅ **Keep data/ and model_outputs/ mounted** (persistence)  
✅ **Stop container before restarting Docker** (`docker stop ...`)  
✅ **Use named containers** (easier to manage)  
✅ **Check logs if anything fails** (`docker logs ...`)  
✅ **Backup important results** (to local filesystem)  

❌ **Don't use `docker rm` unless you want to start fresh**  
❌ **Don't manually edit container names**  
❌ **Don't remove mounted directories**  
❌ **Don't ignore error messages**  

---

## 🎯 Daily Workflow

```
Morning:
1. bash reopen_dev_server.sh
   → Container starts/restarts
   → You're in the dev environment
   
2. python shoreline_gan_professional.py
   → GUI launches
   → Start your work

Afternoon:
3. docker stop shoreline_gan_gui
   → Save your progress
   → Container stops (keeps data)

Next Day:
4. bash reopen_dev_server.sh
   → Everything is back exactly as you left it
   → No setup needed
```

---

## 📞 Quick Help

### "I don't know what's wrong"
```bash
# Run these commands in order:
docker ps -a                          # Check container status
docker logs shoreline_gan_gui         # Check logs
docker inspect shoreline_gan_gui      # Check details
```

### "I want to start completely fresh"
```bash
docker stop shoreline_gan_gui
docker rm shoreline_gan_gui
docker image rm shoreline_gan:latest  # Or kanchoraboku22/shoreline-gan
bash reopen_dev_server.sh             # Start fresh
```

### "Container is stuck"
```bash
docker kill shoreline_gan_gui   # Force stop
docker rm shoreline_gan_gui     # Remove
bash reopen_dev_server.sh       # Restart
```

### "I need a shell inside the container"
```bash
docker exec -it shoreline_gan_gui /bin/bash
```

---

## 📖 See Also

- [PROFESSIONAL_GUI_README.md](PROFESSIONAL_GUI_README.md) - GUI usage guide
- [DOCKER_GUI_LAUNCH_GUIDE.md](DOCKER_GUI_LAUNCH_GUIDE.md) - Docker setup guide
- [QUICK_START_GUIDE.txt](QUICK_START_GUIDE.txt) - Architecture overview
- [README.md](README.md) - Project overview

---

<div align="center">

### 🔄 Reopen Dev Server - One Click Away

[REOPEN_DEV_SERVER.bat](REOPEN_DEV_SERVER.bat) (Windows) | [reopen_dev_server.sh](reopen_dev_server.sh) (Linux/macOS)

</div>
