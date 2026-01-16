# Use official Python runtime as base image
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL environment variables
ENV GDAL_CONFIG=/usr/bin/gdal-config \
    CPLUS_INCLUDE_PATH=/usr/include/gdal \
    C_INCLUDE_PATH=/usr/include/gdal

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create output directories
RUN mkdir -p model_outputs/{analysis,processed,validation_plots}

# Expose port for Jupyter (optional)
EXPOSE 8888

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CONDA_DEFAULT_ENV=shoreline_gan \
    PATH=/opt/conda/envs/shoreline_gan/bin:$PATH

# Default command runs the complete pipeline
CMD ["python", "scripts/run_phase3_full.py"]

# Alternative: Start Jupyter for interactive analysis
# ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]

# Build: docker build -t shoreline-gan:1.0 .
# Run:   docker run -v /data:/app/data -v /output:/app/model_outputs shoreline-gan:1.0
# Jupyter: docker run -p 8888:8888 -v /data:/app/data -v /output:/app/model_outputs shoreline-gan:1.0
