# WiFi Security Education - Build Guide

**Complete guide for building distribution packages**

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Platform-Specific Builds](#platform-specific-builds)
4. [Distribution Formats](#distribution-formats)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### All Platforms

- **Python 3.11+**
- **pip** (Python package manager)
- **Git**

### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# Fedora/RHEL
sudo dnf install python3 python3-pip git

# Arch Linux
sudo pacman -S python python-pip git
```

### macOS

```bash
# Install Homebrew first (https://brew.sh)
brew install python git
```

### Windows

- Install Python from [python.org](https://www.python.org/downloads/)
- Install Git from [git-scm.com](https://git-scm.com/)

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/JuanCS-Dev/wifi-security-dashboard.git
cd wifi-security-dashboard
git checkout feature/gamification-v3-implementation
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller>=6.0.0
```

### 4. Build for Your Platform

```bash
chmod +x build_scripts/*.sh  # Linux/macOS only
./build_scripts/build_all.sh
```

**That's it!** Distribution files will be in `dist/`

---

## Platform-Specific Builds

### Linux

Creates **AppImage** and **.deb** packages.

```bash
./build_scripts/build_linux.sh
```

**Output:**
- `dist/WiFiSecurityGame-1.0.0-x86_64.AppImage` (universal Linux binary)
- `dist/wifi-security-game_1.0.0_amd64.deb` (Debian/Ubuntu package)

**Install:**

```bash
# AppImage (run anywhere)
chmod +x dist/WiFiSecurityGame-1.0.0-x86_64.AppImage
./dist/WiFiSecurityGame-1.0.0-x86_64.AppImage

# .deb (Debian/Ubuntu)
sudo dpkg -i dist/wifi-security-game_1.0.0_amd64.deb
wifi-security-game
```

---

### macOS

Creates **.app bundle** and **.dmg** installer.

```bash
./build_scripts/build_macos.sh
```

**Output:**
- `dist/WiFiSecurityGame.app` (macOS application)
- `dist/WiFiSecurityGame-1.0.0-macOS.dmg` (installer)

**Install:**

1. Open `.dmg` file
2. Drag `WiFi Security Game.app` to Applications folder
3. Launch from Applications

**Note:** First launch may show "unidentified developer" warning. Right-click → Open to bypass.

---

### Windows

Creates **.exe** standalone and installer.

```bash
./build_scripts/build_windows.sh
```

**Output:**
- `dist/WiFiSecurityGame.exe` (standalone executable)
- `dist/WiFiSecurityGame-1.0.0-Windows-Setup.exe` (installer)

**Install:**

1. Run `WiFiSecurityGame-1.0.0-Windows-Setup.exe`
2. Follow installer wizard
3. Launch from Start Menu or Desktop

**Note:** Windows Defender may show SmartScreen warning for unsigned apps. Click "More info" → "Run anyway"

---

## Distribution Formats

### AppImage (Linux)

**Pros:**
- ✅ Runs on any Linux distribution
- ✅ No installation required
- ✅ Self-contained (includes all dependencies)
- ✅ Portable (run from USB stick)

**Cons:**
- ⚠️ Larger file size (~50-100 MB)
- ⚠️ May need manual executable permissions

**Use case:** Universal Linux distribution

---

### .deb Package (Debian/Ubuntu)

**Pros:**
- ✅ Native package format
- ✅ Integrates with system package manager
- ✅ Automatic dependency resolution
- ✅ Menu integration
- ✅ Easy to install/uninstall

**Cons:**
- ⚠️ Debian/Ubuntu only
- ⚠️ Requires sudo for installation

**Use case:** Debian/Ubuntu users who prefer native packages

---

### .exe (Windows)

**Pros:**
- ✅ Native Windows executable
- ✅ Familiar installation process
- ✅ Start Menu integration
- ✅ Uninstaller included

**Cons:**
- ⚠️ SmartScreen warnings (unsigned)
- ⚠️ Antivirus false positives possible

**Use case:** Windows users

---

### .app / .dmg (macOS)

**Pros:**
- ✅ Native macOS application
- ✅ Drag-and-drop installation
- ✅ Launchpad integration
- ✅ Retina-ready

**Cons:**
- ⚠️ Gatekeeper warnings (unsigned)
- ⚠️ Requires macOS 10.14+

**Use case:** macOS users

---

## Build Scripts Reference

### build_all.sh

Master build script. Detects platform and runs appropriate builder.

```bash
./build_scripts/build_all.sh
```

### build_linux.sh

Builds AppImage and .deb for Linux.

```bash
./build_scripts/build_linux.sh
```

### build_windows.sh

Builds .exe for Windows (requires Wine for cross-compile).

```bash
./build_scripts/build_windows.sh
```

### build_macos.sh

Builds .app and .dmg for macOS (must run on macOS).

```bash
./build_scripts/build_macos.sh
```

---

## Troubleshooting

### "PyInstaller not found"

```bash
pip install pyinstaller>=6.0.0
```

### "Permission denied" (Linux/macOS)

```bash
chmod +x build_scripts/*.sh
```

### AppImage won't run

```bash
chmod +x dist/*.AppImage
```

### macOS "unidentified developer" warning

1. Right-click the app
2. Select "Open"
3. Click "Open" in dialog

### Windows SmartScreen warning

1. Click "More info"
2. Click "Run anyway"

### Build fails with import errors

```bash
# Clean previous builds
rm -rf build/ dist/

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Rebuild
./build_scripts/build_all.sh
```

### Large file size

This is normal for PyInstaller bundles. They include:
- Python interpreter
- All dependencies (Pygame, etc.)
- Game assets

Typical sizes:
- Linux AppImage: ~80 MB
- Windows .exe: ~50 MB
- macOS .app: ~60 MB

---

## Advanced Options

### Custom Icon

Replace icon files:
- `packaging/windows/icon.ico` (Windows)
- `packaging/macos/icon.icns` (macOS)
- `packaging/linux/icon.png` (Linux)

Rebuild after changing icons.

### Signing (macOS/Windows)

**macOS:**
```bash
# Requires Apple Developer account
codesign --force --deep --sign "Developer ID Application: Your Name" dist/WiFiSecurityGame.app
```

**Windows:**
```bash
# Requires code signing certificate
signtool sign /f certificate.pfx /p password dist/WiFiSecurityGame.exe
```

### Custom Version

Edit version in:
- `wifi_security_game.spec` (PyInstaller)
- `build_scripts/*.sh` (all build scripts)
- `packaging/windows/installer.iss` (Windows installer)

---

## CI/CD Integration

### GitHub Actions

See `.github/workflows/build.yml` for automated builds on:
- Push to main
- Pull requests
- Release tags

### GitLab CI

See `.gitlab-ci.yml` for automated builds.

---

## File Structure

```
wifi_security_education/
├── build_scripts/           # Build automation
│   ├── build_all.sh        # Master builder
│   ├── build_linux.sh      # Linux builder
│   ├── build_windows.sh    # Windows builder
│   ├── build_macos.sh      # macOS builder
│   ├── create_appimage.sh  # AppImage creator
│   └── create_deb.sh       # .deb creator
├── packaging/              # Platform-specific files
│   ├── appimage/           # AppImage assets
│   ├── deb/                # Debian package files
│   ├── windows/            # Windows installer config
│   └── macos/              # macOS bundle assets
├── dist/                   # Build output
├── wifi_security_game.py   # Entry point
└── wifi_security_game.spec # PyInstaller config
```

---

## Support

**Issues:** https://github.com/JuanCS-Dev/wifi-security-dashboard/issues
**Docs:** https://github.com/JuanCS-Dev/wifi-security-dashboard/wiki

---

**Soli Deo Gloria** ✝️
