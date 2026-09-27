@echo off
REM ==============================================================================
REM NeuroAcoustic Sound Studio — Windows Executable Build Script
REM ==============================================================================

echo ==================================================================
echo  WINDOWS EXE BUILDER — NEUROACOUSTIC SOUND STUDIO
echo ==================================================================

REM Navigate to project root
cd /d "%~dp0\.."

echo [1/3] Verifying dependencies...
python -m pip install -q pyinstaller -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    exit /b %errorlevel%
)

echo [2/3] Cleaning previous builds...
if exist "dist\NeuroAcousticStudio" rmdir /s /q "dist\NeuroAcousticStudio"
if exist "build" rmdir /s /q "build"

echo [3/3] Compiling Windows Executable with PyInstaller...
pyinstaller --clean build_scripts\neuroacoustic_studio.spec

if errorlevel 1 (
    echo [ERROR] PyInstaller compilation failed!
    exit /b %errorlevel%
)

echo ==================================================================
echo  BUILD COMPLETE!
echo  Output directory: dist\NeuroAcousticStudio\
echo  Launch binary: dist\NeuroAcousticStudio\NeuroAcousticStudio.exe
echo ==================================================================
