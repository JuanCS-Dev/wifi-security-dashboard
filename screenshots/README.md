# Screenshots

Visual documentation of WiFi Security Education Dashboard v2.0.

## Mock Mode Dashboard

### Startup Banner

```
     ██╗██╗   ██╗ █████╗ ███╗   ██╗
     ██║██║   ██║██╔══██╗████╗  ██║
     ██║██║   ██║███████║██╔██╗ ██║
██   ██║██║   ██║██╔══██║██║╚██╗██║
╚█████╔╝╚██████╔╝██║  ██║██║ ╚████║
 ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝

WiFi Security Education Dashboard v2.0
Educational Mode (Mock Data - No Root Required)
Soli Deo Gloria ✝️
```

### Main Dashboard Layout

```
┌─ WiFi Security Dashboard v2.0 ─────────────────────────────────────────┐
│                                                                          │
│ ┌─ System Metrics ──────────────────┐  ┌─ WiFi Status ────────────────┐│
│ │ CPU: ████████░░░░░░░░░░ 45.2%     │  │ SSID: FamilyNet_5G           ││
│ │ RAM: ██████████░░░░░░░░ 62.1%     │  │ Signal: ████████░░ -52 dBm   ││
│ │ Disk: ████████████████░ 78.5%     │  │ Connected: 8 devices         ││
│ │                                    │  │ Encryption: WPA3             ││
│ │ CPU History (10 FPS):              │  │ Channel: 36 (5GHz)           ││
│ │ ▂▃▄▅▆▅▄▃▄▅▆▇▆▅▄▃▂▁▂▃▄▅▆▅▄         │  │                              ││
│ └────────────────────────────────────┘  └──────────────────────────────┘│
│                                                                          │
│ ┌─ Network Activity ────────────────────────────────────────────────────┐│
│ │ Upload:   ▲ 2.3 MB/s  ▂▃▄▅▆▅▄▃▄▅                                    ││
│ │ Download: ▼ 8.7 MB/s  ▅▆▇▆▅▄▃▄▅▆▇                                   ││
│ │ Active Connections: 12                                               ││
│ └──────────────────────────────────────────────────────────────────────┘│
│                                                                          │
│ ┌─ Connected Devices (Mock Family Network) ─────────────────────────────┐│
│ │ 📱 Dad's Phone        - 192.168.1.100  - Active (2.1 MB/s)          ││
│ │ 📱 Mom's Phone        - 192.168.1.101  - Active (1.8 MB/s)          ││
│ │ 💻 Dad's Laptop       - 192.168.1.102  - Active (5.2 MB/s)          ││
│ │ 💻 Mom's Laptop       - 192.168.1.103  - Idle                        ││
│ │ 📱 Kid's Tablet       - 192.168.1.104  - Active (3.5 MB/s)          ││
│ │ 🖥️  Smart TV          - 192.168.1.105  - Streaming (8.7 MB/s)       ││
│ │ 🎮 Gaming Console     - 192.168.1.106  - Gaming (4.2 MB/s)          ││
│ │ 🖨️  Printer           - 192.168.1.107  - Idle                        ││
│ └──────────────────────────────────────────────────────────────────────┘│
│                                                                          │
│ [Press Ctrl+C to exit] | Mock Mode | 10 FPS | Coverage: 98%            │
└──────────────────────────────────────────────────────────────────────────┘
```

### Features Highlighted in Mock Mode

- ✅ **No Root Required**: Runs without sudo, safe for students
- ✅ **Realistic Data**: Brownian motion for CPU/RAM, family network simulation
- ✅ **Educational Devices**: Dad, Mom, Kids, Smart TV, Gaming Console
- ✅ **Real-time Graphs**: Sparklines showing metric history
- ✅ **Color-coded**: Green (ok), Yellow (warning), Red (critical)
- ✅ **Unicode Graphics**: Beautiful terminal UI with Rich library
- ✅ **10 FPS**: Smooth 100ms refresh rate

## Real Mode Dashboard

### Differences from Mock Mode

