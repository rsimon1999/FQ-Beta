#!/bin/bash
# ==============================================================================
# NeuroAcoustic Sound Studio — macOS App & DMG Build Script
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DIST_DIR="$PROJECT_ROOT/dist"
BUILD_DIR="$PROJECT_ROOT/build"
APP_NAME="NeuroAcoustic Studio"
DMG_NAME="NeuroAcoustic_Studio_macOS.dmg"

echo "=================================================================="
echo " 🍏 BUILDING NEUROACOUSTIC SOUND STUDIO FOR MACOS"
echo "=================================================================="
echo "Project Root: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

# 1. Ensure Dependencies
echo ""
echo "[1/4] Checking environment dependencies..."
python3 -m pip install -q pyinstaller -r requirements.txt

# 2. Clean Previous Builds
echo ""
echo "[2/4] Cleaning previous build artifacts..."
rm -rf "$BUILD_DIR" "$DIST_DIR/$APP_NAME.app" "$DIST_DIR/$DMG_NAME" "$DIST_DIR/dmg_temp"

# 3. Build .app Bundle with PyInstaller
echo ""
echo "[3/4] Compiling macOS .app bundle with PyInstaller..."
pyinstaller --clean "$SCRIPT_DIR/neuroacoustic_studio.spec"

APP_PATH="$DIST_DIR/$APP_NAME.app"
if [ ! -d "$APP_PATH" ]; then
    echo "❌ Error: App bundle not found at $APP_PATH"
    exit 1
fi
echo "✅ App bundle compiled successfully at: $APP_PATH"

# 4. Create DMG Installer
echo ""
echo "[4/4] Creating macOS DMG disk image with Applications shortcut..."
DMG_TEMP_DIR="$DIST_DIR/dmg_temp"
mkdir -p "$DMG_TEMP_DIR"

# Copy App bundle
cp -R "$APP_PATH" "$DMG_TEMP_DIR/"

# Create symlink to /Applications for drag-and-drop installation
ln -s /Applications "$DMG_TEMP_DIR/Applications"

# Generate DMG using hdiutil
FINAL_DMG="$DIST_DIR/$DMG_NAME"
rm -f "$FINAL_DMG"

hdiutil create \
    -volname "$APP_NAME" \
    -srcfolder "$DMG_TEMP_DIR" \
    -ov \
    -format UDZO \
    "$FINAL_DMG"

# Cleanup staging directory
rm -rf "$DMG_TEMP_DIR"

echo ""
echo "=================================================================="
echo "🎉 BUILD SUCCESSFUL!"
echo "📦 Output DMG: $FINAL_DMG"
echo "📏 DMG Size: $(du -sh "$FINAL_DMG" | awk '{print $1}')"
echo "=================================================================="
