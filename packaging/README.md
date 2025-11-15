# WiFi Security Education - Packaging

**Distribution packages for all platforms**

---

## 📦 Available Formats

### Linux
- **AppImage** - Universal Linux binary (runs everywhere)
- **.deb** - Debian/Ubuntu package

### Windows
- **.exe** - Windows installer with Inno Setup
- Standalone executable

### macOS
- **.app** - macOS application bundle
- **.dmg** - macOS disk image installer

---

## 🚀 Build Instructions

See **[BUILD_GUIDE.md](../docs/BUILD_GUIDE.md)** for complete build instructions.

**Quick start:**

```bash
# Install dependencies
pip install pyinstaller>=6.0.0

# Build for your platform
./build_scripts/build_all.sh
```

---

## 📂 Directory Structure

```
packaging/
├── appimage/       # AppImage build files
│   └── *.AppDir/   # Generated during build
├── deb/            # Debian package build files
│   └── wifi-security-game_*/  # Generated during build
├── windows/        # Windows installer files
│   └── installer.iss  # Inno Setup script
└── macos/          # macOS bundle files
    └── dmg_temp/   # Generated during build
```

---

## 🎯 Platform-Specific Notes

### Linux

**AppImage:**
- Self-contained, no installation needed
- Requires FUSE (usually pre-installed)
- Make executable: `chmod +x *.AppImage`

**.deb:**
- Debian/Ubuntu native package
- Install: `sudo dpkg -i *.deb`
- Uninstall: `sudo apt remove wifi-security-game`

### Windows

**Installer:**
- Built with Inno Setup
- Creates uninstaller automatically
- Requires Visual C++ redistributables (included)

**Standalone .exe:**
- Single file, no installation
- May trigger SmartScreen (click "More info" → "Run anyway")

### macOS

**.app:**
- Standard macOS application
- Code-signed if certificate available
- Gatekeeper: Right-click → Open on first launch

**.dmg:**
- Drag-and-drop installer
- Symbolic link to Applications folder included

---

## ✅ Testing Checklist

Before release, test each package:

- [ ] AppImage runs on Ubuntu, Fedora, Arch
- [ ] .deb installs on Ubuntu 22.04+
- [ ] .exe installs on Windows 10/11
- [ ] .app runs on macOS 10.14+
- [ ] All packages show correct version
- [ ] Menu/Desktop shortcuts work
- [ ] Uninstaller works (where applicable)

---

## 🔧 Customization

### Change Version

Edit version in:
- `wifi_security_game.spec`
- `build_scripts/build_linux.sh`
- `build_scripts/build_windows.sh`
- `build_scripts/build_macos.sh`
- `packaging/windows/installer.iss`

### Change Icon

Replace icon files:
- Windows: `packaging/windows/icon.ico`
- macOS: `packaging/macos/icon.icns`
- Linux: Use .svg or .png in build scripts

### Change Metadata

Edit desktop files and package control files in respective platform directories.

---

## 📝 License

All packaging scripts and configurations are part of the WiFi Security Education project.

**Copyright © 2025 Juan-Dev**
**License:** MIT

**Soli Deo Gloria** ✝️
