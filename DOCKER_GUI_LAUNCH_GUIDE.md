# 🐳 Docker GUI Launch Guide - Shoreline Extraction GAN

## Overview

This guide provides **one-click Docker deployment** with integrated PyQt6 GUI for the Shoreline Extraction GAN pipeline. The scripts handle GPU support, X11 forwarding, data mounting, and automatic GUI launching across Windows, Linux, and macOS.

---

## 🚀 Quick Start

### Windows
```batch
LAUNCH_DOCKER_GUI.bat
```
Double-click the batch file. The container will build, start, and launch the PyQt6 GUI.

### Linux
```bash
bash launch_docker_gui.sh
```

### macOS
```bash
bash launch_docker_gui.sh
```
(Requires XQuartz for GUI support)

---

## 📋 Prerequisites

### Windows
- **Docker Desktop** (latest version)
- **WSL2 backend** (Windows Subsystem for Linux 2)
- GPU support requires NVIDIA Docker runtime and CUDA drivers

### Linux
- **Docker** and **Docker Compose**
- **NVIDIA Docker runtime** (for GPU)
- **X11 server** (usually pre-installed on most Linux distributions)
- `xhost` command available (for X11 permissions)

### macOS
- **Docker Desktop** (latest version)
- **XQuartz** (download from https://www.xquartz.org/)
- GPU support limited (macOS Docker doesn't support GPU natively yet)

---

## 🎯 Features

✅ **Automatic Docker image build**
✅ **Container lifecycle management** (cleanup, restart)
✅ **GPU support** (NVIDIA CUDA)
✅ **Volume mounting** for data persistence
✅ **X11 forwarding** for GUI rendering
✅ **PyQt6 GUI auto-launch** (if display available)
✅ **Headless fallback** (interactive shell if no display)
✅ **Multi-platform support** (Windows, Linux, macOS)
✅ **Production-ready** with error handling

---

## 📁 File Structure

```
shoreline-extraction-gan/
├── LAUNCH_DOCKER_GUI.bat          # Windows launcher (double-click)
├── launch_docker_gui.sh            # Linux/macOS launcher (bash script)
├── docker_entrypoint_gui.sh        # Container entrypoint (GUI + headless)
├── Dockerfile                      # Container image definition
├── data/                           # Input data (mounted in container)
├── model_outputs/                  # Results (persistent across runs)
├── shoreline_gui_advanced.py       # Advanced dashboard
├── shoreline_gui_pipeline.py       # Pipeline executor
└── PHASE_*.py                      # Pipeline phases
```

---

## 🔧 Configuration

### Enable/Disable GPU Support

**With GPU (default):**
```bash
docker run --gpus all ...
```

**Without GPU (CPU only):**
Edit the launcher scripts and change:
```bash
# FROM:
docker run --gpus all ...

# TO:
docker run ...
```

### Change Port Mappings

Default ports:
- `8888` - Jupyter notebook
- `5000` - Flask API

To change, edit the launcher script:
```bash
# FROM:
-p 8888:8888 -p 5000:5000 \

# TO:
-p 9999:8888 -p 6000:5000 \
```

### Custom Volume Mounts

To mount additional directories, add `-v` flags:
```bash
-v "$(pwd)/custom_data:/app/custom_data" \
```

---

## 🖥️ GUI Support Details

### Windows (Docker Desktop)

**X11 Forwarding:** Uses `host.docker.internal:0` to access X Server on host.

**Requirements:**
- Windows X server (e.g., VcXsrv, Xming) running on host
- Or use WSL2 with X11 server installed

**Troubleshooting:**
```bash
# If GUI doesn't appear, check X server is running
# On Windows, download and run: https://sourceforge.net/projects/vcxsrv/
```

### Linux

**X11 Forwarding:** Uses socket-based X11 forwarding (most reliable).

**How it works:**
```bash
-v /tmp/.X11-unix:/tmp/.X11-unix:rw    # Share X11 socket
-e DISPLAY=$DISPLAY                     # Forward DISPLAY variable
```

**Troubleshooting:**
```bash
# Verify X11 socket exists
ls -l /tmp/.X11-unix

# Grant Docker access to X11
xhost +local:docker

# Check DISPLAY variable
echo $DISPLAY
```

### macOS (XQuartz)

**X11 Forwarding:** Uses XQuartz (official macOS X11 server).

**How it works:**
1. Script auto-starts XQuartz if not running
2. Runs `xhost +local:docker` to allow Docker containers
3. Uses `host.docker.internal:0` for display

**Setup (one-time):**
```bash
# Download XQuartz
open https://www.xquartz.org/

# Or via Homebrew
brew install xquartz

# Allow Docker access
xhost +local:docker
```

**Troubleshooting:**
```bash
# Check if XQuartz is running
pgrep -l X11

# Manually start XQuartz
open -a XQuartz

# Grant Docker access
xhost +local:docker
```

---

## 🎬 Workflow Examples

### Example 1: Run Advanced Dashboard

```bash
bash launch_docker_gui.sh
# GUI launches automatically
# Use the dashboard to monitor pipeline execution
# Outputs saved to model_outputs/
```

### Example 2: Run Pipeline in Headless Mode

If X11 is not available, the container starts an interactive shell:

```bash
bash launch_docker_gui.sh
# (X11 not found, starting interactive shell)
# root@container:/app# python3 PHASE_1_QUICK_START.py
# (pipeline runs)
# root@container:/app# exit
```

### Example 3: Custom Pipeline with Data

```bash
# Edit launcher to add custom data volume
-v "$(pwd)/my_data:/app/my_data" \

# Run and use custom data in pipeline
bash launch_docker_gui.sh
# (in container)
# python3 PHASE_1_QUICK_START.py --data /app/my_data/
```

### Example 4: Check Container Logs

While container is running in another terminal:

```bash
docker logs -f shoreline_gan
# Shows real-time pipeline output
```

### Example 5: Execute Commands in Running Container

```bash
docker exec -it shoreline_gan python3 PHASE_2_QUICK_START.py
# Runs Phase 2 in the existing container
```

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to Docker daemon"

**Solution:**
```bash
# On Windows: Start Docker Desktop
# On Linux: Start Docker service
sudo systemctl start docker

# On macOS: Start Docker Desktop
open -a Docker
```

### Issue: "GPU not available"

**Solution:**
```bash
# Check if NVIDIA Docker runtime is installed
docker run --rm --gpus all nvidia/cuda:11.0 nvidia-smi

# If not, install NVIDIA Docker runtime:
# https://github.com/NVIDIA/nvidia-docker
```

### Issue: GUI doesn't appear

**Windows:**
- Install X server (VcXsrv, Xming, etc.)
- Edit launcher to use correct X server address

**Linux:**
- Run: `xhost +local:docker`
- Check: `echo $DISPLAY`

**macOS:**
- Install XQuartz: `brew install xquartz`
- Run: `xhost +local:docker`

### Issue: "Permission denied" on Linux

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Then run without sudo
bash launch_docker_gui.sh
```

### Issue: Container exits immediately

**Solution:**
```bash
# Check container logs
docker logs shoreline_gan

# If X11 error, disable GUI:
# Edit launcher and remove -e DISPLAY or run in headless mode
```

---

## 📊 Performance Tips

### 1. **Cache Docker Layers**

The first build takes time, but subsequent builds are faster due to layer caching:

```bash
# First run: ~10-30 minutes (builds everything)
LAUNCH_DOCKER_GUI.bat

# Second run: ~5-10 minutes (uses cached layers)
LAUNCH_DOCKER_GUI.bat
```

### 2. **Use Persistent Volumes**

Model outputs are automatically persisted to `model_outputs/`:

```bash
# Outputs from multiple runs accumulate
ls model_outputs/  # Contains results from all runs
```

### 3. **Monitor Resource Usage**

```bash
# In another terminal, watch container stats
docker stats shoreline_gan

# Shows: CPU, memory, network I/O, block I/O
```

### 4. **Optimize GPU Usage**

Monitor GPU in container:

```bash
docker exec -it shoreline_gan nvidia-smi -l 1
# Updates every 1 second
```

---

## 🔒 Security Best Practices

1. **Use version-specific image tags:**
   ```bash
   docker tag shoreline_gan:latest shoreline_gan:v1.0.0
   ```

2. **Don't mount unnecessary volumes:**
   ```bash
   # ✓ Good: mount only required directories
   -v "$(pwd)/data:/app/data" \
   
   # ✗ Bad: mounting home directory
   -v ~:/home/user \
   ```

3. **Run as non-root user (if possible):**
   ```dockerfile
   # In Dockerfile
   RUN useradd -m appuser
   USER appuser
   ```

4. **Limit container resources:**
   ```bash
   docker run --memory=8g --cpus=4 ...
   ```

---

## 📚 Advanced Usage

### Custom Entrypoint

To run a different script at startup, modify the launcher:

```bash
# FROM:
shoreline_gan:latest bash docker_entrypoint_gui.sh

# TO:
shoreline_gan:latest python3 my_custom_script.py
```

### Docker Compose

For more complex setups, use Docker Compose:

```yaml
version: '3.8'
services:
  shoreline_gan:
    image: shoreline_gan:latest
    container_name: shoreline_gan
    volumes:
      - ./data:/app/data
      - ./model_outputs:/app/model_outputs
    ports:
      - "8888:8888"
      - "5000:5000"
    environment:
      - DISPLAY=${DISPLAY}
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix:rw  # Linux only
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

Then run:
```bash
docker-compose up
```

---

## 🎓 Learning Resources

- **Docker Documentation:** https://docs.docker.com/
- **PyQt6 Documentation:** https://www.riverbankcomputing.com/static/Docs/PyQt6/
- **X11 Forwarding:** https://en.wikipedia.org/wiki/X_Window_System
- **NVIDIA Docker:** https://github.com/NVIDIA/nvidia-docker

---

## ✅ Verification Checklist

After launching the container:

- [ ] Docker image built successfully
- [ ] Container started without errors
- [ ] Data volumes mounted correctly
- [ ] GUI appears (if X11 configured)
- [ ] Pipeline runs in background
- [ ] Outputs saved to `model_outputs/`
- [ ] Container logs show no errors
- [ ] GPU detected (if using GPU)

---

## 📞 Support

**Issues with Docker launcher?**
1. Check logs: `docker logs shoreline_gan`
2. Verify prerequisites are installed
3. Ensure Docker daemon is running
4. Check volume permissions

**Issues with GUI?**
1. Verify X11/XQuartz is installed
2. Run: `xhost +local:docker`
3. Check DISPLAY variable: `echo $DISPLAY`
4. Try headless mode (omit GUI launch)

**Issues with GPU?**
1. Check NVIDIA Docker runtime: `docker run --rm --gpus all nvidia/cuda:11.0 nvidia-smi`
2. Verify NVIDIA drivers: `nvidia-smi`
3. Fallback to CPU: Remove `--gpus all` flag

---

**🚀 You're all set! Your Shoreline Extraction GAN pipeline is now fully containerized and production-ready.**
