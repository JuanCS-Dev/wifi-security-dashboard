#!/bin/bash
##
# Create AppImage for Linux
#
# AppImage is a universal Linux package format that runs on any distribution.
#
# Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
# Date: 2025-11-15
##

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

APP_NAME="wifi-security-game"
APP_VERSION="1.0.0"
APPDIR="packaging/appimage/WiFiSecurityGame.AppDir"

echo "📦 Creating AppImage..."

# Clean previous build
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

# Copy executable
echo "  Copying executable..."
cp "dist/$APP_NAME" "$APPDIR/usr/bin/"

# Create .desktop file
echo "  Creating .desktop file..."
cat > "$APPDIR/usr/share/applications/$APP_NAME.desktop" << 'EOF'
[Desktop Entry]
Type=Application
Name=WiFi Security Education
Comment=Educational game teaching WiFi security concepts
Exec=wifi-security-game
Icon=wifi-security-game
Categories=Education;Game;
Terminal=false
StartupNotify=true
EOF

# Create AppRun script
echo "  Creating AppRun..."
cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
exec "${HERE}/usr/bin/wifi-security-game" "$@"
EOF
chmod +x "$APPDIR/AppRun"

# Create icon (placeholder - using emoji)
echo "  Creating icon..."
cat > "$APPDIR/usr/share/icons/hicolor/256x256/apps/$APP_NAME.svg" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" xmlns="http://www.w3.org/2000/svg">
  <rect width="256" height="256" fill="#2196F3"/>
  <text x="128" y="180" font-size="120" text-anchor="middle" fill="white">🛡️</text>
</svg>
EOF

# Symlink for AppImage standard
ln -sf "usr/share/applications/$APP_NAME.desktop" "$APPDIR/$APP_NAME.desktop"
ln -sf "usr/share/icons/hicolor/256x256/apps/$APP_NAME.svg" "$APPDIR/$APP_NAME.svg"

# Download appimagetool if not present
APPIMAGETOOL="packaging/appimage/appimagetool-x86_64.AppImage"
if [ ! -f "$APPIMAGETOOL" ]; then
    echo "  Downloading appimagetool..."
    wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage" \
        -O "$APPIMAGETOOL"
    chmod +x "$APPIMAGETOOL"
fi

# Build AppImage
echo "  Building AppImage..."
ARCH=x86_64 "$APPIMAGETOOL" "$APPDIR" "dist/WiFiSecurityGame-${APP_VERSION}-x86_64.AppImage"

echo "✅ AppImage created: dist/WiFiSecurityGame-${APP_VERSION}-x86_64.AppImage"
