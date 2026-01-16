#!/bin/bash

################################################################################
#                                                                              #
#   Shoreline Extraction GAN - Professional GUI Quick Launcher                #
#   Linux/macOS Bash Script                                                   #
#                                                                              #
#   This script provides an interactive menu to launch various components     #
#   of the Shoreline Extraction GAN system                                    #
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
    echo "║      🌊 SHORELINE EXTRACTION GAN - PROFESSIONAL GUI 🌊        ║"
    echo "║                                                                ║"
    echo "║           Coastal Erosion Monitoring Platform v2.0            ║"
    echo "║                                                                ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Function to print menu
print_menu() {
    echo ""
    echo "Select Launch Option:"
    echo ""
    echo "  ${CYAN}[1]${NC} 🖥️  Launch Professional GUI (Desktop Application)"
    echo "  ${CYAN}[2]${NC} 🐳  Launch GUI via Docker (Containerized)"
    echo "  ${CYAN}[3]${NC} ⚡  Run Quick Pipeline (Phase 1-2-3)"
    echo "  ${CYAN}[4]${NC} 📊  Run Integration Tests"
    echo "  ${CYAN}[5]${NC} 📖  Open Documentation"
    echo "  ${CYAN}[6]${NC} ⚙️  Open Settings/Configuration"
    echo "  ${CYAN}[7]${NC} 📁  Open Project Folder"
    echo "  ${CYAN}[8]${NC} 🔧  System Diagnostics"
    echo "  ${CYAN}[9]${NC} ❌  Exit"
    echo ""
}

# Function to check command availability
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main menu
show_menu() {
    while true; do
        print_header
        print_menu
        read -p "Enter your choice [1-9]: " choice
        
        case $choice in
            1) launch_gui ;;
            2) launch_docker ;;
            3) quick_pipeline ;;
            4) run_tests ;;
            5) open_docs ;;
            6) open_settings ;;
            7) open_folder ;;
            8) system_diagnostics ;;
            9) exit_menu ;;
            *) echo -e "${RED}Invalid choice. Please try again.${NC}"; sleep 2 ;;
        esac
    done
}

# Launch GUI
launch_gui() {
    clear
    echo -e "${BLUE}"
    echo "═══════════════════════════════════════════════════════════════"
    echo " 🖥️  Launching Professional GUI..."
    echo "═══════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    echo ""
    
    # Check if Python is installed
    if ! command_exists python3; then
        echo -e "${RED}❌ ERROR: Python3 is not installed or not in PATH${NC}"
        echo ""
        echo "Please install Python 3.11+ from https://www.python.org/"
        echo ""
        read -p "Press Enter to continue..."
        return
    fi
    
    # Check if PyQt6 is installed
    if ! python3 -c "import PyQt6" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  PyQt6 not found. Installing dependencies...${NC}"
        pip install --upgrade PyQt6 PyQt6-Charts matplotlib psutil pandas
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Failed to install dependencies${NC}"
            read -p "Press Enter to continue..."
            return
        fi
    fi
    
    echo "Starting application..."
    echo ""
    python3 shoreline_gan_professional.py
    
    if [ $? -ne 0 ]; then
        echo ""
        echo -e "${RED}❌ Error launching GUI. Check console output above.${NC}"
        read -p "Press Enter to continue..."
    fi
}

# Launch Docker
launch_docker() {
    clear
    echo -e "${BLUE}"
    echo "═══════════════════════════════════════════════════════════════"
    echo " 🐳  Launching GUI via Docker..."
    echo "═══════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    echo ""
    
    # Check if Docker is installed
    if ! command_exists docker; then
        echo -e "${RED}❌ ERROR: Docker is not installed${NC}"
        echo ""
        echo "Please install Docker from https://www.docker.com/"
        echo ""
        read -p "Press Enter to continue..."
        return
    fi
    
    echo "Starting Docker launcher..."
    echo ""
    
    # Detect OS and run appropriate script
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        bash launch_docker_gui.sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        bash launch_docker_gui.sh
    else
        echo -e "${RED}❌ Unsupported OS for Docker launcher${NC}"
        read -p "Press Enter to continue..."
        return
    fi
    
    if [ $? -ne 0 ]; then
        echo ""
        echo -e "${YELLOW}⚠️  Docker launcher returned an error${NC}"
        read -p "Press Enter to continue..."
    fi
}

# Quick pipeline
quick_pipeline() {
    clear
    echo -e "${BLUE}"
    echo "═══════════════════════════════════════════════════════════════"
    echo " ⚡  Running Quick Pipeline (Phase 1-2-3)..."
    echo "═══════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    echo ""
    
    echo -e "${CYAN}Running Phase 1: Preprocessing...${NC}"
    python3 PHASE_1_QUICK_START.py
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Phase 1 failed${NC}"
        read -p "Press Enter to continue..."
        return
    fi
    
    echo ""
    echo -e "${CYAN}Running Phase 2: GAN Training...${NC}"
    python3 PHASE_2_QUICK_START.py
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Phase 2 failed${NC}"
        read -p "Press Enter to continue..."
        return
    fi
    
    echo ""
    echo -e "${CYAN}Running Phase 3: Temporal Analysis...${NC}"
    python3 PHASE_3_QUICK_START.py
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Phase 3 failed${NC}"
        read -p "Press Enter to continue..."
        return
    fi
    
    echo ""
    echo -e "${GREEN}✅ Pipeline completed successfully!${NC}"
    read -p "Press Enter to continue..."
}

