# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.0.x   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do NOT** create a public GitHub issue

Security vulnerabilities should not be disclosed publicly until patched.

### 2. Report privately via:
- **GitHub Security Advisories**: (preferred)
- **Email**: [create security email]

### 3. Include in your report:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 4. What to expect:
- **Initial response**: Within 48 hours
- **Status updates**: Every 72 hours
- **Fix timeline**: Depends on severity
  - Critical: 1-7 days
  - High: 7-14 days
  - Medium: 14-30 days
  - Low: 30-90 days

## Security Best Practices

### For Users:
- **Mock Mode**: Use mock mode for demonstrations (no root required)
- **Root Access**: Only use real mode with root when necessary
- **Network**: Understand that real mode captures network packets
- **Updates**: Keep dependencies updated (`pip install -U -r requirements-v2.txt`)

### For Contributors:
- **Input Validation**: Always validate user inputs (P3 - Ceticismo Crítico)
- **API Validation**: Verify external APIs exist before use (P2 - Validação Preventiva)
- **Dependencies**: Use `try/except` for optional dependencies
- **Secrets**: Never commit API keys, passwords, or tokens
- **Permissions**: Document when root/admin is required

## Known Security Considerations

### Real Mode
- **Requires root**: Real mode needs root for packet capture
- **Network sniffing**: Captures network traffic for analysis
- **Privacy**: Only use on networks you own/have permission to monitor

### Mock Mode
- **No privileges needed**: Safe for educational demonstrations
- **No real data**: Uses simulated data, no privacy concerns

## Security Features

- ✅ **No network exposure**: Dashboard runs locally only
- ✅ **No external APIs**: No data sent to external servers
- ✅ **Graceful fallbacks**: Falls back to mock mode if permissions missing
- ✅ **Input validation**: All inputs validated before processing
- ✅ **Dependency checks**: Validates dependencies before use (P2)

## Disclosure Policy

- Vulnerabilities will be disclosed after a fix is available
- Credit will be given to reporters (unless they prefer anonymity)
- CVE IDs will be requested for serious vulnerabilities

---

**Framework:** Constituição Vértice v3.0 (P2 - Validação Preventiva)

**Soli Deo Gloria** ✝️
