# Support

Get help with WiFi Security Education Dashboard v2.0.

## Documentation

Before opening an issue, please check our comprehensive documentation:

### Getting Started
- **[README.md](../README.md)** - Project overview and features
- **[QUICK_START.md](../docs/QUICK_START.md)** - 5-minute installation guide
- **[FAQ.md](../docs/FAQ.md)** - 50+ frequently asked questions

### Technical Documentation
- **[ARCHITECTURE.md](../docs/ARCHITECTURE.md)** - System architecture and design patterns
- **[PLUGIN_API.md](../docs/PLUGIN_API.md)** - Plugin development guide
- **[DEPLOYMENT.md](../docs/DEPLOYMENT.md)** - Docker, systemd deployment options

### Community & Contributing
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Contribution guidelines (P1-P6 framework)
- **[CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md)** - Community standards
- **[ROADMAP.md](../ROADMAP.md)** - Future plans (v2.1, v3.0, v4.0)

### Security & Legal
- **[SECURITY.md](../SECURITY.md)** - Security policy and vulnerability reporting
- **[LICENSE](../LICENSE)** - MIT License terms

---

## Common Issues

### Installation Problems

**Issue**: `ModuleNotFoundError: No module named 'rich'`

**Solution**:
```bash
pip3 install -r requirements-v2.txt
# Or check dependencies
bash scripts/check_dependencies.sh
```

**Issue**: `Permission denied` when running dashboard

**Solution**:
```bash
# Use mock mode (no root needed)
python3 main_v2.py

# Or use sudo for real mode
sudo python3 main_v2.py --real
```

**Issue**: Graphs don't display correctly

**Solution**:
```bash
# Resize terminal (minimum 160x40)
# Install fonts
sudo apt install fonts-noto
# Set TERM variable
export TERM=xterm-256color
```

### Usage Questions

**Question**: How do I switch between mock and real mode?

**Answer**: See [FAQ.md - Mock vs Real Mode](../docs/FAQ.md#mock-vs-real-mode)

**Question**: How do I create a custom plugin?

**Answer**: See [PLUGIN_API.md](../docs/PLUGIN_API.md)

**Question**: How do I deploy with Docker?

**Answer**: See [DEPLOYMENT.md - Docker Deployment](../docs/DEPLOYMENT.md#docker-deployment)

---

## Getting Help

### 1. Search Existing Issues

Before opening a new issue, search for similar problems:
- **[GitHub Issues](https://github.com/[your-user]/wifi_security_education/issues)**
- **[Closed Issues](https://github.com/[your-user]/wifi_security_education/issues?q=is%3Aissue+is%3Aclosed)**

### 2. Check FAQ

90% of questions are answered in:
- **[FAQ.md](../docs/FAQ.md)** - 50+ Q&As across 10 categories

### 3. Open GitHub Issue

If documentation doesn't help, open an issue:
- **[Bug Report](.github/ISSUE_TEMPLATE/bug_report.md)** - For bugs and crashes
- **[Feature Request](.github/ISSUE_TEMPLATE/feature_request.md)** - For new features

**Include**:
- Operating system and version
- Python version (`python3 --version`)
- Dashboard version (check `VERSION` file)
- Mode (mock or real)
- Full error message or screenshot
- Steps to reproduce

---

## Community Support

This is an educational open-source project maintained by volunteers.

**Response Times**:
- Bug reports: 2-5 business days
- Feature requests: 1-2 weeks
- Security issues: 24-48 hours (see [SECURITY.md](../SECURITY.md))

**Best Practices**:
- Be respectful (see [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md))
- Provide complete information
- Search before posting
- One issue per GitHub Issue

---

## Contributing

Want to contribute instead of just reporting?

See **[CONTRIBUTING.md](../CONTRIBUTING.md)** for:
- P1-P6 development framework (Constituição Vértice v3.0)
- Testing requirements (≥98% coverage)
- Code style (Black, isort, flake8)
- Pull request process

---

## Educational Use

This is an **educational tool** designed for learning WiFi security and network monitoring concepts.

**Ethical Use**:
- Only monitor networks you own or have permission to monitor
- Use mock mode for demonstrations and learning
- Respect privacy laws (GDPR, LGPD)
- See [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) for ethical guidelines

**Educational Resources**:
- Mock mode simulates realistic family network (no root needed)
- Plugin architecture teaches software design patterns
- 98% test coverage demonstrates testing best practices
- Comprehensive documentation for self-learning

---

**Framework**: Constituição Vértice v3.0 (P4 - Rastreabilidade Total)

**Soli Deo Gloria** ✝️
