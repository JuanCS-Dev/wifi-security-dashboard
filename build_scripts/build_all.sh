#!/bin/bash
##
# WiFi Security Education - Master Build Script
#
# Builds all distribution formats:
# - AppImage (Linux)
# - .deb (Debian/Ubuntu)
# - .exe (Windows via Wine/cross-compile)
# - .app (macOS)
#
# Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
# Date: 2025-11-15
##

set -e  # Exit on error

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "🎮 WiFi Security Education - Master Build Script"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📋 Checking Python version..."
python3 --version || { echo -e "${RED}❌ Python 3 not found${NC}"; exit 1; }

# Check if virtualenv exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
fi

# Activate virtualenv
source venv/bin/activate

# Install/upgrade build dependencies
echo ""
echo "📦 Installing build dependencies..."
pip install --upgrade pip setuptools wheel
pip install pyinstaller>=6.0.0
pip install -r requirements.txt

# Detect platform
PLATFORM="$(uname -s)"
echo ""
echo "🖥️  Detected platform: $PLATFORM"

# Build based on platform
case "$PLATFORM" in
    Linux*)
        echo ""
        echo -e "${GREEN}🐧 Building for Linux...${NC}"
        ./build_scripts/build_linux.sh
        ;;
    Darwin*)
        echo ""
        echo -e "${GREEN}🍎 Building for macOS...${NC}"
        ./build_scripts/build_macos.sh
        ;;
    MINGW*|MSYS*|CYGWIN*)
        echo ""
        echo -e "${GREEN}🪟 Building for Windows...${NC}"
        ./build_scripts/build_windows.sh
        ;;
    *)
        echo -e "${RED}❌ Unsupported platform: $PLATFORM${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Build complete!${NC}"
echo ""
echo "📦 Distribution files created in: dist/"
echo ""
echo "✝️ Soli Deo Gloria"
