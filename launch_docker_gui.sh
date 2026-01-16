#!/bin/bash
# Shoreline Extraction GAN - Docker Launcher with PyQt6 GUI (Linux/Mac)

# Step 1: Build the Docker image
echo "Building Docker image..."
docker build -t shoreline_gan:latest .

# Step 2: Stop & remove old container
echo "Cleaning up old container if exists..."
docker stop shoreline_gan 2>/dev/null
docker rm shoreline_gan 2>/dev/null

# Step 3: Detect OS and configure X11 forwarding
OS_TYPE=$(uname -s)

if [[ "$OS_TYPE" == "Linux" ]]; then
    echo "Running on Linux with X11 forwarding..."
    docker run --gpus all -it --name shoreline_gan \
        -v "$(pwd)/data:/app/data" \
        -v "$(pwd)/model_outputs:/app/model_outputs" \
        -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
        -e DISPLAY=$DISPLAY \
        -p 8888:8888 -p 5000:5000 \
        shoreline_gan:latest bash docker_entrypoint_gui.sh

elif [[ "$OS_TYPE" == "Darwin" ]]; then
    echo "Running on macOS with XQuartz forwarding..."
    # First, ensure XQuartz is running
    if ! pgrep -q "X11"; then
        echo "Starting XQuartz..."
        open -a XQuartz
        sleep 2
    fi
    # Allow Docker containers to connect to XQuartz
    xhost +local:docker
    docker run --gpus all -it --name shoreline_gan \
        -v "$(pwd)/data:/app/data" \
        -v "$(pwd)/model_outputs:/app/model_outputs" \
        -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
        -e DISPLAY=host.docker.internal:0 \
        -p 8888:8888 -p 5000:5000 \
        shoreline_gan:latest bash docker_entrypoint_gui.sh

else
    echo "Unsupported OS: $OS_TYPE"
    exit 1
fi

echo "Docker container with GUI is running!"
echo "Pipeline execution output will appear above."
