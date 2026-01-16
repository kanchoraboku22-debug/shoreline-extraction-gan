#!/bin/bash
# Shoreline Extraction GAN - Docker Launcher (Linux/Mac)

# Step 1: Build the Docker image
echo "Building Docker image..."
docker build -t shoreline_gan:latest .

# Step 2: Stop & remove old container
echo "Cleaning up old container if exists..."
docker stop shoreline_gan 2>/dev/null
docker rm shoreline_gan 2>/dev/null

# Step 3: Run container with GPU support
echo "Running Docker container..."
docker run --gpus all -it --name shoreline_gan \
    -v "$(pwd)/data:/app/data" \
    -v "$(pwd)/model_outputs:/app/model_outputs" \
    -p 8888:8888 -p 5000:5000 \
    shoreline_gan:latest

# Optional: Launch GUI inside container
# docker exec -it shoreline_gan python3 shoreline_gui_pipeline.py

echo "Docker container is running!"
