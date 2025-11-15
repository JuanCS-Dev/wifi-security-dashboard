#!/bin/bash
##
# WiFi Security Education - Windows Build Script
#
# Creates .exe installer for Windows using PyInstaller
#
# Note: This script can run on Linux using Wine for cross-compilation,
# or natively on Windows using Git Bash/MSYS2.
#
# Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
# Date: 2025-11-15
##

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

APP_NAME="wifi-security-game"
APP_VERSION="1.0.0"

echo "🪟 Building for Windows..."
echo ""

# Check if running on Windows or Linux
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Native Windows build
    echo "📍 Detected native Windows environment"
    PYTHON_CMD="python"
else
    # Linux cross-compile (requires Wine)
    echo "📍 Detected Linux environment (cross-compiling with Wine)"
    PYTHON_CMD="wine python"

    # Check if Wine is installed
    if ! command -v wine &> /dev/null; then
        echo "⚠️  Wine not installed. Installing Wine..."
        echo "   On Ubuntu/Debian: sudo apt install wine wine64"
        echo ""
        echo "Skipping Windows build for now..."
        echo "To build for Windows, either:"
        echo "  1. Install Wine and Python for Windows"
        echo "  2. Run this script on a Windows machine"
        echo ""
        exit 0
    fi
fi

# Build with PyInstaller
echo "1️⃣ Building Windows executable with PyInstaller..."

# PyInstaller for Windows (creates single .exe)
$PYTHON_CMD -m PyInstaller \
    --clean \
    --noconfirm \
    --onefile \
    --windowed \
    --name "WiFiSecurityGame" \
    --add-data "src:src" \
    wifi_security_game.py

# Check if build succeeded
if [ ! -f "dist/WiFiSecurityGame.exe" ]; then
    echo "❌ PyInstaller build failed"
    exit 1
fi

echo "✅ Windows executable created"
echo ""

# Create installer using Inno Setup (if available)
echo "2️⃣ Creating Windows installer..."

if command -v iscc &> /dev/null || command -v wine &> /dev/null; then
    ./build_scripts/create_windows_installer.sh
else
    echo "⚠️  Inno Setup not found. Skipping installer creation."
    echo "   Standalone .exe is available in dist/"
fi

echo ""
echo "✅ Windows build complete!"
echo ""
echo "Created files:"
ls -lh dist/*.exe 2>/dev/null || echo "  (Check dist/ directory)"
