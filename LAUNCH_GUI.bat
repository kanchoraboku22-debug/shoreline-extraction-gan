@echo off
REM Shoreline Extraction GAN - GUI Launcher for Windows
REM Non-technical users: Just double-click this file to launch the GUI!

title Shoreline Extraction GAN - GUI Launcher

echo.
echo ================================================================================
echo   SHORELINE EXTRACTION GAN - DESKTOP APPLICATION
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please download Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✓ Python found

REM Check if PyQt6 is installed, if not, install it
echo.
echo Checking PyQt6 installation...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo PyQt6 not found. Installing...
    python -m pip install PyQt6 matplotlib --quiet
    if errorlevel 1 (
        echo ERROR: Failed to install PyQt6
        echo Please run: pip install PyQt6 matplotlib
        pause
        exit /b 1
    )
    echo ✓ PyQt6 installed successfully
)

echo ✓ PyQt6 is installed

echo.
echo ================================================================================
echo SELECT GUI APPLICATION
echo ================================================================================
echo.
echo 1. ADVANCED DASHBOARD (Recommended) - Full features with live charts
echo 2. PIPELINE EXECUTOR - Execute complete workflow step-by-step
echo 3. STANDALONE DASHBOARD - Simple desktop interface
echo 4. HTML MOCKUP - Browser-based prototype
echo 0. EXIT
echo.

set /p choice="Choose an option (0-4): "

if "%choice%"=="1" (
    echo.
    echo Launching Advanced Dashboard...
    python shoreline_gui_advanced.py
) else if "%choice%"=="2" (
    echo.
    echo Launching Pipeline Executor...
    python shoreline_gui_pipeline.py
) else if "%choice%"=="3" (
    echo.
    echo Launching Standalone Dashboard...
    python shoreline_gui.py
) else if "%choice%"=="4" (
    echo.
    echo Opening HTML Prototype in browser...
    start gui_prototype.html
) else if "%choice%"=="0" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid choice. Exiting...
    exit /b 1
)

pause
