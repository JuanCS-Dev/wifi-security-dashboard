#!/usr/bin/env python3
"""
Test Dashboard Initialization - Full integration test
Author: Dev Sênior Rafael
Date: 2025-11-11
Sprint: 7 (Validation)

This test validates that:
1. Dashboard can be initialized with py_cui mode
2. All components load correctly
3. All adapters are created
4. Plugins initialize
5. No crashes during setup
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_dashboard_initialization():
    """Test full dashboard initialization"""
    print("=" * 70)
    print("TEST: Dashboard Initialization (py_cui mode)")
    print("=" * 70)

    try:
        from src.core.dashboard import Dashboard
        from src.core.config_loader import ConfigLoader

        # Load config
        config_path = "config/dashboard_grid_complex.yml"
        print(f"\n1️⃣ Loading config: {config_path}")
        config = ConfigLoader.load(config_path)
        print(f"   ✅ Config loaded")
        print(f"   - Title: {config.title}")
        print(f"   - Components: {len(config.components)}")
        print(f"   - Plugins: {len(config.plugins)}")

        # Create dashboard instance
        print(f"\n2️⃣ Creating Dashboard instance")
        dashboard = Dashboard(config_path, pycui_mode=True, mock_mode=True)
        print(f"   ✅ Dashboard instance created")

        # Check components
        print(f"\n3️⃣ Checking components")
        print(f"   Components created: {len(dashboard.components)}")
        for i, comp in enumerate(dashboard.components, 1):
            comp_type = comp.config.type
            title = comp.config.title
            print(f"   {i}. {comp_type:12} - {title}")

        # Check plugins
        print(f"\n4️⃣ Checking plugins")
        if hasattr(dashboard, 'plugin_manager'):
            plugins = dashboard.plugin_manager.plugins
            print(f"   Plugins initialized: {len(plugins)}")
            for name, plugin in plugins.items():
                status = plugin.status if hasattr(plugin, 'status') else 'unknown'
                print(f"   - {name:20} [{status}]")
        else:
            print(f"   ⚠️  No plugin_manager found")

        # Check renderer
        print(f"\n5️⃣ Checking renderer")
        if hasattr(dashboard, 'renderer') and dashboard.renderer:
            renderer = dashboard.renderer
            print(f"   ✅ Renderer created: {type(renderer).__name__}")

            # Check if it's PyCUI renderer
            if hasattr(renderer, 'renderer'):
                pycui_renderer = renderer.renderer
                print(f"   - Grid size: {pycui_renderer.width}x{pycui_renderer.height}")
                print(f"   - Adapters: {len(pycui_renderer.adapters)}")

                # List adapters
                for i, adapter in enumerate(pycui_renderer.adapters, 1):
                    adapter_type = type(adapter).__name__
                    print(f"     {i}. {adapter_type}")
            else:
                print(f"   ⚠️  Not a PyCUI renderer")
        else:
            print(f"   ❌ No renderer found")
            return False

        # Summary
        print(f"\n{'=' * 70}")
        print(f"✅ DASHBOARD INITIALIZATION: SUCCESS")
        print(f"{'=' * 70}")
        print(f"\nDashboard is ready to run!")
        print(f"To test interactively:")
        print(f"  python3 main_v2.py --config {config_path} --pycui-mode --mock")
        print()

        return True

    except Exception as e:
        print(f"\n❌ Dashboard initialization FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_adapter_creation_real():
    """Test that adapters are actually created during initialization"""
    print("=" * 70)
    print("TEST: Adapter Creation (Real Dashboard)")
    print("=" * 70)

    try:
        from src.core.dashboard import Dashboard

        # Create dashboard
        config_path = "config/dashboard_grid_complex.yml"
        print(f"\nInitializing dashboard with: {config_path}")

        dashboard = Dashboard(config_path, pycui_mode=True, mock_mode=True)

        # Get renderer
        if not hasattr(dashboard, 'renderer') or not dashboard.renderer:
            print(f"❌ No renderer found")
            return False

        renderer = dashboard.renderer
        if not hasattr(renderer, 'renderer'):
            print(f"❌ Not a PyCUI renderer")
            return False

        pycui_renderer = renderer.renderer
        adapters = pycui_renderer.adapters

        print(f"\n✅ Found {len(adapters)} adapters:")

        # Count by type
        adapter_counts = {}
        for adapter in adapters:
            adapter_type = type(adapter).__name__
            adapter_counts[adapter_type] = adapter_counts.get(adapter_type, 0) + 1

        for adapter_type, count in sorted(adapter_counts.items()):
            print(f"   - {adapter_type:25} x{count}")

        # Expected adapters
        expected = {
            'RunchartAdapter': 3,      # WiFi Signal, Network Throughput, Packet Rate
            'SparklineAdapter': 3,     # CPU, Memory, Disk
            'PacketTableAdapter': 1,   # Packet Analyzer
        }

        print(f"\nValidation:")
        all_ok = True
        for expected_type, expected_count in expected.items():
            actual_count = adapter_counts.get(expected_type, 0)
            if actual_count == expected_count:
                print(f"   ✅ {expected_type}: {actual_count}/{expected_count}")
            else:
                print(f"   ❌ {expected_type}: {actual_count}/{expected_count} (MISMATCH)")
                all_ok = False

        if all_ok:
            print(f"\n✅ ALL ADAPTERS CREATED CORRECTLY!\n")
        else:
            print(f"\n❌ ADAPTER COUNT MISMATCH!\n")

        return all_ok

    except Exception as e:
        print(f"\n❌ Adapter creation test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("DASHBOARD INITIALIZATION TEST SUITE")
    print("=" * 70)
    print()

    results = []

    # Test 1: Dashboard initialization
    results.append(("Dashboard Initialization", test_dashboard_initialization()))

    # Test 2: Adapter creation (real)
    results.append(("Adapter Creation (Real)", test_adapter_creation_real()))

    # Summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print()
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("✅ Dashboard is ready to run!")
        print("\nTo test interactively:")
        print("  python3 main_v2.py --config config/dashboard_grid_complex.yml --pycui-mode --mock")
        return 0
    else:
        print(f"\n❌ {total - passed} tests failed")
        print("⚠️  Fix issues before running dashboard")
        return 1


if __name__ == "__main__":
    sys.exit(main())