```
┌─ WiFi Security Dashboard v2.0 (REAL MODE - Root Required) ─────────────┐
│                                                                          │
│ ⚠️  MONITORING REAL NETWORK - USE RESPONSIBLY                           │
│                                                                          │
│ ┌─ System Metrics (Actual) ─────────┐  ┌─ WiFi Status (Live) ─────────┐│
│ │ CPU: ██░░░░░░░░░░░░░░░░ 12.8%     │  │ SSID: MyHomeNetwork          ││
│ │ RAM: █████████░░░░░░░░░ 58.3%     │  │ Signal: ██████░░░░ -65 dBm   ││
│ │ Disk: ███████████████░░ 72.1%     │  │ Connected: 3 devices         ││
│ │                                    │  │ Encryption: WPA2-PSK         ││
│ │ [Actual system data via psutil]   │  │ Channel: 6 (2.4GHz)          ││
│ └────────────────────────────────────┘  └──────────────────────────────┘│
│                                                                          │
│ ┌─ Network Activity (Live Capture) ─────────────────────────────────────┐│
│ │ Interface: wlan0                                                      ││
│ │ Upload:   ▲ 125 KB/s                                                 ││
│ │ Download: ▼ 3.2 MB/s                                                 ││
│ │ [Real network traffic via scapy]                                     ││
│ └──────────────────────────────────────────────────────────────────────┘│
│                                                                          │
│ ┌─ Connected Devices (ARP Scan) ────────────────────────────────────────┐│
│ │ [Real devices detected on network via iw/ip commands]                ││
│ │ Device hostnames and MACs from actual network                        ││
│ └──────────────────────────────────────────────────────────────────────┘│
│                                                                          │
│ [Press Ctrl+C to exit] | REAL Mode | 10 FPS | Root Access Active       │
└──────────────────────────────────────────────────────────────────────────┘
```

### Real Mode Features

- ⚠️ **Requires Root**: `sudo python3 main_v2.py --real`
- 📡 **Live WiFi Scan**: Actual SSID, signal strength via `iw`
- 🌐 **Real Network Traffic**: Bandwidth monitoring via `scapy`
- 💻 **Actual System Stats**: CPU/RAM/Disk via `psutil`
- 🔍 **ARP Scanning**: Connected devices detection
- ⚡ **Live Updates**: Real-time data every 100ms

## Layout Breakdown

### Header Section
- Application title and version
- Mode indicator (Mock/Real)
- Warning banner (Real mode only)

### System Metrics Panel (Top Left)
- CPU percentage with bar chart
- RAM usage with bar chart
- Disk usage with bar chart
- CPU history sparkline (50 data points)

### WiFi Status Panel (Top Right)
- Network SSID
- Signal strength (dBm) with bar
- Connected device count
- Encryption type (WPA2/WPA3)
- Channel and frequency band

### Network Activity Panel (Middle)
- Upload speed with sparkline
- Download speed with sparkline
- Active connections count

### Connected Devices Panel (Bottom)
- Device list with icons (📱💻🖥️🎮🖨️)
- IP addresses
- Connection status (Active/Idle/Streaming)
- Bandwidth per device

### Footer Section
- Controls reminder (Ctrl+C to exit)
- Mode indicator
- FPS counter
- Additional status info

## Terminal Requirements

**Minimum Terminal Size**: 160 columns × 40 rows

```bash
# Check your terminal size
echo "Columns: $COLUMNS, Lines: $LINES"

# Should show: Columns: 160+, Lines: 40+
```

**Required Terminal Features**:
- Unicode support (for box drawing characters)
- 256-color support (for colored graphs)
- TERM=xterm-256color or compatible

**Recommended Terminals**:
- ✅ GNOME Terminal (Linux)
- ✅ Konsole (KDE Linux)
- ✅ iTerm2 (macOS)
- ✅ Windows Terminal (Windows 10+)
- ✅ Alacritty (Cross-platform)
- ⚠️ TTY (limited colors)

## How to Run

### Mock Mode (Recommended for Learning)

```bash
# Default: runs in mock mode
python3 main_v2.py

# Explicit mock flag
python3 main_v2.py --mock
```

### Real Mode (Monitoring)

```bash
# Requires root privileges
sudo python3 main_v2.py --real
```

### With Custom Config

```bash
# Use custom configuration
python3 main_v2.py --config config/my-dashboard.yml
```

## Performance

- **Target FPS**: 10 FPS (100ms refresh rate)
- **CPU Usage**: 5-15% (normal), <30% (acceptable)
- **Memory**: ~50MB RSS (mock mode), ~100MB (real mode)
- **Frame Time**: <100ms total (plugins + UI rendering)

## Color Scheme

**System Metrics**:
- 🟢 Green: 0-60% (OK)
- 🟡 Yellow: 60-80% (Warning)
- 🔴 Red: 80-100% (Critical)

**WiFi Signal**:
- 🟢 Green: -50 dBm to -1 dBm (Excellent)
- 🟡 Yellow: -70 dBm to -51 dBm (Good)
- 🟠 Orange: -80 dBm to -71 dBm (Fair)
- 🔴 Red: -90 dBm to -81 dBm (Poor)

**Network Activity**:
- 🔵 Blue: Upload traffic
- 🟣 Purple: Download traffic

## Screenshot Notes

**Note**: Actual screenshots cannot be captured easily due to:
1. Rich TUI requires interactive terminal
2. ANSI color codes don't translate to static images
3. Dynamic content changes every 100ms

**Alternatives**:
- ASCII art representation (shown above)
- Terminal recording (asciinema.org)
- Video screen recording

## Recording Dashboard

### Using asciinema (Recommended)

