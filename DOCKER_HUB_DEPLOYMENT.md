# Docker Hub Deployment Guide

**Publish your Shoreline Extraction GAN application to Docker Hub for cloud-based execution**

---

## 📋 Prerequisites

1. **Docker Installed**
   ```bash
   docker --version
   ```

2. **Docker Hub Account**
   - Sign up at https://hub.docker.com/
   - Free tier includes unlimited public repositories

3. **Command Line Access**
   - Windows: PowerShell or Command Prompt
   - macOS/Linux: Terminal

---

## 🚀 Step 1: Build Docker Image

Navigate to project root and build:

```bash
cd "path/to/Shoreline_Extraction_GAN-main"

# Build image
docker build -t shoreline-gan:latest .

# Verify build succeeded
docker images | grep shoreline-gan
```

**Output should show:**
```
shoreline-gan    latest    <IMAGE_ID>    <SIZE>    <DATE>
```

---

## 🔐 Step 2: Create Docker Hub Account & Login

### Create Account (if needed)
1. Visit https://hub.docker.com/signup
2. Enter email and create password
3. Verify email
4. Choose username (e.g., `yourusername`)

### Login from Command Line
```bash
docker login
```

Enter your Docker Hub credentials:
```
Username: yourusername
Password: [your_password]
Login Succeeded
```

---

## 📝 Step 3: Tag Image for Hub

Format: `dockerhubusername/repository-name:tag`

```bash
# Replace 'yourusername' with your Docker Hub username
docker tag shoreline-gan:latest yourusername/shoreline-extraction-gan:latest

# Also tag with version
docker tag shoreline-gan:latest yourusername/shoreline-extraction-gan:1.0.0
```

**Verify tags:**
```bash
docker images | grep shoreline
```

---

## ⬆️ Step 4: Push to Docker Hub

```bash
# Push latest tag
docker push yourusername/shoreline-extraction-gan:latest

# Push version tag
docker push yourusername/shoreline-extraction-gan:1.0.0

# Monitor progress (will show upload status)
```

**Expected output:**
```
Pushing yourusername/shoreline-extraction-gan:latest
The push refers to repository [docker.io/yourusername/shoreline-extraction-gan]
abc123... Pushing [========>        ]
...
latest: digest: sha256:abc123... size: 5000
```

**This may take 5-15 minutes depending on connection speed.**

---

## ✅ Step 5: Verify on Docker Hub

1. Visit https://hub.docker.com/repositories
2. Find `shoreline-extraction-gan`
3. Check:
   - ✅ Repository is public
   - ✅ Description visible
   - ✅ Tags listed (latest, 1.0.0)
   - ✅ Dockerfile visible

---

## 🎯 Step 6: Update Repository Information

### Add Description
On Docker Hub page:
1. Click "Edit description"
2. Add:
   ```
   Deep Learning-based Shoreline Extraction & Forecasting System
   
   Features:
   - 3,204 shoreline contours extracted via Pix2Pix GAN
   - 62 transects analyzed for coastal change
   - 124 LSTM-based forecasts (2034, 2044)
   - Interactive PyQt6 GUI dashboard
   - 30 DPI publication-quality visualizations
   - Complete pipeline execution
   
   Quick Start:
   docker run -it yourusername/shoreline-extraction-gan:latest python shoreline_gui_advanced.py
   ```

### Add Readme
Create `README.md` in Docker Hub:
```
# Shoreline Extraction GAN

## Quick Start

### Run Advanced Dashboard
docker run -it yourusername/shoreline-extraction-gan:latest python shoreline_gui_advanced.py

### Run Pipeline Executor
docker run yourusername/shoreline-extraction-gan:latest python shoreline_gui_pipeline.py

### Run with GPU
docker run --gpus all yourusername/shoreline-extraction-gan:latest python shoreline_gui_advanced.py

## Documentation
- [GitHub Repository](https://github.com/yourusername/shoreline-extraction-gan)
- [User Guide](https://github.com/yourusername/shoreline-extraction-gan/docs/GUI_USER_GUIDE.md)
- [Manuscript](https://github.com/yourusername/shoreline-extraction-gan/MANUSCRIPT_TEMPLATE.md)

## Citation
@software{shoreline_gan_2026,
  title={Shoreline Extraction GAN},
  author={Your Name},
  year={2026},
  url={https://github.com/yourusername/shoreline-extraction-gan}
}
```

