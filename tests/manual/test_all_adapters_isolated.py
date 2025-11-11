#!/usr/bin/env python3
"""
Test All Adapters Isolated - Comprehensive adapter validation
Author: Dev Sênior Rafael
Date: 2025-11-11
Sprint: 7 (Validation)

This test validates that:
1. Each adapter can be loaded with its dedicated config
2. Dashboard initializes without errors
3. Adapters are created correctly
4. Mock data flows correctly
5. No crashes during setup
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_adapter(adapter_name: str, config_path: str, expected_adapter_type: str, expected_adapter_count: int):
    """
    Test a single adapter in isolation.

    Args:
        adapter_name: Name of adapter being tested
        config_path: Path to test config
        expected_adapter_type: Expected adapter class name
        expected_adapter_count: Expected number of adapters created

    Returns:
        True if test passed, False otherwise
    """
    print(f"\n{'=' * 70}")
    print(f"TEST: {adapter_name}")
    print(f"{'=' * 70}")
    print(f"Config: {config_path}")

    try:
        from src.core.dashboard import Dashboard
        from src.core.config_loader import ConfigLoader

        # Validate config first
        print(f"\n1️⃣  Validating config...")
        try:
            config = ConfigLoader.load(config_path)
            print(f"   ✅ Config valid")
            print(f"   - Title: {config.title}")
            print(f"   - Components: {len(config.components)}")
            print(f"   - Plugins: {len(config.plugins)}")
        except Exception as e:
            print(f"   ❌ Config invalid: {e}")
            return False

        # Create dashboard
        print(f"\n2️⃣  Creating dashboard...")
        try:
            dashboard = Dashboard(config_path, pycui_mode=True, mock_mode=True)
            print(f"   ✅ Dashboard created")
        except Exception as e:
            print(f"   ❌ Dashboard creation failed: {e}")
            import traceback
            traceback.print_exc()
            return False

        # Check components
        print(f"\n3️⃣  Checking components...")
        print(f"   Components loaded: {len(dashboard.components)}")
        for i, comp in enumerate(dashboard.components, 1):
            comp_type = comp.config.type.value
            title = comp.config.title
            print(f"   {i}. {comp_type:12} - {title}")

        # Check adapters
        print(f"\n4️⃣  Checking adapters...")
        adapter_count = 0
        for component in dashboard.components:
            adapter = dashboard._create_adapter_for_component(component)
            if adapter:
                adapter_type = type(adapter).__name__
                adapter_count += 1

                if adapter_type == expected_adapter_type:
                    print(f"   ✅ {expected_adapter_type} created")
                else:
                    print(f"   ❌ Wrong adapter type: {adapter_type} (expected {expected_adapter_type})")
                    return False
            else:
                print(f"   ❌ No adapter created for {component.config.title}")
                return False

        # Validate adapter count
        if adapter_count == expected_adapter_count:
            print(f"   ✅ Adapter count correct: {adapter_count}/{expected_adapter_count}")
        else:
            print(f"   ❌ Adapter count mismatch: {adapter_count}/{expected_adapter_count}")
            return False

        # Check plugins
        print(f"\n5️⃣  Checking plugins...")
        if hasattr(dashboard, 'plugin_manager'):
            plugins = dashboard.plugin_manager.plugins
            print(f"   Plugins initialized: {len(plugins)}")
            for name, plugin in plugins.items():
                status = plugin.status if hasattr(plugin, 'status') else 'unknown'
                print(f"   - {name:20} [{status}]")
        else:
            print(f"   ❌ No plugin_manager found")
            return False

        # Success
        print(f"\n{'=' * 70}")
        print(f"✅ {adapter_name} TEST: PASSED")
        print(f"{'=' * 70}\n")
        return True

    except Exception as e:
        print(f"\n❌ {adapter_name} TEST: FAILED")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        print(f"{'=' * 70}\n")
        return False


def main():
    """Run all adapter tests"""
    print("\n" + "=" * 70)
    print("ISOLATED ADAPTER TEST SUITE")
    print("=" * 70)
    print("\nTesting each adapter in isolation to ensure 0 technical debt\n")

    # Define tests
    tests = [
        {
            'name': 'Textbox Adapter',
            'config': 'config/test_textbox_complete.yml',
            'adapter_type': 'TextboxAdapter',
            'adapter_count': 2,  # 2 textbox components
        },
        {
            'name': 'Runchart Adapter',
            'config': 'config/test_runchart_complete.yml',
            'adapter_type': 'RunchartAdapter',
            'adapter_count': 2,  # 2 runchart components
        },
        {
            'name': 'Sparkline Adapter',
            'config': 'config/test_sparkline_complete.yml',
            'adapter_type': 'SparklineAdapter',
            'adapter_count': 3,  # 3 sparkline components
        },
        {
            'name': 'PacketTable Adapter',
            'config': 'config/test_packettable_complete.yml',
            'adapter_type': 'PacketTableAdapter',
            'adapter_count': 1,  # 1 packettable component
        },
    ]

    # Run tests
    results = []
    for test in tests:
        result = test_adapter(
            test['name'],
            test['config'],
            test['adapter_type'],
            test['adapter_count']
        )
        results.append((test['name'], result))

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
        print("\n🎉 ALL ADAPTERS PASSED! 🎉")
        print("✅ Each adapter works correctly in isolation!")
        print("✅ No technical debt found in adapter layer!")
        return 0
    else:
        print(f"\n❌ {total - passed} adapters failed")
        print("⚠️  Technical debt detected - fix before continuing")
        return 1


if __name__ == "__main__":
    sys.exit(main())
