# Use official Python runtime as base image
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies including GUI support
RUN apt-get update && apt-get install -y \
    build-essential \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    git \
    wget \
    libxkbcommon-x11-0 \
    libdbus-1-3 \
    libfontconfig1 \
    libxext6 \
    libxrender1 \
    mesa-utils \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL environment variables
ENV GDAL_CONFIG=/usr/bin/gdal-config \
    CPLUS_INCLUDE_PATH=/usr/include/gdal \
    C_INCLUDE_PATH=/usr/include/gdal

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies (core + GUI)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt || true && \
    pip install --no-cache-dir --only-binary=:all: PyQt6-sip PyQt6 PyQt6-Charts matplotlib 2>/dev/null || \
    pip install --no-cache-dir matplotlib plotly jupyter flask

# Copy project files
COPY . .

# Create output directories
RUN mkdir -p model_outputs/{analysis,processed,validation_plots}

# Expose ports for Jupyter and GUI services
EXPOSE 8888 5000 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CONDA_DEFAULT_ENV=shoreline_gan \
    PATH=/opt/conda/envs/shoreline_gan/bin:$PATH \
    QT_QPA_PLATFORM=offscreen

# Use docker_entrypoint_gui.sh as entrypoint for smart GUI/headless detection
ENTRYPOINT ["bash", "docker_entrypoint_gui.sh"]

# Default command: Run advanced GUI dashboard
CMD ["python", "shoreline_gui_advanced.py"]

# Alternative: Run pipeline executor GUI
# CMD ["python", "shoreline_gui_pipeline.py"]

# Alternative: Run standalone GUI
# CMD ["python", "shoreline_gui.py"]

# Alternative: Run complete pipeline
# CMD ["python", "scripts/run_phase3_full.py"]

# Alternative: Start Jupyter for interactive analysis
# ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]

# Build: docker build -t shoreline-gan:latest .
# Run GUI with X11 forwarding (Linux/macOS):
#   docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix shoreline-gan:latest
# Run pipeline executor:
#   docker run shoreline-gan:latest python shoreline_gui_pipeline.py
# Run:   docker run -v /data:/app/data -v /output:/app/model_outputs shoreline-gan:1.0
# Jupyter: docker run -p 8888:8888 -v /data:/app/data -v /output:/app/model_outputs shoreline-gan:1.0
