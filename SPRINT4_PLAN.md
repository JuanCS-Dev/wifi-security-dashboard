# Sprint 4 - Implementation Plan
**Date:** 2025-11-12  
**Author:** Juan-Dev - Soli Deo Gloria ✝️  
**Status:** 🚧 In Progress

---

## 🎯 Sprint 4 Objectives

**Goal:** Full integration with real plugins (no fallback to mock unless necessary)

**Scope:**
1. Enhance WiFi Plugin for robust real-world data collection
2. Improve Network Plugin with more detailed metrics
3. Add proper permissions handling and error messages
4. Create comprehensive documentation for real mode setup
5. Implement health checks for all plugins

---

## 📊 Current State Analysis

### ✅ Available Tools (System Check)
```bash
✅ nmcli          - NetworkManager CLI (WiFi)
✅ iwconfig       - Wireless tools (WiFi fallback)
✅ scapy          - Packet capture library
❌ tshark         - Wireshark CLI (optional for PyShark)
✅ psutil         - System metrics (already integrated)
```

### 🔌 Network Interfaces Detected
```
lo              - Loopback (127.0.0.1)
wlp0s20f3       - WiFi interface ← TARGET
br-06454e4161c7 - Docker bridge
docker0         - Docker network
```

### 📁 Plugin Status

| Plugin | Real Mode | Fallback | Issues |
|--------|-----------|----------|--------|
| **SystemPlugin** | ✅ Working | N/A | None |
| **WiFiPlugin** | ⚠️ Needs testing | Mock | Error handling |
| **NetworkPlugin** | ✅ Working | N/A | None |
| **PacketAnalyzerPlugin** | ⚠️ Graceful fallback | Mock | Requires root for real capture |

---

## 🔧 Implementation Tasks

### Task 1: WiFi Plugin Enhancement
**Priority:** HIGH  
**Complexity:** MEDIUM

**Current Issues:**
- Error messages not user-friendly
- No detection of interface if auto-detect fails
- Security info not reliably captured

**Subtasks:**
- [x] Verify nmcli/iwconfig availability
- [ ] Test real WiFi data collection with `wlp0s20f3`
- [ ] Improve error messages (user-friendly)
- [ ] Add fallback chain: nmcli → iwconfig → /proc/net/wireless → mock
- [ ] Parse security type reliably (WPA2, WPA3, Open)
- [ ] Add validation for signal strength ranges
- [ ] Handle disconnected state gracefully

**Acceptance Criteria:**
- WiFi dashboard shows real signal strength, SSID, channel
- Graceful degradation if no WiFi available
- Clear error messages guide user on how to fix issues
- No crashes, only warnings

---

### Task 2: Network Plugin Enhancement
**Priority:** MEDIUM  
**Complexity:** LOW

**Current State:**
- Basic bandwidth calculation working
- Connection counting working

**Enhancements:**
- [ ] Add per-interface breakdown (optional, advanced mode)
- [ ] Improve connection state filtering (show only relevant states)
- [ ] Add connection protocol breakdown (TCP vs UDP)
- [ ] Cache results to avoid excessive psutil calls
- [ ] Add network interface up/down detection

**Acceptance Criteria:**
- Network dashboard shows accurate real-time bandwidth
- Connection counts are meaningful (exclude TIME_WAIT, etc.)
- No performance degradation from excessive polling

---

### Task 3: Packet Analyzer Real Mode
**Priority:** HIGH  
**Complexity:** HIGH

**Current State:**
- Graceful fallback to mock mode working ✅
- Scapy installed ✅
- Needs root permissions for packet capture

**Strategy:**
1. **Don't require root by default** - use fallback
2. **Detect capabilities at runtime** - test if can capture
3. **Guide user if they want real capture** - documentation

**Subtasks:**
- [ ] Test Scapy packet capture with current permissions
- [ ] Implement permission check (can we capture?)
- [ ] If no permission: show educational message + fallback to mock
- [ ] Add capability detection: `getcap` check for Python binary
- [ ] Document setcap approach: `sudo setcap cap_net_raw+ep $(which python3)`
- [ ] Add "Demo Mode" flag in UI showing when using mock vs real

**Acceptance Criteria:**
- Packet capture works if user has permissions
- Graceful fallback to mock if no permissions
- UI clearly indicates mock vs real capture
- Documentation explains how to enable real capture

---

### Task 4: Health Checks & Monitoring
**Priority:** MEDIUM  
**Complexity:** LOW

**Goal:** Dashboard shows plugin health status

**Subtasks:**
- [ ] Add `get_health()` method to base Plugin class
- [ ] Each plugin reports: HEALTHY, DEGRADED, MOCK, FAILED
- [ ] Add health indicator in footer or header
- [ ] Show warning icon if any plugin in degraded state
- [ ] Implement health check interval (every 30s)

**Health States:**
```python
HEALTHY   = Real data, working correctly
DEGRADED  = Real data, but with issues (e.g., weak signal)
MOCK      = Using simulated data
FAILED    = Plugin initialization failed
```

