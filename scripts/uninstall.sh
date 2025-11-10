#!/bin/bash
# WiFi Security Education Dashboard - Uninstall Script
# Removes system-wide installation created by install.sh

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
INSTALL_DIR="/opt/wifi-dashboard"
SERVICE_NAME="wifi-dashboard"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

echo -e "${YELLOW}WiFi Security Education Dashboard - Uninstall${NC}"
echo "================================================"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Error: This script must be run as root (use sudo)${NC}"
    exit 1
fi

# Check if installation exists
if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}Warning: Installation directory $INSTALL_DIR not found.${NC}"
    echo -e "${YELLOW}Dashboard may not be installed system-wide.${NC}"
fi

echo -e "\n${YELLOW}This will remove:${NC}"
echo "  - Dashboard files: $INSTALL_DIR"
echo "  - Systemd service: $SERVICE_FILE"
echo "  - Service will be stopped and disabled"
echo ""
read -p "$(echo -e ${YELLOW}Continue with uninstall? [y/N]: ${NC})" -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}Uninstall cancelled.${NC}"
    exit 0
fi

# Stop service if running
echo -e "\n${YELLOW}[1/4] Stopping service...${NC}"
if systemctl is-active --quiet $SERVICE_NAME; then
    systemctl stop $SERVICE_NAME
    echo -e "${GREEN}✓ Service stopped${NC}"
else
    echo -e "${YELLOW}Service not running${NC}"
fi

# Disable service
echo -e "\n${YELLOW}[2/4] Disabling service...${NC}"
if systemctl is-enabled --quiet $SERVICE_NAME; then
    systemctl disable $SERVICE_NAME
    echo -e "${GREEN}✓ Service disabled${NC}"
else
    echo -e "${YELLOW}Service not enabled${NC}"
fi

# Remove service file
echo -e "\n${YELLOW}[3/4] Removing service file...${NC}"
if [ -f "$SERVICE_FILE" ]; then
    rm -f $SERVICE_FILE
    systemctl daemon-reload
    echo -e "${GREEN}✓ Service file removed${NC}"
else
    echo -e "${YELLOW}Service file not found${NC}"
fi

# Remove installation directory
echo -e "\n${YELLOW}[4/4] Removing installation files...${NC}"
if [ -d "$INSTALL_DIR" ]; then
    rm -rf $INSTALL_DIR
    echo -e "${GREEN}✓ Installation directory removed${NC}"
else
    echo -e "${YELLOW}Installation directory not found${NC}"
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Uninstall Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Note:${NC} Python dependencies (rich, psutil, etc.) were NOT removed."
echo -e "To remove them manually:"
echo -e "  ${YELLOW}pip3 uninstall rich psutil pytest pytest-cov pyyaml${NC}"
echo ""
echo -e "${GREEN}Soli Deo Gloria ✝️${NC}"
