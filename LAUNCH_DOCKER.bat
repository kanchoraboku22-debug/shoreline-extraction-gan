@echo off
REM Shoreline Extraction GAN - Docker Launcher (Windows)

REM Step 1: Build the Docker image
echo Building Docker image...
docker build -t shoreline_gan:latest .

REM Step 2: Stop and remove any existing container
echo Cleaning up old container if exists...
docker stop shoreline_gan 2>nul
docker rm shoreline_gan 2>nul

REM Step 3: Run the container with GPU support
echo Running Docker container...
docker run --gpus all -it --name shoreline_gan ^
    -v "%cd%\data:/app/data" ^
    -v "%cd%\model_outputs:/app/model_outputs" ^
    -p 8888:8888 -p 5000:5000 ^
    shoreline_gan:latest

REM Optional: Launch PyQt6 GUI
REM Uncomment the line below if you want the GUI to launch automatically
REM docker exec -it shoreline_gan python3 shoreline_gui_pipeline.py

echo Docker container is running!
pause
