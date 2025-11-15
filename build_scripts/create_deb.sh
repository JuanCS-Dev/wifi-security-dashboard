#!/bin/bash
##
# Create .deb package for Debian/Ubuntu
#
# Standard Debian package format.
#
# Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
# Date: 2025-11-15
##

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

APP_NAME="wifi-security-game"
APP_VERSION="1.0.0"
ARCH="amd64"
DEB_DIR="packaging/deb/${APP_NAME}_${APP_VERSION}_${ARCH}"

echo "📦 Creating .deb package..."

# Clean previous build
rm -rf "$DEB_DIR"
mkdir -p "$DEB_DIR/DEBIAN"
mkdir -p "$DEB_DIR/usr/bin"
mkdir -p "$DEB_DIR/usr/share/applications"
mkdir -p "$DEB_DIR/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$DEB_DIR/usr/share/doc/$APP_NAME"

# Copy executable
echo "  Copying executable..."
cp "dist/$APP_NAME" "$DEB_DIR/usr/bin/"
chmod +x "$DEB_DIR/usr/bin/$APP_NAME"

# Create control file
echo "  Creating control file..."
cat > "$DEB_DIR/DEBIAN/control" << EOF
Package: wifi-security-game
Version: ${APP_VERSION}
Section: education
Priority: optional
Architecture: ${ARCH}
Depends: python3 (>= 3.11), python3-pygame (>= 2.5.0)
Maintainer: Juan-Dev <noreply@example.com>
Description: WiFi Security Education Game
 Educational game teaching WiFi security concepts through interactive gameplay.
 .
 Features:
  * Interactive characters (Guardian, Professor Packet)
  * Educational scenarios about encryption, rogue APs, and packet sniffing
  * Real-time WiFi network monitoring
  * Age-appropriate content (9-16 years)
 .
 Soli Deo Gloria ✝️
EOF

# Create .desktop file
echo "  Creating .desktop file..."
cat > "$DEB_DIR/usr/share/applications/$APP_NAME.desktop" << 'EOF'
[Desktop Entry]
Type=Application
Name=WiFi Security Education
Comment=Educational game teaching WiFi security concepts
Exec=/usr/bin/wifi-security-game
Icon=wifi-security-game
Categories=Education;Game;Network;
Terminal=false
StartupNotify=true
Keywords=wifi;security;education;network;encryption;
EOF

# Create icon
echo "  Creating icon..."
cat > "$DEB_DIR/usr/share/icons/hicolor/256x256/apps/$APP_NAME.svg" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
  <rect width="256" height="256" fill="#2196F3"/>
  <text x="128" y="180" font-size="120" text-anchor="middle" fill="white">🛡️</text>
</svg>
EOF

# Create copyright file
echo "  Creating copyright..."
cat > "$DEB_DIR/usr/share/doc/$APP_NAME/copyright" << 'EOF'
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: WiFi Security Education
Upstream-Contact: Juan-Dev
Source: https://github.com/JuanCS-Dev/wifi-security-dashboard

Files: *
Copyright: 2025 Juan-Dev
License: MIT
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 .
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 .
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
 .
 Soli Deo Gloria ✝️
EOF

# Create changelog
echo "  Creating changelog..."
cat > "$DEB_DIR/usr/share/doc/$APP_NAME/changelog.gz" << 'EOF'
wifi-security-game (1.0.0) stable; urgency=medium

  * Initial release
  * Character system (Guardian, Professor Packet)
  * Scenario system (3 educational scenarios)
  * Threat system (Impostor, Eavesdropper)
  * Emoji-based visual assets
  * 77 unit tests (100% pass)
  * Performance: 62.22 FPS (103.7% of target)

 -- Juan-Dev <noreply@example.com>  Fri, 15 Nov 2025 12:00:00 +0000
EOF
gzip -9 "$DEB_DIR/usr/share/doc/$APP_NAME/changelog.gz"

# Set permissions
echo "  Setting permissions..."
chmod 755 "$DEB_DIR/DEBIAN"
chmod 644 "$DEB_DIR/DEBIAN/control"
find "$DEB_DIR/usr" -type d -exec chmod 755 {} \;
find "$DEB_DIR/usr" -type f -exec chmod 644 {} \;
chmod 755 "$DEB_DIR/usr/bin/$APP_NAME"

# Build .deb package
echo "  Building package..."
dpkg-deb --build --root-owner-group "$DEB_DIR" "dist/${APP_NAME}_${APP_VERSION}_${ARCH}.deb"

echo "✅ .deb package created: dist/${APP_NAME}_${APP_VERSION}_${ARCH}.deb"
