@echo off
REM ====================================================================
REM  Shoreline Extraction GAN - Dev Server Reopen Script
REM  Windows Batch - One-Click Dev Environment Restart
REM ====================================================================
REM  This script reopens your development server exactly where you
REM  left off, with all data and configurations intact.
REM ====================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     🐳 SHORELINE EXTRACTION GAN - DEV SERVER REOPEN 🐳        ║
echo ║                                                                ║
echo ║               Reopening Development Environment...            ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Docker is not installed or not running
    echo.
    echo Please:
    echo   1. Install Docker Desktop from https://www.docker.com/
    echo   2. Start Docker Desktop
    echo   3. Run this script again
    echo.
    pause
    exit /b 1
)

echo Checking for existing container...
echo.

REM Check if container exists and is running
docker ps --filter "name=shoreline_gan_gui" --format "{{.Status}}" >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ Container found and is running!
    echo.
    echo Attaching to container...
    timeout /t 2 >nul
    docker attach shoreline_gan_gui
    exit /b 0
)

REM Check if container exists but is stopped
docker ps -a --filter "name=shoreline_gan_gui" --format "{{.Status}}" >nul 2>&1
if !errorlevel! equ 0 (
    echo ⏸️  Container found (stopped). Restarting...
    echo.
    docker start shoreline_gan_gui
    echo.
    echo ✅ Container restarted! Attaching now...
    timeout /t 3 >nul
    docker attach shoreline_gan_gui
    exit /b 0
)

REM Container doesn't exist - create it
echo ⚠️  No existing container found. Creating new development environment...
echo.
echo This will:
echo   • Pull the latest shoreline-gan image
echo   • Create a new dev container
echo   • Mount your data and model_outputs directories
echo   • Enable GPU support (if available)
echo.
echo ⏳ Please wait (this may take 1-5 minutes on first run)...
echo.

docker run --gpus all -it ^
  --name shoreline_gan_gui ^
  -v "%cd%\data:/app/data" ^
  -v "%cd%\model_outputs:/app/model_outputs" ^
  -p 8000:8000 ^
  kanchoraboku22/shoreline-gan:latest

if errorlevel 1 (
    echo.
    echo ❌ Failed to start container
    echo.
    echo Troubleshooting:
    echo   1. Check Docker is running: docker ps
    echo   2. Check Docker logs: docker logs shoreline_gan_gui
    echo   3. Try removing old container: docker rm shoreline_gan_gui
    echo   4. Rebuild image: docker build -t shoreline_gan:latest .
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Development server reopened successfully!
echo.
pause
exit /b 0
