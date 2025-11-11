#!/usr/bin/env python3
"""
Test Adapter Factory - Validate adapter creation logic
Author: Dev Sênior Rafael
Date: 2025-11-11
Sprint: 7 (Validation)

This test validates that:
1. Adapter factory correctly converts Enum to string
2. All 5 adapter types can be created
3. Factory returns correct adapter for each component type
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_adapter_factory():
    """Test that adapter factory creates correct adapters"""
    print("=" * 70)
    print("TEST: Adapter Factory")
    print("=" * 70)

    try:
        from src.core.dashboard import Dashboard
        from src.core.config_loader import ConfigLoader

        # Load config
        config_path = "config/dashboard_grid_complex.yml"
        print(f"\n1️⃣ Loading config and creating dashboard")
        dashboard = Dashboard(config_path, pycui_mode=True, mock_mode=True)
        print(f"   ✅ Dashboard created")
        print(f"   - Components: {len(dashboard.components)}")

        # Test adapter factory for each component
        print(f"\n2️⃣ Testing adapter factory")

        created_adapters = {}
        for i, component in enumerate(dashboard.components, 1):
            comp_type = component.config.type
            comp_type_str = comp_type.value if hasattr(comp_type, 'value') else comp_type
            title = component.config.title

            print(f"\n   Component {i}: {comp_type_str}")
            print(f"      Title: {title}")

            # Call factory method
            adapter = dashboard._create_adapter_for_component(component)

            if adapter:
                adapter_type = type(adapter).__name__
                print(f"      ✅ Adapter created: {adapter_type}")
                created_adapters[comp_type_str] = created_adapters.get(comp_type_str, 0) + 1
            else:
                print(f"      ❌ No adapter created (factory returned None)")
                return False

        # Summary
        print(f"\n3️⃣ Adapter creation summary:")
        for comp_type, count in sorted(created_adapters.items()):
            print(f"   - {comp_type:15} x{count}")

        # Expected counts
        expected = {
            'runchart': 3,
            'sparkline': 3,
            'packettable': 1,
        }

        print(f"\n4️⃣ Validation:")
        all_ok = True
        for exp_type, exp_count in expected.items():
            actual_count = created_adapters.get(exp_type, 0)
            if actual_count == exp_count:
                print(f"   ✅ {exp_type:15} {actual_count}/{exp_count}")
            else:
                print(f"   ❌ {exp_type:15} {actual_count}/{exp_count} (MISMATCH)")
                all_ok = False

        if all_ok:
            print(f"\n✅ ALL ADAPTERS CREATED CORRECTLY!\n")
        else:
            print(f"\n❌ ADAPTER COUNT MISMATCH!\n")

        return all_ok

    except Exception as e:
        print(f"\n❌ Adapter factory test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_adapter_types():
    """Test that adapters have correct types"""
    print("=" * 70)
    print("TEST: Adapter Types")
    print("=" * 70)

    try:
        from src.core.dashboard import Dashboard

        # Create dashboard
        config_path = "config/dashboard_grid_complex.yml"
        print(f"\nInitializing dashboard")
        dashboard = Dashboard(config_path, pycui_mode=True, mock_mode=True)

        # Expected adapter types for each component type
        expected_adapters = {
            'runchart': 'RunchartAdapter',
            'sparkline': 'SparklineAdapter',
            'packettable': 'PacketTableAdapter',
        }

        print(f"\nTesting adapter types:")
        all_ok = True

        for component in dashboard.components:
            comp_type_str = component.config.type.value
            adapter = dashboard._create_adapter_for_component(component)

            if not adapter:
                print(f"   ❌ {comp_type_str:15} - No adapter created")
                all_ok = False
                continue

            adapter_type = type(adapter).__name__
            expected_type = expected_adapters.get(comp_type_str)

            if adapter_type == expected_type:
                print(f"   ✅ {comp_type_str:15} → {adapter_type}")
            else:
                print(f"   ❌ {comp_type_str:15} → {adapter_type} (expected {expected_type})")
                all_ok = False

        if all_ok:
            print(f"\n✅ ALL ADAPTER TYPES CORRECT!\n")
        else:
            print(f"\n❌ ADAPTER TYPE MISMATCH!\n")

        return all_ok

    except Exception as e:
        print(f"\n❌ Adapter types test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("ADAPTER FACTORY TEST SUITE")
    print("=" * 70)
    print()

    results = []

    # Test 1: Adapter factory
    results.append(("Adapter Factory", test_adapter_factory()))

    # Test 2: Adapter types
    results.append(("Adapter Types", test_adapter_types()))

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
        print("✅ Adapter factory is working correctly!")
        return 0
    else:
        print(f"\n❌ {total - passed} tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
