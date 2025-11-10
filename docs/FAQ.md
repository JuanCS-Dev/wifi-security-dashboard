# Frequently Asked Questions (FAQ)

Common questions and answers about WiFi Security Education Dashboard v2.0.

## Table of Contents

1. [General Questions](#general-questions)
2. [Installation & Setup](#installation--setup)
3. [Mock vs Real Mode](#mock-vs-real-mode)
4. [Usage & Features](#usage--features)
5. [Plugins](#plugins)
6. [Performance](#performance)
7. [Troubleshooting](#troubleshooting)
8. [Development](#development)
9. [Security & Privacy](#security--privacy)
10. [Roadmap & Future](#roadmap--future)

---

## General Questions

### What is WiFi Security Education Dashboard?

An educational terminal dashboard for monitoring WiFi and system metrics in real-time. Designed for students learning about network security, system administration, and Python development.

### Is this tool for hacking WiFi networks?

**No**. This is an **educational tool** for learning network monitoring concepts. You may only use it on networks you own or have explicit permission to monitor. See [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) and [SECURITY.md](../SECURITY.md).

### Do I need to be a programmer to use it?

No! Mock mode requires zero configuration. Just run `python3 main_v2.py` and explore the dashboard. However, plugin development requires Python knowledge.

### What's the difference between v1.0 and v2.0?

- **v1.0**: Monolithic architecture, limited testing
- **v2.0**: Plugin-based, event-driven, 98% test coverage, mock mode, Docker support

### Is it free and open source?

Yes! Licensed under MIT License. See [LICENSE](../LICENSE).

---

## Installation & Setup

### What are the system requirements?

- **OS**: Linux (Ubuntu 20.04+, Debian 11+)
- **Python**: 3.10 or higher
- **Terminal**: Unicode support, 160x40 minimum
- **Dependencies**: rich, psutil, pytest, pyyaml

See [QUICK_START.md](./QUICK_START.md) for details.

### Can I run it on Windows or macOS?

**Mock mode** works on all platforms (Windows, macOS, Linux).
**Real mode** is Linux-only (uses `iw`, `ip`, `scapy` which are Linux-specific).

### How do I install it?

**Quick install**:
```bash
git clone https://github.com/[your-user]/wifi_security_education.git
cd wifi_security_education
bash scripts/setup.sh
python3 main_v2.py
```

See [QUICK_START.md](./QUICK_START.md) for step-by-step guide.

### Installation fails with "psutil not found"

```bash
# Install psutil
pip3 install psutil
# Or system-wide
sudo apt install python3-psutil
```

Then run `bash scripts/check_dependencies.sh` to verify.

### Can I install it system-wide?

Yes! Use `scripts/install.sh` for systemd service installation:
```bash
sudo bash scripts/install.sh
```

This installs to `/opt/wifi-dashboard` with auto-start on boot.

---

## Mock vs Real Mode

### What is mock mode?

Mock mode simulates a realistic family network without requiring root privileges or real WiFi interfaces. Perfect for:
- Learning the dashboard safely
- Demonstrations without network access
- Testing plugins
- Educational presentations

### What is real mode?

Real mode monitors your actual system and network using root privileges. Requires:
- Linux OS
- Root access (`sudo`)
- WiFi interface (for WiFi plugin)
- Network tools (`iw`, `ip`, `scapy`)

### Which mode should I use?

- **Learning?** → Mock mode
- **Demonstrations?** → Mock mode
- **Actual monitoring?** → Real mode (with permission)

### How do I switch between modes?

**Mock mode** (default):
```bash
python3 main_v2.py
```

**Real mode**:
```bash
sudo python3 main_v2.py --real
```

### Can I customize mock data?

Yes! Edit `src/mock/mock_data_generator.py` to change:
- Device names
- Network SSIDs
- Baseline CPU/RAM usage
- Number of connected devices

See [ARCHITECTURE.md](./ARCHITECTURE.md) for mock data design.

---

## Usage & Features

### How do I exit the dashboard?

Press `Ctrl+C` for graceful shutdown.

### What metrics does it display?

- **System**: CPU%, RAM%, Disk usage
- **WiFi**: SSID, signal strength, connected devices
- **Network**: Bandwidth (upload/download), connections

### Can I customize the UI layout?

Currently no (v2.0). Planned for v3.0 (Textual framework with drag-and-drop widgets).

### How do I change the refresh rate?

Edit `config/dashboard-example.yml`:
```yaml
dashboard:
  refresh_rate_ms: 100  # 10 FPS
  # Or slower: 200 (5 FPS)
```

Then run with `--config`:
```bash
python3 main_v2.py --config config/dashboard-example.yml
```

### Can I export the data?

Not in v2.0. Planned for v2.1:
- CSV export
- JSON export
- Prometheus exporter

---

## Plugins

### How do I create a custom plugin?

See [PLUGIN_API.md](./PLUGIN_API.md) for complete guide. Quick start:

```python
from src.core.base_plugin import BasePlugin

class MyPlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="my_plugin", update_rate_ms=1000)

    def collect_data(self):
        return {"value": 42}
```

Save to `src/plugins/my_plugin.py` and restart dashboard.

### Where can I find more plugins?

**Plugin Marketplace** coming in v2.1. Currently:
- Browse `src/plugins/` for examples
- Community plugins on GitHub (search for "wifi-dashboard-plugin")

### Can plugins break the dashboard?

Plugins run in try/except. If a plugin crashes, PluginManager logs error and continues. Dashboard remains stable.

### How do I disable a plugin?

Edit config:
```yaml
plugins:
  wifi:
    enabled: false  # Disable WiFi plugin
```

Or remove plugin file from `src/plugins/`.

---

## Performance

### Dashboard is slow / laggy

**Solutions**:
1. Increase refresh rate (100ms → 200ms)
2. Increase plugin update rates (1s → 5s)
3. Disable expensive plugins (WiFi scan)
4. Check performance: `python3 scripts/benchmark.py`

Target: <100ms frame time, ≥10 FPS.

### High CPU usage

**Normal**: 5-15% CPU for 10 FPS dashboard.
**High**: >30% CPU indicates problem.

**Solutions**:
```yaml
# Slow down dashboard
dashboard:
  refresh_rate_ms: 200  # 5 FPS instead of 10 FPS

# Slow down expensive plugins
plugins:
  wifi:
    rate_ms: 10000  # Scan every 10s instead of 5s
```

### Terminal rendering is slow

**Requirements**:
- Unicode-capable terminal
- 256-color support
- Terminal size ≥160x40

**Test**:
```bash
echo $TERM  # Should be xterm-256color
echo $COLUMNS x $LINES  # Should be 160x40+
```

---

## Troubleshooting

### "Permission denied" errors

**Cause**: Real mode requires root.

**Solutions**:
```bash
# Use mock mode (no root)
python3 main_v2.py

# Or use sudo for real mode
sudo python3 main_v2.py --real
```

### Graphs don't display correctly

**Causes**: Terminal too small, missing Unicode fonts.

**Solutions**:
```bash
# Resize terminal to 160x40+
# Install fonts
sudo apt install fonts-noto

# Set TERM
export TERM=xterm-256color
```

### "ModuleNotFoundError"

**Cause**: Dependencies not installed.

**Solution**:
```bash
bash scripts/check_dependencies.sh
pip3 install -r requirements-v2.txt
```

### Dashboard crashes immediately

**Debug**:
```bash
# Run with Python debugging
python3 -v main_v2.py

# Check logs (if using systemd)
sudo journalctl -u wifi-dashboard -n 50
```

---

## Development

### How do I contribute?

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- P1-P6 principles (Constituição Vértice v3.0)
- Contribution process
- Testing requirements (≥98% coverage)
- Code style (Black, isort, flake8)

### How do I run tests?

```bash
# All tests
make test

# Unit tests only
make test-unit

# With coverage
make coverage
```

Target: ≥98% coverage, FPC ≥95%, LEI <1.0, CRS ≥95%.

### How do I add a new dependency?

1. Add to `requirements-v2.txt`
2. Update `scripts/check_dependencies.sh`
3. Validate with P2 (Validação Preventiva): check if package exists before use
4. Update tests

**Example**:
```python
# P2: Validate before use
try:
    import new_package
    HAS_NEW_PACKAGE = True
except ImportError:
    HAS_NEW_PACKAGE = False

# Use with fallback
if HAS_NEW_PACKAGE:
    # Use feature
else:
    # Fallback or warn
```

### What are the coding standards?

- **Python**: 3.10+ type hints
- **Line length**: 100 characters (Black)
- **Imports**: Sorted with isort (black profile)
- **Docstrings**: Google style
- **Tests**: pytest, ≥98% coverage
- **Framework**: Constituição Vértice v3.0 (P1-P6)

Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

---

## Security & Privacy

### Is my network data sent anywhere?

**No**. Dashboard runs **100% locally**. No data is sent to external servers.

### Can I use this on public WiFi?

**Mock mode**: Yes (simulated data only).
**Real mode**: **NO**. Only monitor networks you own or have explicit permission.

### Is it legal to monitor my home network?

Yes, monitoring your own network is legal. However:
- Do NOT monitor neighbors' networks
- Do NOT use for malicious purposes
- Respect privacy laws (GDPR, LGPD)

See [SECURITY.md](../SECURITY.md) and [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md).

### Does it store logs or history?

v2.0: **No persistent storage**.
v2.1: Optional logging to files/SQLite (with user consent).

### Is it safe to run with sudo?

**Mock mode**: No sudo needed.
**Real mode**: Sudo required but safe (no network modification, read-only monitoring).

**Security**:
- Code is open source (auditable)
- No external network calls
- Follows principle of least privilege

---

## Roadmap & Future

### When is v2.1 released?

Planned: **Q1 2026** (3 months development + 1 month beta).

Features: Plugin marketplace, alerting, data export, web dashboard (beta).

### Will v3.0 break my plugins?

**No**. Plugin API guaranteed 100% backward compatible. See [ROADMAP.md](../ROADMAP.md).

### Can I request a feature?

Yes! Open GitHub Issue with `[Feature Request]` tag. Describe:
- Use case
- Educational value
- Implementation ideas

See [CONTRIBUTING.md](../CONTRIBUTING.md).

### Is there a web UI version?

Not in v2.0. Coming in **v2.1 (beta)** with FastAPI + React + WebSockets.

### Will it support Windows/macOS fully?

**v2.0**: Mock mode only.
**v2.1+**: Investigating multi-platform support for real mode.

---

## Still Have Questions?

- **Docs**: [README.md](../README.md), [ARCHITECTURE.md](./ARCHITECTURE.md), [QUICK_START.md](./QUICK_START.md)
- **GitHub Issues**: [Open an issue](https://github.com/[your-user]/wifi_security_education/issues)
- **Contributing**: [CONTRIBUTING.md](../CONTRIBUTING.md)

---

**Framework**: Constituição Vértice v3.0 (P4 - Rastreabilidade Total)

**Soli Deo Gloria** ✝️