---

## 🌐 Deployment Options

### Option 1: Local System (Any OS)
```bash
# Pull and run
docker pull yourusername/shoreline-extraction-gan:latest
docker run -it yourusername/shoreline-extraction-gan:latest python shoreline_gui_advanced.py
```

### Option 2: Google Cloud Run
```bash
# Configure Docker authentication
gcloud auth configure-docker

# Tag for Cloud Registry
docker tag shoreline-gan:latest gcr.io/PROJECT_ID/shoreline-gan:latest

# Push to Google Cloud
docker push gcr.io/PROJECT_ID/shoreline-gan:latest

# Deploy
gcloud run deploy shoreline-gan --image gcr.io/PROJECT_ID/shoreline-gan:latest
```

### Option 3: AWS ECR
```bash
# Create ECR repository
aws ecr create-repository --repository-name shoreline-gan

# Push to ECR
docker push ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/shoreline-gan:latest

# Run on EC2
docker pull ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/shoreline-gan:latest
docker run -it ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/shoreline-gan:latest python shoreline_gui_advanced.py
```

### Option 4: Azure Container Registry
```bash
# Login to Azure
az acr login --name myregistry

# Tag image
docker tag shoreline-gan:latest myregistry.azurecr.io/shoreline-gan:latest

# Push
docker push myregistry.azurecr.io/shoreline-gan:latest

# Deploy
az container create --resource-group mygroup --name shoreline-gan --image myregistry.azurecr.io/shoreline-gan:latest
```

### Option 5: Kubernetes
```bash
# Create deployment manifest (shoreline-deployment.yaml)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shoreline-gan
spec:
  replicas: 3
  selector:
    matchLabels:
      app: shoreline-gan
  template:
    metadata:
      labels:
        app: shoreline-gan
    spec:
      containers:
      - name: shoreline-gan
        image: yourusername/shoreline-extraction-gan:latest
        ports:
        - containerPort: 8000

# Deploy
kubectl apply -f shoreline-deployment.yaml
```

---

## 📊 Container Usage Examples

### Basic Usage
```bash
docker pull yourusername/shoreline-extraction-gan:latest
docker run yourusername/shoreline-extraction-gan:latest python shoreline_gui_pipeline.py
```

### Mount Local Data
```bash
docker run -v /path/to/data:/app/data yourusername/shoreline-extraction-gan:latest
```

### GPU Support
```bash
docker run --gpus all yourusername/shoreline-extraction-gan:latest
```

### Custom Command
```bash
docker run yourusername/shoreline-extraction-gan:latest python export_publication_charts.py
```

### Interactive Mode
```bash
docker run -it yourusername/shoreline-extraction-gan:latest /bin/bash
```

---

## 🔒 Security Best Practices

### 1. Use Version Tags
```bash
# Good
docker pull yourusername/shoreline-extraction-gan:1.0.0

# Avoid
docker pull yourusername/shoreline-extraction-gan  # defaults to 'latest'
```

### 2. Scan for Vulnerabilities
```bash
# Docker Scout (built-in)
docker scout cves yourusername/shoreline-extraction-gan:latest

# Third-party: Trivy
trivy image yourusername/shoreline-extraction-gan:latest
```

### 3. Keep Base Image Updated
```dockerfile
# Update base image regularly
FROM python:3.11-slim  # Check for security patches
```

