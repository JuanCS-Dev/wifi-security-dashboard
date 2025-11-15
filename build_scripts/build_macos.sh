#!/bin/bash
##
# WiFi Security Education - macOS Build Script
#
# Creates .app bundle for macOS
#
# Note: This must run on macOS to create a valid .app bundle
#
# Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
# Date: 2025-11-15
##

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

APP_NAME="WiFi Security Game"
APP_BUNDLE="WiFiSecurityGame.app"
APP_VERSION="1.0.0"

echo "🍎 Building for macOS..."
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  Not running on macOS. Skipping macOS build."
    echo ""
    echo "To build for macOS, run this script on a Mac."
    echo ""
    exit 0
fi

# Build with PyInstaller (creates .app bundle automatically on macOS)
echo "1️⃣ Building macOS .app bundle with PyInstaller..."

pyinstaller --clean --noconfirm wifi_security_game.spec

# Check if build succeeded
if [ ! -d "dist/$APP_BUNDLE" ]; then
    echo "❌ PyInstaller build failed"
    exit 1
fi

echo "✅ .app bundle created"
echo ""

# Sign the app (if codesign certificate available)
echo "2️⃣ Code signing..."

if command -v codesign &> /dev/null; then
    # Check if we have a signing identity
    if security find-identity -v -p codesigning | grep -q "Developer ID"; then
        echo "   Signing app with Developer ID..."
        codesign --force --deep --sign "Developer ID Application" "dist/$APP_BUNDLE"
        echo "✅ App signed"
    else
        echo "⚠️  No Developer ID found. Skipping code signing."
        echo "   App will show 'unidentified developer' warning on first launch."

        # Ad-hoc signing (allows app to run locally)
        echo "   Applying ad-hoc signature..."
        codesign --force --deep --sign - "dist/$APP_BUNDLE"
    fi
else
    echo "⚠️  codesign not found. Skipping code signing."
fi

echo ""

# Create DMG installer
echo "3️⃣ Creating DMG installer..."

if command -v hdiutil &> /dev/null; then
    DMG_NAME="WiFiSecurityGame-${APP_VERSION}-macOS.dmg"
    DMG_TEMP="packaging/macos/dmg_temp"

    # Clean temp
    rm -rf "$DMG_TEMP"
    mkdir -p "$DMG_TEMP"

    # Copy app to temp
    cp -R "dist/$APP_BUNDLE" "$DMG_TEMP/"

    # Create symbolic link to Applications
    ln -s /Applications "$DMG_TEMP/Applications"

    # Create DMG
    hdiutil create -volname "$APP_NAME" \
        -srcfolder "$DMG_TEMP" \
        -ov -format UDZO \
        "dist/$DMG_NAME"

    # Clean temp
    rm -rf "$DMG_TEMP"

    echo "✅ DMG installer created: dist/$DMG_NAME"
else
    echo "⚠️  hdiutil not found. Skipping DMG creation."
fi

echo ""
echo "✅ macOS build complete!"
echo ""
echo "Created files:"
ls -lh "dist/$APP_BUNDLE" "dist/*.dmg" 2>/dev/null || echo "  (Check dist/ directory)"
