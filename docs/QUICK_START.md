# Quick Start Guide

Get up and running with WiFi Security Education Dashboard in 5 minutes!

## Prerequisites

- Linux (Ubuntu/Debian recommended)
- Python 3.10+
- Terminal with Unicode support

## Installation (5 minutes)

### Option 1: Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/[your-user]/wifi_security_education.git
cd wifi_security_education

# Run automated setup
bash scripts/setup.sh

# Done! Run dashboard
python3 main_v2.py
```

### Option 2: Manual Setup

```bash
# Install dependencies
pip3 install -r requirements-v2.txt

# Verify installation
bash scripts/check_dependencies.sh

# Run dashboard
python3 main_v2.py
```

## First Run

### Mock Mode (No Root Required)

```bash
# Start in mock mode (default)
python3 main_v2.py
```

You'll see a simulated family network with:
- 📱 Parents' smartphones
- 💻 Laptops
- 📱 Children's tablets
- 🖥️ Smart TV

### Real Mode (Requires Root)

```bash
# For real system data
sudo python3 main_v2.py --real
```

## Quick Commands

```bash
# Run tests
make test

# Check code quality
make validate

# View metrics
make metrics

# Get help
python3 main_v2.py --help
```

## Troubleshooting

### "psutil not found"
```bash
pip3 install psutil
# or
sudo apt install python3-psutil
```

### "Permission denied"
Use mock mode (no root needed):
```bash
python3 main_v2.py  # Mock is default
```

### Graphs don't appear
- Resize terminal to 160x40+
- Install Unicode fonts: `sudo apt install fonts-noto`

## Next Steps

1. **Read**: [README.md](../README.md) for full documentation
2. **Learn**: [CONTRIBUTING.md](../CONTRIBUTING.md) to contribute
3. **Explore**: Run `make help` for all commands

---

**Soli Deo Gloria** ✝️