```bash
# Install asciinema
sudo apt install asciinema

# Record session
asciinema rec dashboard-demo.cast

# Run dashboard
python3 main_v2.py

# Press Ctrl+C to stop
# Press Ctrl+D to stop recording

# Play recording
asciinema play dashboard-demo.cast

# Upload to asciinema.org
asciinema upload dashboard-demo.cast
```

### Using script

```bash
# Record terminal session
script -c "python3 main_v2.py" dashboard.log

# Stop with Ctrl+C

# View recording
cat dashboard.log
```

## Packet Analyzer (Wireshark-style) 🆕

**NEW in v2.0!** - Educational packet analysis component

```
╭───────────────────────── Packet Analyzer (Wireshark-style) ─────────────────────────╮
│                                                                                      │
│  📊 Rate: 85.5 pkts/s  |  Total: 803  |  Backend: mock                               │
│                                                                                      │
│  🔝 Top Protocols:                                                                   │
│    HTTPS    █████████████████ 442 pkts (55%)                                         │
│    H264     ███ 154 pkts (19%)                                                       │
│    DNS      ██ 89 pkts (11%)                                                         │
│    QUIC     ██ 76 pkts (9%)                                                          │
│    HTTP     █ 31 pkts (4%) ⚠️ Unencrypted!                                            │
│    MDNS      11 pkts (1%)                                                            │
│                                                                                      │
│                                                                                      │
│                               📦 Recent Packets                                      │
│  ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓ │
│  ┃ Time         ┃ Source           ┃ Destination      ┃ Protocol   ┃ Info            ┃ │
│  ┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩ │
│  │ 14:32:15.234 │ 192.168.1.102    │ 142.250.185.46   │ HTTPS      │ Gmail -         │ │
│  │              │                  │                  │            │ Encrypted ✅    │ │
│  │ 14:32:15.456 │ 192.168.1.104    │ 93.184.216.34    │ HTTP       │ ⚠️ Unencrypted   │ │
│  │              │                  │                  │            │ website!        │ │
│  │              │                  │                  │            │ Passwords       │ │
│  │              │                  │                  │            │ visible!        │ │
│  │ 14:32:15.678 │ 192.168.1.105    │ 54.192.147.14    │ H264       │ Netflix - Video │ │
│  │              │                  │                  │            │ streaming ✅    │ │
│  │ 14:32:15.890 │ 192.168.1.100    │ 31.13.86.36      │ QUIC       │ WhatsApp -      │ │
│  │              │                  │                  │            │ Encrypted       │ │
│  │              │                  │                  │            │ messaging ✅    │ │
│  │ 14:32:16.012 │ 192.168.1.112    │ 142.250.185.46   │ HTTPS      │ YouTube Kids -  │ │
│  │              │                  │                  │            │ Encrypted ✅    │ │
│  └──────────────┴──────────────────┴──────────────────┴────────────┴─────────────────┘ │
│                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────╯
```

### Features

- **📊 Protocol Analysis**: Real-time breakdown of network protocols (HTTPS, HTTP, DNS, QUIC, etc.)
- **🔝 Top Protocols**: Visual bars showing most common protocols with percentages
- **📦 Recent Packets**: Wireshark-style table with time, source, destination, protocol, and info
- **⚠️ Security Warnings**: Educational alerts for unencrypted traffic (HTTP)
- **✅ Safety Indicators**: Visual confirmation of encrypted protocols (HTTPS, QUIC)
- **🎓 Educational**: Teaches children about internet security in real-time

### Educational Value

**For Kids (7-8 years)**:
- Learn that internet uses "different languages" (protocols)
- See which websites are safe (🔒 padlock = HTTPS)
- Understand why HTTP is dangerous (passwords can be seen!)
- Connect actions (watching Netflix) with data (H264 traffic increases)

**For Parents**:
- Monitor home network traffic transparently
- Teach internet safety with visual examples
- Identify what apps/devices are doing
- Start conversations about encryption and privacy

### Backend Modes

1. **Mock Mode** (Default - No root required)
   - Simulated family network traffic
   - Realistic protocol distribution
   - Educational examples (HTTP warnings)
   - Perfect for learning!

2. **Scapy Mode** (Real - Requires permissions)
   - Live packet capture
   - Full protocol analysis
   - Real network monitoring

3. **PyShark Mode** (Real - Requires Wireshark)
   - TShark integration
   - Complete Wireshark dissectors
   - Advanced protocol detection

### Documentation

📚 Full documentation: [`docs/PACKET_ANALYZER.md`](../docs/PACKET_ANALYZER.md)

## See Also

- [QUICK_START.md](../docs/QUICK_START.md) - Installation guide
- [ARCHITECTURE.md](../docs/ARCHITECTURE.md) - System design
- [FAQ.md](../docs/FAQ.md) - Common questions
- [PACKET_ANALYZER.md](../docs/PACKET_ANALYZER.md) - Packet analyzer guide 🆕

---

**Framework**: Constituição Vértice v3.0 (P4 - Rastreabilidade Total)

**Soli Deo Gloria** ✝️
