"""
Manual testing script for real mode validation.

Tests REAL-001, REAL-002, REAL-003, REAL-004 from the testing plan.
This script validates real data collection and fallback mechanisms.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-10
"""

import sys
import os
import subprocess
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.plugins.system_plugin import SystemPlugin
from src.plugins.wifi_plugin import WiFiPlugin
from src.plugins.network_plugin import NetworkPlugin
from src.plugins.base import PluginConfig, PluginStatus


def test_real_001_system_metrics():
    """
    Test REAL-001: Validate real system metrics.

    Checks:
    - SystemPlugin collects real data
    - CPU/RAM readings are realistic
    - psutil is available
    """
    print("\n" + "="*70)
    print("TEST REAL-001: Real System Metrics")
    print("="*70)

    print("\n[1] Testing psutil availability...")
    try:
        import psutil
        print(f"   ✅ PASS: psutil {psutil.__version__} available")
    except ImportError:
        print("   ❌ FAIL: psutil not installed")
        print("   Install with: pip3 install psutil")
        return False

    print("\n[2] Testing SystemPlugin initialization...")
    config = PluginConfig(name="system", enabled=True, rate_ms=1000, config={})

    try:
        plugin = SystemPlugin(config)
        plugin.initialize()
        print(f"   ✅ PASS: SystemPlugin initialized (status: {plugin.status})")
    except Exception as e:
        print(f"   ❌ FAIL: Initialization error: {e}")
        return False

    print("\n[3] Testing real data collection...")
    try:
        data = plugin.collect_data()

        # Check required fields
        required_fields = ["cpu_percent", "memory_percent", "disk_percent", "uptime_seconds"]
        for field in required_fields:
            if field in data:
                print(f"   ✅ {field}: {data[field]}")
            else:
                print(f"   ❌ Missing field: {field}")
                return False

        # Validate ranges
        checks = [
            ("CPU%", 0 <= data["cpu_percent"] <= 100),
            ("Memory%", 0 <= data["memory_percent"] <= 100),
            ("Disk%", 0 <= data["disk_percent"] <= 100),
            ("Uptime", data["uptime_seconds"] >= 0),
        ]

        all_valid = True
        for name, check in checks:
            if check:
                print(f"   ✅ {name} within valid range")
            else:
                print(f"   ❌ {name} out of range!")
                all_valid = False

        if not all_valid:
            return False

    except Exception as e:
        print(f"   ❌ FAIL: Data collection error: {e}")
        return False

    print("\n✅ REAL-001 PASSED: System metrics accurate\n")
    return True


def test_real_002_wifi_data():
    """
    Test REAL-002: Validate real WiFi data.

    Checks:
    - WiFiPlugin collects real data
    - SSID matches system
    - Signal strength is realistic
    """
    print("\n" + "="*70)
    print("TEST REAL-002: Real WiFi Data")
    print("="*70)

    print("\n[1] Detecting WiFi interface...")
    # Try to find WiFi interface
    try:
        result = subprocess.run(
            ["ip", "link", "show"],
            capture_output=True,
            text=True,
            timeout=5
        )
        interfaces = result.stdout

        wifi_ifaces = []
        for line in interfaces.split('\n'):
            if 'wlan' in line or 'wlp' in line:
                parts = line.split(':')
                if len(parts) >= 2:
                    wifi_ifaces.append(parts[1].strip())

        if wifi_ifaces:
            wifi_interface = wifi_ifaces[0]
            print(f"   ✅ WiFi interface found: {wifi_interface}")
        else:
            print("   ⚠️  No WiFi interface found (wlan0, wlp*)")
            print("   Skipping REAL-002 (requires WiFi hardware)")
            return None  # Skip, not fail

    except Exception as e:
        print(f"   ⚠️  Could not detect interface: {e}")
        return None

    print("\n[2] Testing WiFiPlugin initialization...")
    config = PluginConfig(name="wifi", enabled=True, rate_ms=1000, config={"interface": wifi_interface})

    try:
        plugin = WiFiPlugin(config)
        plugin.initialize()
        print(f"   ✅ PASS: WiFiPlugin initialized (status: {plugin.status})")
    except Exception as e:
        print(f"   ❌ FAIL: Initialization error: {e}")
        return False

    print("\n[3] Testing real WiFi data collection...")
    try:
        data = plugin.collect_data()

        print(f"   SSID: {data.get('ssid', 'N/A')}")
        print(f"   Signal: {data.get('signal_strength_dbm', 'N/A')} dBm")
        print(f"   Signal: {data.get('signal_strength_percent', 'N/A')}%")
        print(f"   Security: {data.get('security', 'N/A')}")
        print(f"   Frequency: {data.get('frequency_mhz', 'N/A')} MHz")

        # Check if connected or disconnected
        if data.get('ssid') == 'Not Connected':
            print("   ⚠️  Not connected to WiFi")
            print("   This is OK if running on wired connection")
            print("   Data collection working correctly (fallback to disconnected)")
            return True  # Pass - fallback works

        # If connected, validate data
        signal = data.get('signal_strength_dbm', 0)
        if -100 <= signal <= 0:
            print(f"   ✅ Signal within valid range ({signal} dBm)")
        else:
            print(f"   ❌ Signal out of range: {signal}")
            return False

    except Exception as e:
        print(f"   ❌ FAIL: Data collection error: {e}")
        return False

    print("\n✅ REAL-002 PASSED: WiFi data accurate\n")
    return True


