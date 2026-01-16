#!/bin/bash
# Shoreline Extraction GAN - Docker Entrypoint with GUI Launch

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}   Shoreline Extraction GAN - Docker${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Step 1: Check if DISPLAY is set for GUI
if [ -z "$DISPLAY" ]; then
    echo -e "${YELLOW}⚠ Warning: DISPLAY not set. Launching in headless mode.${NC}"
    echo "To enable GUI, restart with X11 forwarding enabled."
    GUI_ENABLED=false
else
    echo -e "${GREEN}✓ DISPLAY=$DISPLAY - GUI enabled${NC}"
    GUI_ENABLED=true
fi

echo ""

# Step 2: Verify data directories
if [ -d "/app/data" ]; then
    echo -e "${GREEN}✓ Data directory found${NC}"
    ls -lah /app/data | head -5
else
    echo -e "${YELLOW}⚠ Data directory not found${NC}"
fi

if [ -d "/app/model_outputs" ]; then
    echo -e "${GREEN}✓ Model outputs directory found${NC}"
    ls -lah /app/model_outputs | head -5
else
    echo -e "${YELLOW}⚠ Model outputs directory not found${NC}"
fi

echo ""

# Step 3: Activate conda environment (if using conda)
if [ -f "/opt/miniconda3/bin/activate" ]; then
    echo -e "${BLUE}Activating conda environment...${NC}"
    source /opt/miniconda3/bin/activate shoreline_gan || true
else
    echo -e "${YELLOW}Conda not found. Using system Python.${NC}"
fi

echo ""

# Step 4: Launch GUI if enabled
if [ "$GUI_ENABLED" = true ]; then
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}   Launching PyQt6 GUI...${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    # Check which GUI is available
    if [ -f "shoreline_gui_advanced.py" ]; then
        echo -e "${GREEN}Launching Advanced Dashboard (shoreline_gui_advanced.py)${NC}"
        python3 shoreline_gui_advanced.py
    elif [ -f "shoreline_gui_pipeline.py" ]; then
        echo -e "${GREEN}Launching Pipeline Executor (shoreline_gui_pipeline.py)${NC}"
        python3 shoreline_gui_pipeline.py
    elif [ -f "shoreline_gui.py" ]; then
        echo -e "${GREEN}Launching Standalone Dashboard (shoreline_gui.py)${NC}"
        python3 shoreline_gui.py
    else
        echo -e "${YELLOW}No GUI application found. Please ensure shoreline_gui*.py is in the project root.${NC}"
        echo "Available Python files:"
        ls -la *.py 2>/dev/null | head -10 || echo "No Python files found"
    fi
else
    # Headless mode: start interactive shell
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}   Launching Interactive Shell${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${GREEN}You can now:${NC}"
    echo "  • Run: python3 PHASE_1_QUICK_START.py"
    echo "  • Run: python3 PHASE_2_QUICK_START.py"
    echo "  • Run: python3 PHASE_3_QUICK_START.py"
    echo "  • Launch GUI: python3 shoreline_gui_advanced.py (requires X11)"
    echo "  • Exit: Type 'exit' and press Enter"
    echo ""
    
    # Start interactive bash shell
    /bin/bash
fi

echo ""
echo -e "${BLUE}Container exiting. Outputs saved to /app/model_outputs/${NC}"