### 4. Never Commit Secrets
```bash
# Don't include in Dockerfile:
# - API keys
# - Passwords
# - Authentication tokens

# Use environment variables instead
docker run -e API_KEY=xxx yourusername/shoreline-extraction-gan:latest
```

---

## 📈 Performance Optimization

### Reduce Image Size
Current size: ~2-3 GB

To reduce:
```dockerfile
# Use multi-stage builds
FROM python:3.11-slim as builder
# ... build dependencies ...

FROM python:3.11-slim as runtime
COPY --from=builder /app /app
```

### Cache Layers
```dockerfile
# Order matters for caching
COPY requirements.txt .
RUN pip install -r requirements.txt  # Cache this layer
COPY . /app  # Only this layer changes with code
```

---

## 🚨 Troubleshooting

### Build fails
```bash
# Check Docker daemon
docker ps

# Clear build cache
docker builder prune

# Rebuild
docker build --no-cache -t shoreline-gan:latest .
```

### Push fails
```bash
# Check login
docker logout
docker login

# Verify repository exists
docker tag shoreline-gan yourusername/shoreline-extraction-gan:latest

# Try again
docker push yourusername/shoreline-extraction-gan:latest
```

### Container won't run
```bash
# Check image
docker images | grep shoreline

# Check logs
docker logs <CONTAINER_ID>

# Rebuild from scratch
docker build --no-cache -t shoreline-gan:latest .
```

---

## 📝 Sharing Your Container

### Share Pull Command
```
docker pull yourusername/shoreline-extraction-gan:latest
```

### Docker Compose (optional)
Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  shoreline-gan:
    image: yourusername/shoreline-extraction-gan:latest
    volumes:
      - ./data:/app/data
      - ./model_outputs:/app/model_outputs
    environment:
      - CUDA_VISIBLE_DEVICES=0
    stdin_open: true
    tty: true
```

Run with:
```bash
docker-compose up
```

---

## 📊 Maintenance

### Update Image
```bash
# Make code changes
git pull origin main

# Rebuild locally
docker build -t shoreline-gan:latest .

# Test
docker run -it shoreline-gan:latest python shoreline_gui_advanced.py

# Tag and push
docker tag shoreline-gan:latest yourusername/shoreline-extraction-gan:1.1.0
docker push yourusername/shoreline-extraction-gan:1.1.0
docker tag shoreline-gan:latest yourusername/shoreline-extraction-gan:latest
docker push yourusername/shoreline-extraction-gan:latest
```

### View Download Statistics
On Docker Hub:
- Click your repository
- View "Pulls" and "Stars"
- Check "Activity" for recent usage

---

## ✅ Deployment Checklist

Before publishing:

- [ ] Image builds successfully locally
- [ ] Image runs all GUI applications
- [ ] Docker Hub account created and verified
- [ ] Image tagged with username
- [ ] Image pushed to Docker Hub
- [ ] Repository description added
- [ ] README created on Docker Hub
- [ ] Links updated (GitHub, documentation)
- [ ] Security scan passed
- [ ] Image size acceptable
- [ ] Tested on clean Docker install

---

## 🎉 Your Container is Live!

Share your Docker Hub repository:

```
🐳 Shoreline Extraction GAN - Now on Docker Hub!

Pull and run:
docker pull yourusername/shoreline-extraction-gan:latest
docker run -it yourusername/shoreline-extraction-gan:latest python shoreline_gui_advanced.py

GitHub: https://github.com/yourusername/shoreline-extraction-gan
Docker Hub: https://hub.docker.com/r/yourusername/shoreline-extraction-gan
```

---

## 📞 Support

- **Docker Documentation:** https://docs.docker.com/
- **Docker Hub Help:** https://docs.docker.com/docker-hub/
- **GitHub Issues:** Report problems on your GitHub repo
- **Container Registry Docs:** Google Cloud, AWS, Azure documentation

---

**Status:** ✅ Ready for Production Deployment

Your application is now accessible to anyone with Docker installed! 🚀
