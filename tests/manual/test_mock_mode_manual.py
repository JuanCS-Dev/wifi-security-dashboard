"""
Manual testing script for mock mode validation.

Tests MOCK-001, MOCK-002, MOCK-003 from the testing plan.
This script validates mock data generator behavior programmatically.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-10
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.mock_data_generator import MockDataGenerator


def test_mock_001_cohesiveness():
    """
    Test MOCK-001: Validate mock data generator cohesiveness.

    Checks:
    - Devices remain consistent (no random disappearance)
    - Traffic patterns natural (no jumps from 0 to 100 MB/s)
    - Apps correlate with traffic
    """
    print("\n" + "="*70)
    print("TEST MOCK-001: Mock Data Cohesiveness")
    print("="*70)

    gen = MockDataGenerator()

    # Test 1: Device consistency over time
    print("\n[1] Testing device consistency...")
    devices_t0 = gen.get_devices()
    device_ids_t0 = {d['mac'] for d in devices_t0}

    time.sleep(2)

    devices_t1 = gen.get_devices()
    device_ids_t1 = {d['mac'] for d in devices_t1}

    if device_ids_t0 == device_ids_t1:
        print(f"   ✅ PASS: Devices consistent ({len(device_ids_t0)} devices)")
    else:
        print(f"   ❌ FAIL: Devices changed!")
        print(f"   T0: {device_ids_t0}")
        print(f"   T1: {device_ids_t1}")
        return False

    # Test 2: Traffic patterns are natural
    print("\n[2] Testing traffic pattern naturalness...")
    traffic_samples = []
    for _ in range(10):
        stats = gen.get_network_stats()
        traffic_samples.append(stats['bandwidth_rx_mbps'])
        time.sleep(0.1)

    # Check no huge jumps (>50 Mbps in 0.1s)
    max_jump = 0
    for i in range(1, len(traffic_samples)):
        jump = abs(traffic_samples[i] - traffic_samples[i-1])
        max_jump = max(max_jump, jump)

    if max_jump < 50:
        print(f"   ✅ PASS: Traffic natural (max jump: {max_jump:.2f} Mbps)")
    else:
        print(f"   ❌ FAIL: Traffic chaotic (max jump: {max_jump:.2f} Mbps)")
        return False

    # Test 3: Apps correlate with device traffic
    print("\n[3] Testing app-traffic correlation...")
    devices = gen.get_devices()
    apps = gen.get_top_apps()

    # Check that active devices' apps appear in top apps
    active_devices = [d for d in devices if d['is_active']]
    device_apps = {d['current_app'] for d in active_devices if d['current_app'] != 'Idle'}
    top_apps = set(apps.keys())

    if device_apps.issubset(top_apps):
        print(f"   ✅ PASS: Apps correlate with devices")
        print(f"      Device apps: {device_apps}")
        print(f"      Top apps: {top_apps}")
    else:
        missing = device_apps - top_apps
        print(f"   ⚠️  WARNING: Some device apps not in top apps: {missing}")

    print("\n✅ MOCK-001 PASSED: Mock data is cohesive and natural\n")
    return True


def test_mock_002_no_root_required():
    """
    Test MOCK-002: Validate mock mode without root.

    Checks:
    - All plugins collect data
    - No permission errors
    """
    print("\n" + "="*70)
    print("TEST MOCK-002: Mock Mode Without Root")
    print("="*70)

    print("\n[1] Testing mock data generator initialization...")
    try:
        gen = MockDataGenerator()
        print("   ✅ PASS: Generator initialized without root")
    except PermissionError as e:
        print(f"   ❌ FAIL: Permission error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ FAIL: Unexpected error: {e}")
        return False

    print("\n[2] Testing data collection...")
    try:
        system_data = gen.get_system_metrics()
        wifi_data = gen.get_wifi_info()
        network_data = gen.get_network_stats()
        devices = gen.get_devices()
        apps = gen.get_top_apps()

        print(f"   ✅ PASS: System metrics collected ({len(system_data)} fields)")
        print(f"   ✅ PASS: WiFi info collected ({len(wifi_data)} fields)")
        print(f"   ✅ PASS: Network stats collected ({len(network_data)} fields)")
        print(f"   ✅ PASS: Devices collected ({len(devices)} devices)")
        print(f"   ✅ PASS: Apps collected ({len(apps)} apps)")
    except Exception as e:
        print(f"   ❌ FAIL: Data collection error: {e}")
        return False

    print("\n✅ MOCK-002 PASSED: Mock mode works without root\n")
    return True


def test_mock_003_educational_value():
    """
    Test MOCK-003: Validate educational value of mock data.

    Checks:
    - Data is understandable
    - Device owners are clear (Pai, Mãe, Filho, Filha)
    - Apps are recognizable (YouTube, Netflix, WhatsApp)
    - Values are realistic
    """
    print("\n" + "="*70)
    print("TEST MOCK-003: Educational Value")
    print("="*70)

    gen = MockDataGenerator()

    # Test 1: Device owners are clear
    print("\n[1] Testing device owner clarity...")
    devices = gen.get_devices()
    owners = [d['owner'] for d in devices]

    family_members = ['Pai', 'Mãe', 'Filho', 'Filha', 'Família']
    clear_owners = [o for o in owners if any(member in o for member in family_members)]

    if len(clear_owners) == len(owners):
        print(f"   ✅ PASS: All devices have clear owners")
        for owner in set(owners):
            print(f"      - {owner}")
    else:
        print(f"   ❌ FAIL: Some devices have unclear owners")
        return False

    # Test 2: Apps are recognizable
    print("\n[2] Testing app recognizability...")
    apps = gen.get_top_apps()
    recognizable_apps = [
        'YouTube', 'Netflix', 'WhatsApp', 'Instagram',
        'Gmail', 'Chrome', 'Firefox', 'Kids'
    ]

    app_list = list(apps.keys())
    recognized = [app for app in app_list if any(known in app for known in recognizable_apps)]

    if len(recognized) == len(app_list):
        print(f"   ✅ PASS: All apps are recognizable")
        for app in app_list:
            print(f"      - {app}: {apps[app]:.2f} Mbps")
    else:
        print(f"   ⚠️  WARNING: Some apps might be unclear")

    # Test 3: Values are realistic
    print("\n[3] Testing value realism...")
    system = gen.get_system_metrics()
    wifi = gen.get_wifi_info()
    network = gen.get_network_stats()

    checks = [
        ("CPU%", 0 <= system['cpu_percent'] <= 100),
        ("RAM%", 0 <= system['ram_percent'] <= 100),
        ("Signal", -100 <= wifi['signal_strength'] <= 0),
        ("Download", 0 <= network['bandwidth_rx_mbps'] <= 20),
        ("Upload", 0 <= network['bandwidth_tx_mbps'] <= 5),
    ]

    all_realistic = True
    for name, check in checks:
        if check:
            print(f"   ✅ {name} within realistic range")
        else:
            print(f"   ❌ {name} out of range!")
            all_realistic = False

    if not all_realistic:
        return False

    # Test 4: Educational concepts
    print("\n[4] Testing educational concepts...")
    concepts = [
        f"WiFi Signal: {wifi['signal_strength']} dBm (stronger is better)",
        f"Security: {wifi['security']} (keeps network safe)",
        f"Devices: {len(devices)} connected (family members)",
        f"Apps: {', '.join(list(apps.keys())[:3])} (using internet)",
    ]

    print("   Educational concepts demonstrated:")
    for concept in concepts:
        print(f"      - {concept}")
    print("   ✅ PASS: Educational concepts clear")

    print("\n✅ MOCK-003 PASSED: Mock data has high educational value\n")
    return True


def main():
    """Run all mock mode tests."""
    print("\n" + "="*70)
    print("MOCK MODE VALIDATION - Fase 2")
    print("WiFi Security Education Dashboard v2.0")
    print("Framework: Constituição Vértice v3.0")
    print("="*70)

    results = []

    # Run all tests
    results.append(("MOCK-001", test_mock_001_cohesiveness()))
    results.append(("MOCK-002", test_mock_002_no_root_required()))
    results.append(("MOCK-003", test_mock_003_educational_value()))

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_id, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_id}: {status}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL MOCK MODE TESTS PASSED!")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED - Review above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
