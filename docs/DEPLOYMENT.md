# Deployment Guide

Complete guide for deploying WiFi Security Education Dashboard in various environments.

## Quick Deployment Options

**Local (Python)**: `python3 main_v2.py`  
**Docker (Mock)**: `docker-compose --profile mock up`  
**Docker (Real)**: `docker-compose --profile real up` (requires --privileged)

## Prerequisites

- Linux (Ubuntu 20.04+ recommended)
- Python 3.10+ (local) OR Docker 20.10+ (container)
- Terminal with Unicode support (160x40 minimum)

## Local Deployment

```bash
# Quick start
bash scripts/setup.sh
python3 main_v2.py

# Manual
pip3 install -r requirements-v2.txt
python3 main_v2.py
```

## Docker Deployment

```bash
# Build
docker build -t wifi-dashboard:2.0.0 .

# Run mock mode
docker run -it wifi-dashboard:2.0.0

# Run real mode (requires privileges)
docker run -it --privileged --net=host wifi-dashboard:2.0.0 python3 main_v2.py --real
```

## Docker Compose (Recommended)

```bash
# Mock mode (educational, no root)
docker-compose --profile mock up

# Real mode (monitoring, requires privileges)
docker-compose --profile real up

# Development (with source mounted)
docker-compose --profile dev up
```

## Production Best Practices

1. **Use Mock Mode by Default** (safe, educational)
2. **Never Expose to Internet** (local CLI tool only)
3. **Monitor Performance** (`python3 scripts/benchmark.py`)
4. **Keep Dependencies Updated** (Dependabot automated)
5. **Backup Configurations** (`config/dashboard.yml`)

## Troubleshooting

- **Permission Denied**: Use mock mode OR `sudo python3 main_v2.py --real`
- **Missing Dependencies**: Run `bash scripts/check_dependencies.sh`
- **Broken UI**: Resize terminal (160x40+), install fonts (`sudo apt install fonts-noto`)
- **High CPU**: Increase `refresh_rate_ms` in config (100ms → 200ms)

See [QUICK_START.md](./QUICK_START.md) for detailed setup.

---

**Framework**: Constituição Vértice v3.0 (P2 - Validação Preventiva)

**Soli Deo Gloria** ✝️
