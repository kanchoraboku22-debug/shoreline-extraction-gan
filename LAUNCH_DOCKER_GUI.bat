@echo off
REM Shoreline Extraction GAN - Docker Launcher with PyQt6 GUI (Windows)

REM Step 1: Build the Docker image
echo Building Docker image...
docker build -t shoreline_gan:latest .

REM Step 2: Stop and remove any existing container
echo Cleaning up old container if exists...
docker stop shoreline_gan 2>nul
docker rm shoreline_gan 2>nul

REM Step 3: Run the container with GPU support and GUI
echo Running Docker container with PyQt6 GUI support...

REM Option A: Using Docker Desktop with WSL2 (Recommended for Windows)
docker run --gpus all -it --name shoreline_gan ^
    -v "%cd%\data:/app/data" ^
    -v "%cd%\model_outputs:/app/model_outputs" ^
    -p 8888:8888 -p 5000:5000 ^
    -e DISPLAY=host.docker.internal:0 ^
    shoreline_gan:latest bash docker_entrypoint_gui.sh

REM Alternative: Mount /tmp/.X11-unix for X11 forwarding (if on WSL2 with X11 server)
REM docker run --gpus all -it --name shoreline_gan ^
REM     -v "%cd%\data:/app/data" ^
REM     -v "%cd%\model_outputs:/app/model_outputs" ^
REM     -v /tmp/.X11-unix:/tmp/.X11-unix:rw ^
REM     -p 8888:8888 -p 5000:5000 ^
REM     -e DISPLAY=:0 ^
REM     shoreline_gan:latest bash docker_entrypoint_gui.sh

echo Docker container with GUI is running!
echo Pipeline execution output will appear above.
pause
