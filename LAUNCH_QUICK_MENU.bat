@echo off
REM ====================================================================
REM  Shoreline Extraction GAN - Professional GUI Quick Launcher
REM  Windows Batch Script
REM ====================================================================
REM  This script provides an interactive menu to launch various
REM  components of the Shoreline Extraction GAN system
REM ====================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

:menu
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║      🌊 SHORELINE EXTRACTION GAN - PROFESSIONAL GUI 🌊        ║
echo ║                                                                ║
echo ║           Coastal Erosion Monitoring Platform v2.0            ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Select Launch Option:
echo.
echo   [1] 🖥️  Launch Professional GUI (Desktop Application)
echo   [2] 🐳  Launch GUI via Docker (Containerized)
echo   [3] ⚡  Run Quick Pipeline (Phase 1-2-3)
echo   [4] 📊  Run Integration Tests
echo   [5] 📖  Open Documentation
echo   [6] ⚙️  Open Settings/Configuration
echo   [7] 📁  Open Project Folder
echo   [8] 🔧  System Diagnostics
echo   [9] ❌  Exit
echo.
set /p choice="Enter your choice [1-9]: "

if "%choice%"=="1" goto launch_gui
if "%choice%"=="2" goto launch_docker
if "%choice%"=="3" goto quick_pipeline
if "%choice%"=="4" goto tests
if "%choice%"=="5" goto docs
if "%choice%"=="6" goto settings
if "%choice%"=="7" goto folder
if "%choice%"=="8" goto diagnostics
if "%choice%"=="9" goto exit
echo Invalid choice. Please try again.
timeout /t 2 >nul
goto menu

:launch_gui
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  🖥️  Launching Professional GUI...
echo ═══════════════════════════════════════════════════════════════
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.11+ from https://www.python.org/
    echo Make sure to add Python to your PATH during installation
    echo.
    pause
    goto menu
)

REM Check if PyQt6 is installed
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PyQt6 not found. Installing dependencies...
    pip install --upgrade PyQt6 PyQt6-Charts matplotlib psutil pandas
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        goto menu
    )
)

echo Starting application...
echo.
python shoreline_gan_professional.py
if errorlevel 1 (
    echo.
    echo ❌ Error launching GUI. Check console output above.
    pause
)
goto menu

:launch_docker
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  🐳  Launching GUI via Docker...
echo ═══════════════════════════════════════════════════════════════
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Docker is not installed or not running
    echo.
    echo Please install Docker Desktop from https://www.docker.com/
    echo.
    pause
    goto menu
)

echo Starting Docker launcher...
echo.
call LAUNCH_DOCKER_GUI.bat
if errorlevel 1 (
    echo.
    echo ⚠️  Docker launcher returned an error
    pause
)
goto menu

:quick_pipeline
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  ⚡  Running Quick Pipeline (Phase 1-2-3)...
echo ═══════════════════════════════════════════════════════════════
echo.

python PHASE_1_QUICK_START.py
if errorlevel 1 (
    echo ❌ Phase 1 failed
    pause
    goto menu
)

python PHASE_2_QUICK_START.py
if errorlevel 1 (
    echo ❌ Phase 2 failed
    pause
    goto menu
)

python PHASE_3_QUICK_START.py
if errorlevel 1 (
    echo ❌ Phase 3 failed
    pause
    goto menu
)

echo.
echo ✅ Pipeline completed successfully!
pause
goto menu

:tests
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  📊  Running Integration Tests...
echo ═══════════════════════════════════════════════════════════════
echo.

python -m pytest test_docker_gui_integration.py -v
if errorlevel 1 (
    echo ⚠️  Some tests may have failed
    pause
    goto menu
)

echo.
echo ✅ All tests completed!
pause
goto menu

:docs
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  📖  Opening Documentation...
echo ═══════════════════════════════════════════════════════════════
echo.

if exist "PROFESSIONAL_GUI_USER_GUIDE.md" (
    start "" "PROFESSIONAL_GUI_USER_GUIDE.md"
    echo ✅ Opening Professional GUI User Guide...
) else (
    echo ❌ Documentation file not found
)

timeout /t 2 >nul
goto menu

:settings
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  ⚙️  Settings and Configuration
echo ═══════════════════════════════════════════════════════════════
echo.

echo Select configuration file to edit:
echo.
echo   [1] requirements.txt (Dependencies)
echo   [2] projects.json (Saved Projects)
echo   [3] Docker Compose (docker-compose.yml)
echo   [4] Return to Main Menu
echo.
set /p config_choice="Enter your choice [1-4]: "

if "%config_choice%"=="1" (
    if exist "requirements.txt" start "" notepad requirements.txt
) else if "%config_choice%"=="2" (
    if exist "projects.json" start "" notepad projects.json
) else if "%config_choice%"=="3" (
    if exist "docker-compose.yml" start "" notepad docker-compose.yml
) else if "%config_choice%"=="4" (
    goto menu
)

timeout /t 1 >nul
goto menu

:folder
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  📁  Opening Project Folder...
echo ═══════════════════════════════════════════════════════════════
echo.

explorer .
timeout /t 1 >nul
goto menu

:diagnostics
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  🔧  System Diagnostics
echo ═══════════════════════════════════════════════════════════════
echo.

echo Checking system requirements...
echo.

REM Python check
python --version
if errorlevel 1 (
    echo ❌ Python not found
) else (
    echo ✅ Python installed
)
echo.

REM Docker check
docker --version
if errorlevel 1 (
    echo ⚠️  Docker not found
) else (
    echo ✅ Docker installed
)
echo.

REM GPU check
where nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo ⚠️  NVIDIA GPU not detected
) else (
    echo ✅ NVIDIA GPU detected
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
)
echo.

REM File check
echo Checking project files...
for %%f in (
    "shoreline_gan_professional.py"
    "PHASE_1_QUICK_START.py"
    "PHASE_2_QUICK_START.py"
    "PHASE_3_QUICK_START.py"
    "requirements.txt"
    "Dockerfile"
) do (
    if exist "%%f" (
        echo ✅ %%f
    ) else (
        echo ❌ %%f (missing)
    )
)

echo.
pause
goto menu

:exit
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║                  Thank you for using                           ║
echo ║        🌊 SHORELINE EXTRACTION GAN 🌊                         ║
echo ║                                                                ║
echo ║             Goodbye! Happy researching! 👋                    ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
exit /b 0

REM Error handler
:error
cls
echo.
echo ❌ An error occurred. Returning to menu...
echo.
pause
goto menu