# Run tests
run_tests() {
    clear
    echo -e "${BLUE}"
    echo "═══════════════════════════════════════════════════════════════"
    echo " 📊  Running Integration Tests..."
    echo "═══════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    echo ""
    
    if command_exists pytest; then
        python3 -m pytest test_docker_gui_integration.py -v
    else
        echo -e "${YELLOW}Installing pytest...${NC}"
        pip install pytest
        python3 -m pytest test_docker_gui_integration.py -v
    fi
    
    if [ $? -ne 0 ]; then
        echo ""
        echo -e "${YELLOW}⚠️  Some tests may have failed${NC}"
        read -p "Press Enter to continue..."
        return
    fi
    
    echo ""
    echo -e "${GREEN}✅ All tests completed!${NC}"
    read -p "Press Enter to continue..."
}

# Open documentation
open_docs() {
    clear
    echo -e "${BLUE}"
    echo "═══════════════════════════════════════════════════════════════"
    echo " 📖  Opening Documentation..."
    echo "═══════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    echo ""
    
    if [ -f "PROFESSIONAL_GUI_USER_GUIDE.md" ]; then
        echo -e "${GREEN}✅ Opening Professional GUI User Guide...${NC}"
        # Try common markdown viewers
        if command_exists open; then
            open "PROFESSIONAL_GUI_USER_GUIDE.md"
        elif command_exists xdg-open; then
            xdg-open "PROFESSIONAL_GUI_USER_GUIDE.md"
        else
            less "PROFESSIONAL_GUI_USER_GUIDE.md"
        fi
    else
        echo -e "${RED}❌ Documentation file not found${NC}"
    fi
    
    sleep 1
}

# Open settings
open_settings() {
    clear
    echo -e "${BLUE}"
    echo "═══════════════════════════════════════════════════════════════"
    echo " ⚙️  Settings and Configuration"
    echo "═══════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    echo ""
    
    echo "Select configuration file to edit:"
    echo ""
    echo "  ${CYAN}[1]${NC} requirements.txt (Dependencies)"
    echo "  ${CYAN}[2]${NC} projects.json (Saved Projects)"
    echo "  ${CYAN}[3]${NC} docker-compose.yml (Docker Compose)"
    echo "  ${CYAN}[4]${NC} Return to Main Menu"
    echo ""
    read -p "Enter your choice [1-4]: " config_choice
    
    case $config_choice in
        1)
            if [ -f "requirements.txt" ]; then
                ${EDITOR:-nano} requirements.txt
            fi
            ;;
        2)
            if [ -f "projects.json" ]; then
                ${EDITOR:-nano} projects.json
            fi
            ;;
        3)
            if [ -f "docker-compose.yml" ]; then
                ${EDITOR:-nano} docker-compose.yml
            fi
            ;;
        4)
            return
            ;;
    esac
}

# Open folder
open_folder() {
    clear
    echo -e "${BLUE}"
    echo "═══════════════════════════════════════════════════════════════"
    echo " 📁  Opening Project Folder..."
    echo "═══════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    echo ""
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open .
    elif command_exists xdg-open; then
        xdg-open .
    else
        ls -la
        echo ""
        read -p "Press Enter to continue..."
    fi
}

# System diagnostics
system_diagnostics() {
    clear
    echo -e "${BLUE}"
    echo "═══════════════════════════════════════════════════════════════"
    echo " 🔧  System Diagnostics"
    echo "═══════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    echo ""
    
    echo "Checking system requirements..."
    echo ""
    
    # Python check
    if command_exists python3; then
        echo -e "${GREEN}✅ Python installed:${NC}"
        python3 --version
    else
        echo -e "${RED}❌ Python not found${NC}"
    fi
    echo ""
    
    # Docker check
    if command_exists docker; then
        echo -e "${GREEN}✅ Docker installed:${NC}"
        docker --version
    else
        echo -e "${YELLOW}⚠️  Docker not found${NC}"
    fi
    echo ""
    
    # GPU check
    if command_exists nvidia-smi; then
        echo -e "${GREEN}✅ NVIDIA GPU detected:${NC}"
        nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    else
        echo -e "${YELLOW}⚠️  NVIDIA GPU not detected${NC}"
    fi
    echo ""
    
    # File check
    echo "Checking project files..."
    for file in \
        "shoreline_gan_professional.py" \
        "PHASE_1_QUICK_START.py" \
        "PHASE_2_QUICK_START.py" \
        "PHASE_3_QUICK_START.py" \
        "requirements.txt" \
        "Dockerfile"
    do
        if [ -f "$file" ]; then
            echo -e "${GREEN}✅ $file${NC}"
        else
            echo -e "${RED}❌ $file (missing)${NC}"
        fi
    done
    
    echo ""
    read -p "Press Enter to continue..."
}

# Exit menu
exit_menu() {
    clear
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                                                                ║"
    echo "║                  Thank you for using                           ║"
    echo "║        🌊 SHORELINE EXTRACTION GAN 🌊                         ║"
    echo "║                                                                ║"
    echo "║             Goodbye! Happy researching! 👋                    ║"
    echo "║                                                                ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    exit 0
}

# Make sure script has execute permissions
chmod +x "$0"

# Run main menu
show_menu
