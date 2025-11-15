#!/bin/bash
##
# WiFi Security Education - Linux Build Script
#
# Creates:
# 1. AppImage (universal Linux binary)
# 2. .deb package (Debian/Ubuntu)
#
# Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
# Date: 2025-11-15
##

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

APP_NAME="wifi-security-game"
APP_VERSION="1.0.0"
APP_DISPLAY_NAME="WiFi Security Education"

echo "🐧 Building for Linux..."
echo ""

# Step 1: Build with PyInstaller
echo "1️⃣ Building executable with PyInstaller..."
pyinstaller --clean --noconfirm wifi_security_game.spec

# Check if build succeeded
if [ ! -f "dist/wifi-security-game" ]; then
    echo "❌ PyInstaller build failed"
    exit 1
fi

echo "✅ PyInstaller build complete"
echo ""

# Step 2: Create AppImage
echo "2️⃣ Creating AppImage..."
./build_scripts/create_appimage.sh

echo ""

# Step 3: Create .deb package
echo "3️⃣ Creating .deb package..."
./build_scripts/create_deb.sh

echo ""
echo "✅ Linux builds complete!"
echo ""
echo "Created files:"
ls -lh dist/*.AppImage dist/*.deb 2>/dev/null || echo "  (Check dist/ directory)"
