# WiFi Security Education - Installation Guide

**Complete installation instructions for all platforms**

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Version: v1.0.0
Date: 2025-11-15

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Windows Installation](#windows-installation)
3. [macOS Installation](#macos-installation)
4. [Linux Installation](#linux-installation)
5. [Troubleshooting](#troubleshooting)
6. [Uninstallation](#uninstallation)

---

## 💻 System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 10, macOS 10.14, or Linux (2015+) |
| **CPU** | Dual-core 2.0 GHz or better |
| **RAM** | 4 GB |
| **Storage** | 200 MB free space |
| **Display** | 1280x720 resolution |
| **Python** | 3.11+ (included in installers) |

### Recommended Requirements

| Component | Recommendation |
|-----------|----------------|
| **OS** | Windows 11, macOS 12+, or Ubuntu 22.04+ |
| **CPU** | Quad-core 2.5 GHz or better |
| **RAM** | 8 GB |
| **Storage** | 500 MB free space |
| **Display** | 1920x1080 resolution |

### Notes

✅ **Internet:** NOT required (game works offline)
✅ **Graphics:** No dedicated GPU needed
✅ **Admin Rights:** Optional (portable versions available)
✅ **Antivirus:** May need to allow/whitelist the game

---

## 🪟 Windows Installation

### Method 1: Installer (Recommended)

**For:** Windows 10 or Windows 11

**Step-by-Step:**

1. **Download the installer**
   - File: `WiFiSecurityGame-1.0.0-Windows-Setup.exe`
   - Size: ~50 MB

2. **Run the installer**
   - Double-click the downloaded `.exe` file
   - Windows Defender SmartScreen may warn you:
     ```
     Windows protected your PC
     Microsoft Defender SmartScreen prevented an unrecognized app from starting
     ```
   - Click **"More info"** → **"Run anyway"**
   - This is normal for unsigned apps

3. **Follow installation wizard**
   - Click **"Next"**
   - Choose installation location (default: `C:\Program Files\WiFi Security Education\`)
   - Select additional tasks:
     - ☑ Create desktop shortcut
     - ☑ Create Start Menu entry
   - Click **"Install"**

4. **Wait for installation**
   - Progress bar shows installation status
   - Takes 30-60 seconds

5. **Launch the game**
   - Click **"Finish"** (checkbox: Launch WiFi Security Game)
   - Or: Desktop shortcut / Start Menu

**First Launch:**
- Antivirus may scan the file (wait for it to complete)
- Firewall may ask for permission (click "Allow")
- Telemetry consent dialog appears (choose yes/no)

---

### Method 2: Portable (No Installation)

**For:** Windows 10/11 without admin rights

**Step-by-Step:**

1. **Download portable version**
   - File: `WiFiSecurityGame-1.0.0-Windows-Portable.exe`
   - Size: ~50 MB

2. **Save to a folder**
   - Choose location (e.g., `C:\Games\` or USB drive)
   - No installation needed!

3. **Run the executable**
   - Double-click `WiFiSecurityGame-1.0.0-Windows-Portable.exe`
   - SmartScreen warning: Click "More info" → "Run anyway"

4. **Create shortcut (optional)**
   - Right-click `.exe` → Send to → Desktop (create shortcut)

**Portable Benefits:**
- No admin rights needed
- Run from USB drive
- Easy to move/delete
- No system changes

---

### Windows Troubleshooting

**Problem:** "Windows protected your PC"
- **Solution:** Click "More info" → "Run anyway"
- **Why:** App is not digitally signed (costs money)

**Problem:** Antivirus blocks the file
- **Solution:** Add exception/whitelist for the .exe
- **Common AVs:**
  - Windows Defender: Settings → Virus & threat protection → Exclusions
  - Norton: Security → Advanced → Exclusions
  - McAfee: Settings → Real-Time Scanning → Excluded Files

**Problem:** "This app can't run on your PC"
- **Solution:** Check Windows version (need Windows 10 or 11)
- **Check:** Settings → System → About

**Problem:** Install fails with "Access Denied"
- **Solution:** Right-click installer → "Run as administrator"

---

## 🍎 macOS Installation

### Method 1: DMG Installer (Recommended)

**For:** macOS 10.14 (Mojave) or later

**Step-by-Step:**

1. **Download the DMG**
   - File: `WiFiSecurityGame-1.0.0-macOS.dmg`
   - Size: ~60 MB

2. **Open the DMG file**
   - Double-click the downloaded `.dmg`
   - A new window opens showing the app and Applications folder

3. **Install the app**
   - Drag **WiFi Security Game.app** to **Applications** folder
   - Wait for copy to complete

4. **Eject the DMG**
   - Right-click the DMG in Finder sidebar → Eject

5. **Launch the game**
   - Open **Applications** folder
   - Find **WiFi Security Game**
   - **Right-click** → **Open** (important!)

6. **Bypass Gatekeeper**
   - First launch shows:
     ```
     "WiFi Security Game" cannot be opened because the developer cannot be verified.
     ```
   - Click **"Cancel"**
   - **Right-click** the app → **"Open"**
   - Click **"Open"** in the dialog
   - This only needs to be done once!

**Alternative Gatekeeper Bypass:**
```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine "/Applications/WiFi Security Game.app"
```

---

### Method 2: App Bundle

**For:** Manual installation

**Step-by-Step:**

1. **Download the app bundle**
   - File: `WiFiSecurityGame.app.zip`
   - Size: ~60 MB

2. **Extract the ZIP**
   - Double-click to unzip
   - Move `.app` to Applications folder

3. **Launch**
   - Right-click → Open (first time)
   - Double-click (subsequent times)

---

### macOS Troubleshooting

**Problem:** "Cannot be opened because the developer cannot be verified"
- **Solution:** Right-click → Open (instead of double-click)
- **Alternative:** System Preferences → Security & Privacy → "Open Anyway"

**Problem:** App opens then immediately closes
- **Solution:** Check macOS version (need 10.14+)
- **Check:** Apple menu → About This Mac

**Problem:** "The application is damaged and can't be opened"
- **Solution:** Remove quarantine attribute:
  ```bash
  xattr -d com.apple.quarantine "/Applications/WiFi Security Game.app"
  ```

**Problem:** App doesn't appear in Launchpad
- **Solution:** Wait 5-10 minutes or log out/in

**Problem:** "App is not optimized for your Mac" (M1/M2)
- **Solution:** Still works! Running via Rosetta 2
- **Future:** Native ARM build coming

---

## 🐧 Linux Installation

### Method 1: AppImage (Recommended)

**For:** Any modern Linux distribution

**Step-by-Step:**

1. **Download AppImage**
   - File: `WiFiSecurityGame-1.0.0-x86_64.AppImage`
   - Size: ~80 MB

2. **Make it executable**
   ```bash
   chmod +x WiFiSecurityGame-1.0.0-x86_64.AppImage
   ```

3. **Run it!**
   ```bash
   ./WiFiSecurityGame-1.0.0-x86_64.AppImage
   ```

**Create Desktop Shortcut:**
```bash
# Create .desktop file
cat > ~/.local/share/applications/wifi-security-game.desktop << EOF
[Desktop Entry]
Name=WiFi Security Game
Exec=/path/to/WiFiSecurityGame-1.0.0-x86_64.AppImage
Icon=wifi-security-game
Type=Application
Categories=Education;Game;
EOF

# Replace /path/to/ with actual path
```

**AppImage Benefits:**
- Universal (works everywhere)
- No installation needed
- Self-contained
- Easy to run from USB

**Requirements:**
- FUSE (usually pre-installed)
- If missing:
  ```bash
  # Ubuntu/Debian
  sudo apt install fuse

  # Fedora
  sudo dnf install fuse

  # Arch
  sudo pacman -S fuse2
  ```

---

### Method 2: .deb Package (Debian/Ubuntu)

**For:** Debian, Ubuntu, Linux Mint, Pop!_OS, etc.

**Step-by-Step:**

1. **Download .deb package**
   - File: `wifi-security-game_1.0.0_amd64.deb`
   - Size: ~50 MB

2. **Install via GUI**
   - Double-click the `.deb` file
   - Software Center opens
   - Click **"Install"**
   - Enter password when prompted

3. **Or install via terminal**
   ```bash
   sudo dpkg -i wifi-security-game_1.0.0_amd64.deb

   # Fix dependencies (if needed)
   sudo apt install -f
   ```

4. **Launch**
   - Application menu → Games → WiFi Security Game
   - Or terminal: `wifi-security-game`

**Benefits:**
- Native package
- System integration
- Automatic updates (future)
- Easy uninstall

---

### Method 3: From Source

**For:** Advanced users, other distros

**Requirements:**
```bash
# Install Python 3.11+
sudo apt install python3 python3-pip python3-venv  # Debian/Ubuntu
sudo dnf install python3 python3-pip              # Fedora
sudo pacman -S python python-pip                   # Arch

# Install Pygame
pip install pygame
```

**Installation:**
```bash
# Clone repository
git clone https://github.com/JuanCS-Dev/wifi-security-dashboard.git
cd wifi-security-dashboard
git checkout feature/gamification-v3-implementation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python3 wifi_security_game.py
```

---

### Linux Troubleshooting

**Problem:** "No such file or directory" when running AppImage
- **Solution:** Make it executable: `chmod +x *.AppImage`

**Problem:** "AppImage requires FUSE to run"
- **Solution:** Install FUSE:
  ```bash
  sudo apt install fuse  # Debian/Ubuntu
  ```

**Problem:** .deb install fails with dependency errors
- **Solution:** Fix dependencies:
  ```bash
  sudo apt install -f
  ```

**Problem:** "Permission denied"
- **Solution:** Don't use `sudo` to run the game (only for install)

**Problem:** Emojis show as boxes
- **Solution:** Install emoji fonts:
  ```bash
  sudo apt install fonts-noto-color-emoji
  ```

**Problem:** Low FPS / laggy
- **Solution:** Install graphics drivers, close other programs

---

## ❌ Uninstallation

### Windows

**Method 1: Control Panel**
1. Start → Settings → Apps
2. Find "WiFi Security Education"
3. Click → Uninstall
4. Confirm

**Method 2: Uninstaller**
1. Start Menu → WiFi Security Education → Uninstall
2. Follow wizard

**Remove user data:**
```cmd
del /F /S /Q %USERPROFILE%\.wifi_security_game
```

---

### macOS

**Method 1: Finder**
1. Open Applications folder
2. Drag "WiFi Security Game" to Trash
3. Empty Trash

**Remove user data:**
```bash
rm -rf ~/.wifi_security_game
```

---

### Linux

**AppImage:**
```bash
# Just delete the file
rm WiFiSecurityGame-1.0.0-x86_64.AppImage

# Remove user data
rm -rf ~/.wifi_security_game
```

**.deb Package:**
```bash
sudo apt remove wifi-security-game

# Or
sudo dpkg -r wifi-security-game

# Remove user data
rm -rf ~/.wifi_security_game
```

---

## 📁 File Locations

### Installation Directories

**Windows:**
- Program Files: `C:\Program Files\WiFi Security Education\`
- User Data: `C:\Users\<YourName>\.wifi_security_game\`

**macOS:**
- App: `/Applications/WiFi Security Game.app`
- User Data: `~/.wifi_security_game/`

**Linux:**
- AppImage: Wherever you saved it
- .deb: `/usr/bin/wifi-security-game`
- User Data: `~/.wifi_security_game/`

### User Data Files

Location: `~/.wifi_security_game/`

Contents:
- `consent.json` - Telemetry preference
- `events.json` - Telemetry events (if enabled)
- `bugs.json` - Bug reports (F1)
- `feedback.json` - Feedback (F12)

**To delete all user data:**
```bash
# Linux/macOS
rm -rf ~/.wifi_security_game/

# Windows
rd /s /q %USERPROFILE%\.wifi_security_game
```

---

## 🔐 Security & Privacy

### Is it safe to install?

**YES!**

✅ Open-source code (review on GitHub)
✅ No malware or adware
✅ No network access required
✅ No personal data collected (unless you opt-in to telemetry)
✅ COPPA compliant

### Why do antiviruses flag it?

**Reasons:**
- Not digitally signed (expensive for open-source)
- PyInstaller bundles (common false positive)
- New application (not yet in AV databases)

**Verification:**
- Check SHA256 hash (provided on download page)
- Review source code on GitHub
- Scan with VirusTotal (may show false positives)

### Digital Signatures

**Current Status:**
- ❌ Windows: Not code-signed (costs $300+/year)
- ❌ macOS: Not notarized (requires Apple Developer account)

**Future Plans:**
- ✅ Planning to add code signing after funding

**Workaround:**
- Follow Gatekeeper/SmartScreen bypass instructions above
- Or build from source yourself!

---

## 🆘 Additional Help

### Installation Issues

**Can't download:**
- Check internet connection
- Try different browser
- Disable VPN/proxy

**Can't install:**
- Check system requirements
- Ensure enough disk space (200 MB+)
- Disable antivirus temporarily

**Can't run:**
- Check OS version
- Update graphics drivers
- Try portable/AppImage version

### Support Channels

**Email:** support@wifisecurity.education
**Discord:** [discord.gg/wifi-security](#)
**GitHub Issues:** [github.com/JuanCS-Dev/wifi-security-dashboard/issues](#)

**Include in support requests:**
- Operating system and version
- Installation method used
- Error messages (screenshots help!)
- What you've already tried

---

## 📝 Platform-Specific Notes

### Windows

**Windows 11:**
- ✅ Fully supported
- ✅ No special steps needed

**Windows 10:**
- ✅ Fully supported
- ⚠️ Needs April 2018 Update or later

**Windows 8.1:**
- ❌ Not officially supported
- May work but untested

**Windows 7:**
- ❌ Not supported (EOL)

---

### macOS

**macOS 14 (Sonoma):**
- ✅ Supported
- ⚠️ Gatekeeper bypass required

**macOS 13 (Ventura):**
- ✅ Supported

**macOS 12 (Monterey):**
- ✅ Supported

**macOS 11 (Big Sur):**
- ✅ Supported

**macOS 10.15 (Catalina):**
- ✅ Supported
- ⚠️ May need extra permissions

**macOS 10.14 (Mojave):**
- ✅ Minimum version

**Older:**
- ❌ Not supported

**Apple Silicon (M1/M2/M3):**
- ✅ Works via Rosetta 2
- ⚠️ Not native ARM (yet)

---

### Linux

**Tested Distributions:**
- ✅ Ubuntu 22.04 LTS
- ✅ Ubuntu 24.04 LTS
- ✅ Fedora 38+
- ✅ Arch Linux (current)
- ✅ Linux Mint 21+
- ✅ Pop!_OS 22.04+

**Should work on:**
- Any distribution with Python 3.11+
- Any distribution with FUSE support

**Wayland:**
- ✅ Supported

**X11:**
- ✅ Supported

---

**Installation complete? Start playing!** 🎮

See [USER_GUIDE.md](USER_GUIDE.md) for how to play.

**Soli Deo Gloria** ✝️
