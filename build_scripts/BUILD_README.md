# NeuroAcoustic Sound Studio — Build & Packaging Guide

This directory contains standalone build scripts and PyInstaller configurations to package **NeuroAcoustic Sound Studio** as a native macOS Application (`.app` / `.dmg`) or Windows Executable (`.exe`).

---

## 📁 Directory Overview

* **`neuroacoustic_studio.spec`:** Universal PyInstaller configuration bundling CustomTkinter themes, NumPy, SciPy, SoundDevice, SoundFile, and all 11 ambient soundscape MP3s.
* **`build_mac_dmg.sh`:** Automated macOS builder that compiles the `.app` bundle and generates a drag-and-drop `.dmg` installer.
* **`build_windows_exe.bat`:** Windows batch builder that compiles the standalone executable folder.
* **`BUILD_AGENT_INFO.md`:** Architectural reference and CI/CD automation guide for AI coding agents.

---

## 🍏 Building for macOS (DMG Installer)

### Prerequisites:
* macOS 12+ (Monterey, Ventura, Sonoma, Sequoia)
* Python 3.10+
* Virtual environment or system Python with `requirements.txt` installed

### Build Command:
Run the build script from anywhere or project root:
```bash
./build_scripts/build_mac_dmg.sh
```

### Build Process:
1. Validates and installs dependencies (`pyinstaller`, `customtkinter`, `scipy`, etc.).
2. Cleans previous build artifacts in `build/` and `dist/`.
3. Runs PyInstaller with `neuroacoustic_studio.spec` to construct `dist/NeuroAcoustic Studio.app`.
4. Staged inside a temporary volume with a `/Applications` symlink.
5. Uses macOS native `hdiutil` to generate compressed image:
   ```
   dist/NeuroAcoustic_Studio_macOS.dmg
   ```

### Installing the DMG:
1. Double-click `dist/NeuroAcoustic_Studio_macOS.dmg`.
2. Drag **NeuroAcoustic Studio** into the **Applications** folder.
3. Launch from Spotlight or Launchpad.

---

## 🪟 Building for Windows (.exe)

### Prerequisites:
* Windows 10/11 (64-bit)
* Python 3.10+ with `requirements.txt` installed

### Build Command:
Execute the batch script in Command Prompt or PowerShell:
```cmd
build_scripts\build_windows_exe.bat
```

### Output:
* Standalone executable bundle: `dist\NeuroAcousticStudio\NeuroAcousticStudio.exe`
* All dependent dynamic libraries (`portaudio`, `libsndfile`) and assets are bundled in the directory.

---

## 📦 What is Bundled in the Package

| Component | Bundled Path | Description |
| :--- | :--- | :--- |
| **Ambient Assets** | `assets/*.mp3` | All 11 field recordings (Ocean, Rain, River, Thunder, etc.) |
| **Presets** | `presets/*.py` | All 27 multi-stage brainwave protocols |
| **CustomTkinter** | `customtkinter/` | JSON dark/light color themes, fonts, and UI assets |
| **Audio Drivers** | Dynamic Libs | SoundFile and SoundDevice / PortAudio backend drivers |

---

## 🧹 Cleaning Build Intermediates

To clean up intermediate `.o` / `.pyc` / `build/` directories:
```bash
rm -rf build/ dist/
```
Or run the workspace maintenance tool:
```bash
python3 scripts/maintenance.py --clean
```
