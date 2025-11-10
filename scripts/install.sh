#!/bin/bash
# WiFi Security Education Dashboard - System-wide Installation Script
# Installs dashboard to /opt/ with systemd service for auto-start

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
INSTALL_DIR="/opt/wifi-dashboard"
SERVICE_NAME="wifi-dashboard"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
CURRENT_USER=$(logname || echo $SUDO_USER)

echo -e "${GREEN}WiFi Security Education Dashboard - System Installation${NC}"
echo "========================================================"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Error: This script must be run as root (use sudo)${NC}"
    exit 1
fi

# Check Python version
echo -e "\n${YELLOW}[1/6] Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 not found. Please install Python 3.10+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"

# Create installation directory
echo -e "\n${YELLOW}[2/6] Creating installation directory...${NC}"
mkdir -p $INSTALL_DIR
echo -e "${GREEN}✓ Created $INSTALL_DIR${NC}"

# Copy files
echo -e "\n${YELLOW}[3/6] Copying dashboard files...${NC}"
cp -r src/ $INSTALL_DIR/
cp -r config/ $INSTALL_DIR/
cp main_v2.py $INSTALL_DIR/
cp requirements-v2.txt $INSTALL_DIR/
cp VERSION $INSTALL_DIR/
echo -e "${GREEN}✓ Files copied${NC}"

# Install Python dependencies
echo -e "\n${YELLOW}[4/6] Installing Python dependencies...${NC}"
pip3 install -r $INSTALL_DIR/requirements-v2.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create systemd service
echo -e "\n${YELLOW}[5/6] Creating systemd service...${NC}"
cat > $SERVICE_FILE << EOF
[Unit]
Description=WiFi Security Education Dashboard
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$INSTALL_DIR
ExecStart=/usr/bin/python3 $INSTALL_DIR/main_v2.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✓ Service file created: $SERVICE_FILE${NC}"

# Enable and start service
echo -e "\n${YELLOW}[6/6] Enabling and starting service...${NC}"
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME
echo -e "${GREEN}✓ Service enabled and started${NC}"

# Check service status
echo -e "\n${YELLOW}Service Status:${NC}"
systemctl status $SERVICE_NAME --no-pager

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Dashboard installed to: ${GREEN}$INSTALL_DIR${NC}"
echo -e "Service name: ${GREEN}$SERVICE_NAME${NC}"
echo ""
echo -e "Useful commands:"
echo -e "  - View logs:       ${YELLOW}sudo journalctl -u $SERVICE_NAME -f${NC}"
echo -e "  - Restart service: ${YELLOW}sudo systemctl restart $SERVICE_NAME${NC}"
echo -e "  - Stop service:    ${YELLOW}sudo systemctl stop $SERVICE_NAME${NC}"
echo -e "  - Disable service: ${YELLOW}sudo systemctl disable $SERVICE_NAME${NC}"
echo ""
echo -e "${GREEN}Soli Deo Gloria ✝️${NC}"