**UI Integration:**
- Footer shows: `📊 All Systems Healthy` or `⚠️ 2 Plugins Mock Mode`
- Click for details modal

---

### Task 5: Documentation & Permissions Guide
**Priority:** HIGH  
**Complexity:** LOW

**Goal:** User can easily set up real mode

**Documents to Create:**
- [ ] `REAL_MODE_SETUP.md` - Complete setup guide
- [ ] `PERMISSIONS.md` - Detailed permissions explanation
- [ ] `TROUBLESHOOTING.md` - Common issues and fixes
- [ ] Update main README.md with links

**REAL_MODE_SETUP.md Contents:**
```markdown
# Real Mode Setup Guide

## Quick Start (Mock Mode - No Setup)
python3 app_textual.py --mock

## Real Mode - System Metrics Only
python3 app_textual.py
# Works: CPU, RAM, Disk, WiFi (nmcli), Network (psutil)
# Mock: Packet capture (needs permissions)

## Real Mode - Full Packet Capture (Requires Root)

### Option 1: Run with sudo (NOT RECOMMENDED)
sudo python3 app_textual.py

### Option 2: Grant capability to Python (RECOMMENDED)
sudo setcap cap_net_raw+ep $(which python3)
python3 app_textual.py

### Option 3: Use demo mode
python3 app_textual.py --demo
# Real metrics + mock packet capture
```

---

### Task 6: Error Handling & User Feedback
**Priority:** HIGH  
**Complexity:** MEDIUM

**Current Issues:**
- Errors are too technical (stack traces)
- User doesn't know what went wrong or how to fix

**Improvements:**
- [ ] Catch all plugin initialization errors
- [ ] Show user-friendly error messages
- [ ] Provide actionable guidance ("Run with sudo" or "Install nmcli")
- [ ] Add `--verbose` flag for technical debugging
- [ ] Log errors to file (wifi_dashboard.log) for troubleshooting

**Example Error Messages:**
```
❌ WiFi Plugin Failed
   Reason: No WiFi interface detected
   Solution: Connect to WiFi or specify interface with --interface wlp0s20f3
   Fallback: Using mock data for demonstration

⚠️  Packet Capture Unavailable
   Reason: Permission denied (requires root)
   Solution: 
     1. Run with: sudo python3 app_textual.py
     2. Or grant capability: sudo setcap cap_net_raw+ep $(which python3)
     3. Or use --mock flag for educational simulation
   Fallback: Using mock packet data
```

---

## 🧪 Testing Plan

### Manual Tests

**Test 1: WiFi Plugin Real Mode**
```bash
python3 app_textual.py
# Press 3 (WiFi Dashboard)
# Verify: Real SSID, signal strength, channel shown
# Expected: Real data from wlp0s20f3
```

**Test 2: Network Plugin Real Mode**
```bash
python3 app_textual.py
# Press 2 (Network Dashboard)
# Open browser, download file
# Verify: Bandwidth graph shows spike
# Expected: Real-time bandwidth changes
```

**Test 3: Packet Capture (No Root)**
```bash
python3 app_textual.py
# Press 4 (Packets Dashboard)
# Verify: Warning message shown
# Verify: Falls back to mock data
# Verify: Educational tips still visible
# Expected: Graceful degradation
```

**Test 4: Full Real Mode (With Root)**
```bash
sudo python3 app_textual.py
# Press 4 (Packets Dashboard)
# Verify: Real packets captured
# Verify: HTTPS/HTTP flags match real traffic
# Expected: Real packet data
```

---

## 📊 Success Metrics

| Metric | Target | Validation |
|--------|--------|------------|
| WiFi Plugin Uptime | >95% | No crashes when WiFi available |
| Network Plugin Accuracy | ±5% | Compare with `iftop` output |
| Packet Capture Coverage | 100% | All packets logged when root |
| Error Recovery | 100% | No fatal errors, only warnings |
| User Satisfaction | Subjective | Clear error messages, no confusion |

---

## 🚀 Deployment Checklist

Before marking Sprint 4 complete:

- [ ] All plugins tested in real mode
- [ ] Documentation complete and reviewed
- [ ] Error messages are user-friendly
- [ ] Health checks implemented
- [ ] Permissions guide tested on clean Ubuntu install
- [ ] No crashes in any mode (mock, real, real+sudo)
- [ ] Git commit with detailed changelog
- [ ] README.md updated with Sprint 4 status

---

## 🎯 Sprint 4 Definition of Done

**Sprint 4 is COMPLETE when:**

1. ✅ WiFi Plugin reliably collects real data when WiFi available
2. ✅ Network Plugin shows accurate real-time bandwidth
3. ✅ Packet Analyzer works with root OR gracefully falls back
4. ✅ Health monitoring shows plugin status in UI
5. ✅ Documentation guides user through real mode setup
6. ✅ Error messages are actionable and user-friendly
7. ✅ No crashes in any operational mode
8. ✅ LEI < 1.0 (no placeholders, complete code)
9. ✅ 100% Constituição Vértice compliance

---

**Soli Deo Gloria** ✝️
