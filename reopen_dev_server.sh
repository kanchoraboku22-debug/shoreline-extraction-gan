#!/bin/bash

################################################################################
#                                                                              #
#   Shoreline Extraction GAN - Dev Server Reopen Script                       #
#   Linux/macOS Bash - One-Click Dev Environment Restart                      #
#                                                                              #
#   This script reopens your development server exactly where you left off,   #
#   with all data and configurations intact.                                  #
#                                                                              #
################################################################################

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Function to print header
print_header() {
    clear
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                                                                ║"
    echo "║     🐳 SHORELINE EXTRACTION GAN - DEV SERVER REOPEN 🐳        ║"
    echo "║                                                                ║"
    echo "║               Reopening Development Environment...            ║"
    echo "║                                                                ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Function to check command availability
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Print header
print_header
echo ""

# Check if Docker is installed
if ! command_exists docker; then
    echo -e "${RED}❌ ERROR: Docker is not installed or not in PATH${NC}"
    echo ""
    echo "Please:"
    echo "  1. Install Docker from https://www.docker.com/"
    echo "  2. Make sure Docker daemon is running"
    echo "  3. Run this script again"
    echo ""
    exit 1
fi

# Check if Docker daemon is running
if ! docker ps > /dev/null 2>&1; then
    echo -e "${RED}❌ ERROR: Docker daemon is not running${NC}"
    echo ""
    echo "Please start Docker and try again"
    echo ""
    exit 1
fi

echo "Checking for existing container..."
echo ""

# Check if container exists and is running
if docker ps --filter "name=shoreline_gan_gui" --format "{{.Names}}" | grep -q "shoreline_gan_gui"; then
    echo -e "${GREEN}✅ Container found and is running!${NC}"
    echo ""
    echo "Attaching to container..."
    sleep 2
    docker attach shoreline_gan_gui
    exit $?
fi

# Check if container exists but is stopped
if docker ps -a --filter "name=shoreline_gan_gui" --format "{{.Names}}" | grep -q "shoreline_gan_gui"; then
    echo -e "${YELLOW}⏸️  Container found (stopped). Restarting...${NC}"
    echo ""
    docker start shoreline_gan_gui
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ Container restarted! Attaching now...${NC}"
        sleep 3
        docker attach shoreline_gan_gui
        exit $?
    else
        echo -e "${RED}❌ Failed to start container${NC}"
        echo ""
        echo "Try:"
        echo "  docker logs shoreline_gan_gui"
        echo "  docker rm shoreline_gan_gui"
        exit 1
    fi
fi

# Container doesn't exist - create it
echo -e "${YELLOW}⚠️  No existing container found. Creating new development environment...${NC}"
echo ""
echo "This will:"
echo "  • Pull the latest shoreline-gan image"
echo "  • Create a new dev container"
echo "  • Mount your data and model_outputs directories"
echo "  • Enable GPU support (if available)"
echo ""
echo -e "${CYAN}⏳ Please wait (this may take 1-5 minutes on first run)...${NC}"
echo ""

docker run --gpus all -it \
  --name shoreline_gan_gui \
  -v "$SCRIPT_DIR/data:/app/data" \
  -v "$SCRIPT_DIR/model_outputs:/app/model_outputs" \
  -p 8000:8000 \
  kanchoraboku22/shoreline-gan:latest

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Failed to start container${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check Docker is running: docker ps"
    echo "  2. Check Docker logs: docker logs shoreline_gan_gui"
    echo "  3. Try removing old container: docker rm shoreline_gan_gui"
    echo "  4. Rebuild image: docker build -t shoreline_gan:latest ."
    echo ""
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Development server reopened successfully!${NC}"
echo ""
exit 0
