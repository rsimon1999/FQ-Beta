# Build & Packaging Architecture — AI Agent Specification

> **Audience:** AI Coding Agents, CI/CD Pipeline Engineers, and DevOps Maintainers.  
> **Purpose:** Detailed reference for binary packaging mechanics, PyInstaller spec customizations, dynamic library bundling, and GitHub Actions automated release workflows.

---

## 1. Packaging Architecture & Path Resolution

When frozen with PyInstaller, Python scripts run inside an isolated runtime container where `__file__` behaves differently.

### 1.1 Resource Path Invariant (`sys.frozen` & `sys._MEIPASS`)
* **Bundle Resources (Read-Only):**
  When frozen, bundled assets (`assets/`, `presets/`, `customtkinter/`) are unpacked into `sys._MEIPASS`.
  The codebase dynamically routes asset lookups via:
  ```python
  if getattr(sys, 'frozen', False):
      BUNDLE_ROOT = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
      DEFAULT_ASSETS_DIR = os.path.join(BUNDLE_ROOT, "assets")
  ```
* **User Data & Outputs (Read-Write):**
  Applications bundled into `/Applications` or read-only DMGs **cannot write to `.`**.  
  All session outputs and user settings are routed to the user's home folder:
  ```python
  USER_APP_DIR = os.path.expanduser("~/Documents/NeuroAcousticStudio")
  DEFAULT_OUTPUT_DIR = os.path.join(USER_APP_DIR, "output")
  DEFAULT_DATA_DIR = os.path.join(USER_APP_DIR, "data")
  ```

---

## 2. Spec Configuration Deep Dive (`neuroacoustic_studio.spec`)

### 2.1 Bundled Data Collections
```python
from PyInstaller.utils.hooks import collect_data_files

# Collect CustomTkinter JSON themes, fonts, and assets
customtkinter_datas = collect_data_files('customtkinter')

datas = [
    (os.path.join(PROJECT_ROOT, 'assets'), 'assets'),
    (os.path.join(PROJECT_ROOT, 'presets'), 'presets'),
    (os.path.join(PROJECT_ROOT, 'data'), 'data'),
] + customtkinter_datas
```

### 2.2 Hidden Imports Checklist
Ensure these modules are explicitly declared to prevent runtime `ImportError`:
* `customtkinter`, `darkdetect`, `PIL._tkinter_finder`
* `scipy.signal`, `scipy.signal.windows`
* `sounddevice`, `soundfile`, `cffi`
* `src.audio.*`, `src.ui.*`, `src.utils.*`
* `presets.easy_mode`

---

## 3. macOS DMG Creation Mechanics (`build_mac_dmg.sh`)

1. **Bundle Compilation:** PyInstaller compiles a structured `.app` directory (`dist/NeuroAcoustic Studio.app`).
2. **DMG Volume Generation:**
   * A staging directory is prepared containing `NeuroAcoustic Studio.app` and a symlink to `/Applications`.
   * Native macOS `hdiutil` creates a compressed (`UDZO`), read-only drag-and-drop disk image:
     ```bash
     hdiutil create -volname "NeuroAcoustic Studio" -srcfolder "$DMG_TEMP_DIR" -ov -format UDZO "dist/NeuroAcoustic_Studio_macOS.dmg"
     ```

---

## 4. GitHub Actions CI/CD Workflow Template

For automated cross-platform releases on Git tags (e.g. `v1.0.0`), agents can configure `.github/workflows/release.yml`:

```yaml
name: Build & Release Binaries

on:
  push:
    tags:
      - 'v*'

jobs:
  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pyinstaller -r requirements.txt
      - name: Build macOS DMG
        run: ./build_scripts/build_mac_dmg.sh
      - name: Upload macOS Artifact
        uses: actions/upload-artifact@v4
        with:
          name: macOS-DMG
          path: dist/NeuroAcoustic_Studio_macOS.dmg

  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pyinstaller -r requirements.txt
      - name: Build Windows Executable
        run: pyinstaller --clean build_scripts/neuroacoustic_studio.spec
      - name: Compress Windows Build
        run: Compress-Archive -Path dist/NeuroAcousticStudio -DestinationPath dist/NeuroAcoustic_Studio_Windows.zip
      - name: Upload Windows Artifact
        uses: actions/upload-artifact@v4
        with:
          name: Windows-ZIP
          path: dist/NeuroAcoustic_Studio_Windows.zip
```

---

## 5. Troubleshooting & Agent Packaging Gotchas

1. **Gatekeeper Quarantine (macOS):**
   * If testing locally and macOS blocks untrusted developer apps:
     ```bash
     xattr -cr "/Applications/NeuroAcoustic Studio.app"
     ```
2. **Missing Tkinter / Tcl dynamic libraries:**
   * Handled automatically by declaring `hiddenimports=['PIL._tkinter_finder']` and `customtkinter` data hooks.
3. **SoundDevice PortAudio backend:**
   * Dynamic C libraries bundled automatically via `cffi` hooks into `_sounddevice_data/`.
