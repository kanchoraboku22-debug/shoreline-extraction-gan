#!/bin/bash
# Shoreline Extraction GAN - GUI Launcher for macOS/Linux
# Non-technical users: Just run this script to launch the GUI!

echo ""
echo "================================================================================"
echo "   SHORELINE EXTRACTION GAN - DESKTOP APPLICATION"
echo "================================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo ""
    echo "Please install Python 3 from: https://www.python.org/downloads/"
    echo "Or use your package manager:"
    echo "  Ubuntu/Debian: sudo apt install python3"
    echo "  macOS: brew install python3"
    echo ""
    exit 1
fi

echo "✓ Python found"

# Check if PyQt6 is installed
echo ""
echo "Checking PyQt6 installation..."
python3 -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "PyQt6 not found. Installing..."
    python3 -m pip install PyQt6 matplotlib --quiet
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install PyQt6"
        echo "Please run: pip install PyQt6 matplotlib"
        exit 1
    fi
    echo "✓ PyQt6 installed successfully"
fi

echo "✓ PyQt6 is installed"

echo ""
echo "================================================================================"
echo "SELECT GUI APPLICATION"
echo "================================================================================"
echo ""
echo "1. ADVANCED DASHBOARD (Recommended) - Full features with live charts"
echo "2. PIPELINE EXECUTOR - Execute complete workflow step-by-step"
echo "3. STANDALONE DASHBOARD - Simple desktop interface"
echo "4. HTML MOCKUP - Browser-based prototype"
echo "0. EXIT"
echo ""

read -p "Choose an option (0-4): " choice

case $choice in
    1)
        echo ""
        echo "Launching Advanced Dashboard..."
        python3 shoreline_gui_advanced.py
        ;;
    2)
        echo ""
        echo "Launching Pipeline Executor..."
        python3 shoreline_gui_pipeline.py
        ;;
    3)
        echo ""
        echo "Launching Standalone Dashboard..."
        python3 shoreline_gui.py
        ;;
    4)
        echo ""
        echo "Opening HTML Prototype in browser..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
            open gui_prototype.html
        else
            xdg-open gui_prototype.html
        fi
        ;;
    0)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac
