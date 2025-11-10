#!/bin/bash
# Dependency checker for WiFi Security Education Dashboard
# Validates all required dependencies before running
#
# Author: Juan-Dev - Soli Deo Gloria ✝️
# Date: 2025-11-10

set -e

echo "=================================="
echo "WiFi Security Dashboard v2.0"
echo "Dependency Checker"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Check Python version
echo "[1/5] Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
    echo -e "   ${GREEN}✓${NC} Python $PYTHON_VERSION (OK)"
else
    echo -e "   ${RED}✗${NC} Python $PYTHON_VERSION (need 3.10+)"
    ERRORS=$((ERRORS + 1))
fi

# Check required Python packages
echo ""
echo "[2/5] Checking Python packages..."

REQUIRED_PACKAGES=("rich" "psutil" "pytest" "pyyaml")

for package in "${REQUIRED_PACKAGES[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        VERSION=$(python3 -c "import $package; print(getattr($package, '__version__', 'unknown'))" 2>/dev/null)
        echo -e "   ${GREEN}✓${NC} $package ($VERSION)"
    else
        echo -e "   ${RED}✗${NC} $package (NOT INSTALLED)"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check optional packages
echo ""
echo "[3/5] Checking optional packages..."

OPTIONAL_PACKAGES=("scapy" "netifaces")

for package in "${OPTIONAL_PACKAGES[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        VERSION=$(python3 -c "import $package; print(getattr($package, '__version__', 'unknown'))" 2>/dev/null)
        echo -e "   ${GREEN}✓${NC} $package ($VERSION)"
    else
        echo -e "   ${YELLOW}⚠${NC} $package (optional, not installed)"
        WARNINGS=$((WARNINGS + 1))
    fi
done

# Check system commands
echo ""
echo "[4/5] Checking system commands..."

COMMANDS=("ip" "git")

for cmd in "${COMMANDS[@]}"; do
    if command -v $cmd &> /dev/null; then
        echo -e "   ${GREEN}✓${NC} $cmd"
    else
        echo -e "   ${RED}✗${NC} $cmd (NOT FOUND)"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check WiFi interfaces (optional)
echo ""
echo "[5/5] Checking WiFi interfaces..."

if ip link show 2>/dev/null | grep -q "wl"; then
    WIFI_IFACE=$(ip link show | grep "wl" | awk -F: '{print $2}' | tr -d ' ' | head -n1)
    echo -e "   ${GREEN}✓${NC} WiFi interface found: $WIFI_IFACE"
else
    echo -e "   ${YELLOW}⚠${NC} No WiFi interface found (will use mock mode)"
    WARNINGS=$((WARNINGS + 1))
fi

# Summary
echo ""
echo "=================================="
echo "SUMMARY"
echo "=================================="

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ All required dependencies OK${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠ $WARNINGS optional dependencies missing${NC}"
        echo ""
        echo "Dashboard will work in MOCK MODE (educational simulation)"
        echo "For REAL MODE, install: sudo apt install python3-scapy"
    fi
    echo ""
    echo "Ready to run:"
    echo "  python3 main_v2.py"
    exit 0
else
    echo -e "${RED}✗ $ERRORS required dependencies missing${NC}"
    echo ""
    echo "Install missing dependencies:"
    echo "  pip3 install -r requirements-v2.txt"
    exit 1
fi
