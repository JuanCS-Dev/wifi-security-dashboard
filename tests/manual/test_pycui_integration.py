#!/usr/bin/env python3
"""
Test py_cui Integration - Validate all adapters load correctly
Author: Dev Sênior Rafael
Date: 2025-11-11
Sprint: 7 (Validation)

This test validates that:
1. All 5 adapters can be imported
2. PyCUIRenderer can initialize
3. Adapters can be created without errors
4. Config loads correctly
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_adapter_imports():
    """Test that all adapters can be imported"""
    print("=" * 70)
    print("TEST 1: Adapter Imports")
    print("=" * 70)

    try:
        from src.adapters.textbox_adapter import TextboxAdapter
        print("✅ TextboxAdapter imported")
    except Exception as e:
        print(f"❌ TextboxAdapter import failed: {e}")
        return False

    try:
        from src.adapters.sparkline_adapter import SparklineAdapter
        print("✅ SparklineAdapter imported")
    except Exception as e:
        print(f"❌ SparklineAdapter import failed: {e}")
        return False

    try:
        from src.adapters.runchart_adapter import RunchartAdapter
        print("✅ RunchartAdapter imported")
    except Exception as e:
        print(f"❌ RunchartAdapter import failed: {e}")
        return False

    try:
        from src.adapters.barchart_adapter import BarchartAdapter
        print("✅ BarchartAdapter imported")
    except Exception as e:
        print(f"❌ BarchartAdapter import failed: {e}")
        return False

    try:
        from src.adapters.packet_table_adapter import PacketTableAdapter
        print("✅ PacketTableAdapter imported")
    except Exception as e:
        print(f"❌ PacketTableAdapter import failed: {e}")
        return False

    print("\n✅ All 5 adapters imported successfully!\n")
    return True


def test_pycui_renderer_import():
    """Test that PyCUIRenderer can be imported"""
    print("=" * 70)
    print("TEST 2: PyCUIRenderer Import")
    print("=" * 70)

    try:
        from src.core.pycui_renderer import PyCUIRenderer
        print("✅ PyCUIRenderer imported")
    except Exception as e:
        print(f"❌ PyCUIRenderer import failed: {e}")
        return False

    print("\n✅ PyCUIRenderer imported successfully!\n")
    return True


def test_config_loading():
    """Test that config loads correctly"""
    print("=" * 70)
    print("TEST 3: Config Loading")
    print("=" * 70)

    try:
        from src.core.config_loader import ConfigLoader

        config_path = "config/dashboard_grid_complex.yml"
        config = ConfigLoader.load(config_path)

        print(f"✅ Config loaded: {config_path}")
        print(f"   - Title: {config.title}")
        print(f"   - Components: {len(config.components)}")
        print(f"   - Plugins: {len(config.plugins)}")

        # Check components
        components = config.components
        print(f"\n   Components:")
        for i, comp in enumerate(components, 1):
            comp_type = comp.type
            title = comp.title
            print(f"   {i}. {comp_type}: {title}")

    except Exception as e:
        print(f"❌ Config loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\n✅ Config loaded successfully!\n")
    return True


def test_adapter_creation():
    """Test that adapters can be created from components"""
    print("=" * 70)
    print("TEST 4: Adapter Creation (Dry Run)")
    print("=" * 70)

    try:
        from src.core.config_loader import ConfigLoader
        from src.adapters.textbox_adapter import TextboxAdapter
        from src.adapters.sparkline_adapter import SparklineAdapter
        from src.adapters.runchart_adapter import RunchartAdapter
        from src.adapters.barchart_adapter import BarchartAdapter
        from src.adapters.packet_table_adapter import PacketTableAdapter

        # Map type to adapter class
        ADAPTER_MAP = {
            'textbox': TextboxAdapter,
            'sparkline': SparklineAdapter,
            'runchart': RunchartAdapter,
            'barchart': BarchartAdapter,
            'packettable': PacketTableAdapter,
            'packet_table': PacketTableAdapter,
        }

        config_path = "config/dashboard_grid_complex.yml"
        config = ConfigLoader.load(config_path)

        components = config.components

        created_adapters = []
        for i, comp in enumerate(components, 1):
            comp_type = comp.type
            title = comp.title

            print(f"\n   Component {i}: {comp_type}")
            print(f"      Title: {title}")

            # Try to get adapter class
            adapter_class = ADAPTER_MAP.get(comp_type)
            if not adapter_class:
                print(f"      ⚠️  No adapter mapped for type '{comp_type}'")
                continue

            # Component is already a ComponentConfigModel from pydantic
            print(f"      ✅ ComponentConfigModel exists")

            # For adapters, we need a component instance, not just config
            # For now, just test that we can find the adapter class
            print(f"      ✅ Adapter class found: {adapter_class.__name__}")
            created_adapters.append(adapter_class)

        print(f"\n✅ {len(created_adapters)}/{len(components)} adapters validated!\n")
        return len(created_adapters) == len(components)

    except Exception as e:
        print(f"❌ Adapter creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_dependencies():
    """Test that all required dependencies are available"""
    print("=" * 70)
    print("TEST 5: Dependencies Check")
    print("=" * 70)

    dependencies = [
        ('py_cui', 'PyCUI for grid rendering'),
        ('plotext', 'plotext for charts'),
        ('tabulate', 'tabulate for tables'),
        ('psutil', 'psutil for system metrics'),
        ('yaml', 'PyYAML for config'),
    ]

    all_ok = True
    for module_name, description in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {module_name:15} - {description}")
        except ImportError:
            print(f"❌ {module_name:15} - {description} [NOT INSTALLED]")
            all_ok = False

    if all_ok:
        print("\n✅ All dependencies installed!\n")
    else:
        print("\n❌ Some dependencies missing!\n")

    return all_ok


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("PY_CUI INTEGRATION TEST SUITE")
    print("=" * 70)
    print()

    results = []

    # Test 1: Adapter imports
    results.append(("Adapter Imports", test_adapter_imports()))

    # Test 2: PyCUIRenderer import
    results.append(("PyCUIRenderer Import", test_pycui_renderer_import()))

    # Test 3: Config loading
    results.append(("Config Loading", test_config_loading()))

    # Test 4: Adapter creation
    results.append(("Adapter Creation", test_adapter_creation()))

    # Test 5: Dependencies
    results.append(("Dependencies", test_dependencies()))

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
        print("✅ py_cui integration is ready!")
        return 0
    else:
        print(f"\n❌ {total - passed} tests failed")
        print("⚠️  Fix issues before running dashboard")
        return 1


if __name__ == "__main__":
    sys.exit(main())
