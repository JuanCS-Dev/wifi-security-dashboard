#!/bin/bash
# Quick setup script for WiFi Security Education Dashboard
# Installs dependencies and verifies installation
#
# Author: Juan-Dev - Soli Deo Gloria ✝️
# Date: 2025-11-10

set -e

echo "=================================="
echo "WiFi Security Dashboard v2.0"
echo "Quick Setup"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Check Python
echo -e "${BLUE}[1/4]${NC} Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo "Install with: sudo apt install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "   ✓ Python $PYTHON_VERSION found"

# Step 2: Install pip if needed
echo ""
echo -e "${BLUE}[2/4]${NC} Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "Installing pip3..."
    sudo apt install python3-pip -y
fi
echo "   ✓ pip3 ready"

# Step 3: Install Python dependencies
echo ""
echo -e "${BLUE}[3/4]${NC} Installing Python dependencies..."

if [ -f "requirements-v2.txt" ]; then
    pip3 install -r requirements-v2.txt --user
    echo "   ✓ Dependencies installed"
else
    echo "⚠️  requirements-v2.txt not found, installing manually..."
    pip3 install rich psutil pytest pyyaml --user
    echo "   ✓ Core dependencies installed"
fi

# Step 4: Verify installation
echo ""
echo -e "${BLUE}[4/4]${NC} Verifying installation..."

if [ -f "scripts/check_dependencies.sh" ]; then
    bash scripts/check_dependencies.sh
else
    # Manual verification
    python3 -c "import rich, psutil, pytest, yaml" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "   ✓ All core packages verified"
    else
        echo "   ❌ Verification failed"
        exit 1
    fi
fi

# Success
echo ""
echo "=================================="
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "=================================="
echo ""
echo "Run the dashboard:"
echo "  python3 main_v2.py"
echo ""
echo "Run tests:"
echo "  python3 -m pytest tests/ -v"
echo ""