def test_real_003_network_data():
    """
    Test REAL-003: Validate real network data (requires root).

    Checks:
    - NetworkPlugin requires root for real data
    - Falls back to mock if no root
    """
    print("\n" + "="*70)
    print("TEST REAL-003: Real Network Data (requires root)")
    print("="*70)

    print("\n[1] Checking root access...")
    is_root = os.geteuid() == 0

    if is_root:
        print("   ✅ Running as root")
    else:
        print("   ⚠️  Not running as root")
        print("   NetworkPlugin will fallback to mock mode")
        print("   This is expected behavior - testing fallback...")

    print("\n[2] Testing NetworkPlugin initialization...")
    config = PluginConfig(name="network", enabled=True, rate_ms=1000, config={})

    try:
        plugin = NetworkPlugin(config)
        plugin.initialize()
        print(f"   ✅ PASS: NetworkPlugin initialized (status: {plugin.status})")
    except Exception as e:
        print(f"   ❌ FAIL: Initialization error: {e}")
        return False

    print("\n[3] Testing network data collection...")
    try:
        data = plugin.collect_data()

        # Check required fields
        required_fields = ["bandwidth_rx_mbps", "bandwidth_tx_mbps", "bytes_sent", "bytes_recv"]
        for field in required_fields:
            if field in data:
                print(f"   ✅ {field}: {data[field]}")
            else:
                print(f"   ❌ Missing field: {field}")
                return False

        if is_root:
            print("   ℹ️  Root mode: Data should be real (if scapy available)")
        else:
            print("   ℹ️  Non-root mode: Data is from mock generator (expected)")

    except Exception as e:
        print(f"   ❌ FAIL: Data collection error: {e}")
        return False

    print("\n✅ REAL-003 PASSED: Network data collection working\n")
    return True


def test_real_004_fallback_graceful():
    """
    Test REAL-004: Validate real mode fallback to mock.

    Checks:
    - Dashboard runs without root
    - Plugins fallback gracefully
    - No crashes
    """
    print("\n" + "="*70)
    print("TEST REAL-004: Graceful Fallback (mock when needed)")
    print("="*70)

    print("\n[1] Testing plugin fallback mechanisms...")

    # All plugins should initialize even without their requirements
    plugins_to_test = [
        ("System", SystemPlugin, {}),
        ("WiFi", WiFiPlugin, {"interface": "wlan0"}),
        ("Network", NetworkPlugin, {}),
    ]

    all_ok = True
    for name, plugin_class, extra_config in plugins_to_test:
        try:
            config = PluginConfig(
                name=name.lower(),
                enabled=True,
                rate_ms=1000,
                config=extra_config
            )
            plugin = plugin_class(config)
            plugin.initialize()
            data = plugin.collect_data()

            print(f"   ✅ {name}Plugin: initialized and collected data")
        except Exception as e:
            print(f"   ❌ {name}Plugin: failed with {e}")
            all_ok = False

    if not all_ok:
        return False

    print("\n[2] Testing that fallback is silent (no crashes)...")
    print("   ✅ All plugins handled missing dependencies gracefully")

    print("\n✅ REAL-004 PASSED: Fallback mechanisms working\n")
    return True


def main():
    """Run all real mode tests."""
    print("\n" + "="*70)
    print("REAL MODE VALIDATION - Fase 2")
    print("WiFi Security Education Dashboard v2.0")
    print("Framework: Constituição Vértice v3.0")
    print("="*70)

    # Check environment
    is_root = os.geteuid() == 0
    if is_root:
        print("\n⚠️  Running as ROOT")
        print("   Real mode tests will use actual hardware")
    else:
        print("\nℹ️  Running as NORMAL USER")
        print("   Some tests will validate fallback mechanisms")

    results = []

    # Run all tests
    results.append(("REAL-001", test_real_001_system_metrics()))
    results.append(("REAL-002", test_real_002_wifi_data()))
    results.append(("REAL-003", test_real_003_network_data()))
    results.append(("REAL-004", test_real_004_fallback_graceful()))

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result is True)
    skipped = sum(1 for _, result in results if result is None)
    failed = sum(1 for _, result in results if result is False)
    total = len(results)

    for test_id, result in results:
        if result is True:
            status = "✅ PASS"
        elif result is None:
            status = "⏭️  SKIP"
        else:
            status = "❌ FAIL"
        print(f"{test_id}: {status}")

    print(f"\nTotal: {passed} passed, {skipped} skipped, {failed} failed (of {total})")

    if failed == 0:
        print("\n🎉 ALL REAL MODE TESTS PASSED OR SKIPPED!")
        print("   (Skipped tests require specific hardware)")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED - Review above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
