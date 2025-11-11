#!/usr/bin/env python3
"""
Visual Validation Test - ANSI Code Detection in Adapters

This test validates that ALL adapters produce ANSI-free output suitable for py_cui/curses.

Author: Dev Sênior Rafael
Date: 2025-11-11
Sprint: 8 (Critical Fix - ANSI Rendering)

Purpose:
    Verify that the ANSI stripping fix is correctly applied to all adapters
    that use libraries (plotext, etc.) that generate ANSI codes.

Test Strategy:
    1. Create each adapter with mock data
    2. Generate output from each adapter
    3. Verify output contains NO ANSI escape codes
    4. Verify output DOES contain expected content (charts, tables, etc.)
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.ansi_stripper import has_ansi_codes
from src.core.component import ComponentConfig, Position, ComponentType


def test_runchart_adapter_no_ansi():
    """Test that Runchart adapter produces ANSI-free output"""
    print("\n" + "=" * 70)
    print("TEST: Runchart Adapter - ANSI-Free Output")
    print("=" * 70)

    try:
        from src.components.runchart import Runchart
        from src.adapters.runchart_adapter import RunchartAdapter

        # Create component config
        config = ComponentConfig(
            type=ComponentType.RUNCHART,
            title="CPU Usage Runchart",
            position=Position(x=0, y=0, width=120, height=16),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent",
            color="green",
            triggers=[],
            extra={"max_samples": 60, "marker": "braille"}
        )

        # Create component and adapter
        component = Runchart(config)
        adapter = RunchartAdapter(component)

        # Generate chart with mock data
        for i in range(10):
            adapter.history.append(float(40 + i * 2))

        chart_output = adapter._generate_chart()

        # Validate: NO ANSI codes
        if has_ansi_codes(chart_output):
            print(f"   ❌ ANSI codes detected in output!")
            print(f"   First 200 chars: {repr(chart_output[:200])}")
            return False

        # Validate: DOES contain expected content
        if len(chart_output) < 10:
            print(f"   ❌ Output too short (empty chart?)")
            return False

        print(f"   ✅ Runchart output is ANSI-free")
        print(f"   ✅ Chart length: {len(chart_output)} chars")
        print(f"   ✅ Contains title: {'CPU Usage Runchart' in chart_output}")
        return True

    except Exception as e:
        print(f"   ❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_barchart_adapter_no_ansi():
    """Test that Barchart adapter produces ANSI-free output"""
    print("\n" + "=" * 70)
    print("TEST: Barchart Adapter - ANSI-Free Output")
    print("=" * 70)

    try:
        from src.components.barchart import Barchart
        from src.adapters.barchart_adapter import BarchartAdapter

        # Create component config
        config = ComponentConfig(
            type=ComponentType.BARCHART,
            title="Protocol Distribution",
            position=Position(x=0, y=0, width=120, height=20),
            rate_ms=1000,
            plugin="network",
            data_field="protocol_distribution",
            color="cyan",
            triggers=[],
            extra={"orientation": "horizontal", "max_bars": 10}
        )

        # Create component and adapter
        component = Barchart(config)
        adapter = BarchartAdapter(component)

        # Generate chart with mock data
        mock_data = {
            "HTTPS": 450,
            "DNS": 89,
            "HTTP": 34,
            "SSH": 12,
            "FTP": 5
        }

        categories, values = adapter._parse_data(mock_data)
        chart_output = adapter._generate_chart(categories, values)

        # Validate: NO ANSI codes
        if has_ansi_codes(chart_output):
            print(f"   ❌ ANSI codes detected in output!")
            print(f"   First 200 chars: {repr(chart_output[:200])}")
            return False

        # Validate: DOES contain expected content
        if len(chart_output) < 10:
            print(f"   ❌ Output too short (empty chart?)")
            return False

        print(f"   ✅ Barchart output is ANSI-free")
        print(f"   ✅ Chart length: {len(chart_output)} chars")
        print(f"   ✅ Contains title: {'Protocol Distribution' in chart_output}")
        return True

    except Exception as e:
        print(f"   ❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_sparkline_adapter_no_ansi():
    """Test that Sparkline adapter produces ANSI-free output"""
    print("\n" + "=" * 70)
    print("TEST: Sparkline Adapter - ANSI-Free Output")
    print("=" * 70)

    try:
        from src.components.sparkline import Sparkline
        from src.adapters.sparkline_adapter import SparklineAdapter

        # Create component config
        config = ComponentConfig(
            type=ComponentType.SPARKLINE,
            title="CPU Usage",
            position=Position(x=0, y=0, width=40, height=10),
            rate_ms=1000,
            plugin="system",
            data_field="cpu_percent",
            color="green",
            triggers=[],
            extra={"max_samples": 40, "label": "CPU"}
        )

        # Create component and adapter
        component = Sparkline(config)
        adapter = SparklineAdapter(component)

        # Generate sparkline with mock data
        for i in range(20):
            adapter.history.append(float(40 + i * 2))

        sparkline_output = adapter._build_sparkline_text(60.0)

        # Validate: NO ANSI codes
        if has_ansi_codes(sparkline_output):
            print(f"   ❌ ANSI codes detected in output!")
            print(f"   Output: {repr(sparkline_output)}")
            return False

        # Validate: DOES contain expected content (Unicode sparkline chars)
        if not any(c in sparkline_output for c in "▁▂▃▄▅▆▇█"):
            print(f"   ❌ No sparkline Unicode chars found")
            return False

        print(f"   ✅ Sparkline output is ANSI-free")
        print(f"   ✅ Output length: {len(sparkline_output)} chars")
        print(f"   ✅ Contains Unicode sparkline: {any(c in sparkline_output for c in '▁▂▃▄▅▆▇█')}")
        print(f"   ✅ Sample output: {sparkline_output}")
        return True

    except Exception as e:
        print(f"   ❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_packettable_adapter_no_ansi():
    """Test that PacketTable adapter produces ANSI-free output"""
    print("\n" + "=" * 70)
    print("TEST: PacketTable Adapter - ANSI-Free Output")
    print("=" * 70)

    try:
        from src.components.packet_table import PacketTable
        from src.adapters.packet_table_adapter import PacketTableAdapter

        # Create component config
        config = ComponentConfig(
            type=ComponentType.PACKETTABLE,
            title="Packet Analyzer",
            position=Position(x=0, y=0, width=120, height=44),
            rate_ms=1000,
            plugin="packet_analyzer",
            data_field="packets",
            color="yellow",
            triggers=[],
            extra={"show_protocols": True, "show_recent": True, "max_protocols": 6, "max_recent": 5}
        )

        # Create component and adapter
        component = PacketTable(config)
        adapter = PacketTableAdapter(component)

        # Generate table with mock data
        mock_protocols = {
            "HTTPS": 450,
            "DNS": 89,
            "HTTP": 34
        }

        table_output = adapter._format_protocols(mock_protocols)

        # Validate: NO ANSI codes
        if has_ansi_codes(table_output):
            print(f"   ❌ ANSI codes detected in output!")
            print(f"   First 200 chars: {repr(table_output[:200])}")
            return False

        # Validate: DOES contain expected content (tabulate table)
        if "Protocol" not in table_output or "Packets" not in table_output:
            print(f"   ❌ Table headers not found")
            return False

        print(f"   ✅ PacketTable output is ANSI-free")
        print(f"   ✅ Table length: {len(table_output)} chars")
        print(f"   ✅ Contains table headers: True")
        return True

    except Exception as e:
        print(f"   ❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_textbox_adapter_no_ansi():
    """Test that Textbox adapter produces ANSI-free output"""
    print("\n" + "=" * 70)
    print("TEST: Textbox Adapter - ANSI-Free Output")
    print("=" * 70)

    try:
        from src.components.textbox import Textbox
        from src.adapters.textbox_adapter import TextboxAdapter

        # Create component config
        config = ComponentConfig(
            type=ComponentType.TEXTBOX,
            title="WiFi SSID",
            position=Position(x=0, y=0, width=40, height=3),
            rate_ms=1000,
            plugin="wifi",
            data_field="ssid",
            color="cyan",
            triggers=[],
            extra={"label": "Connected to"}
        )

        # Create component and adapter
        component = Textbox(config)
        adapter = TextboxAdapter(component)

        # Generate text with mock data
        # Note: TextboxAdapter uses _format_value(), not _format_text()
        text_output = adapter._format_value("MyWiFi-5G")

        # Validate: NO ANSI codes
        if has_ansi_codes(text_output):
            print(f"   ❌ ANSI codes detected in output!")
            print(f"   Output: {repr(text_output)}")
            return False

        # Validate: DOES contain expected content
        if "MyWiFi-5G" not in text_output:
            print(f"   ❌ Expected content not found")
            return False

        print(f"   ✅ Textbox output is ANSI-free")
        print(f"   ✅ Output: {text_output}")
        return True

    except Exception as e:
        print(f"   ❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all visual validation tests"""
    print("\n" + "=" * 70)
    print("VISUAL VALIDATION: ANSI-FREE OUTPUT CHECK")
    print("=" * 70)
    print("\nPurpose: Verify that all adapters produce curses-compatible output")
    print("(i.e., NO ANSI escape codes that would appear as garbage in py_cui)")
    print()

    results = []

    # Test all adapters
    results.append(("Runchart Adapter", test_runchart_adapter_no_ansi()))
    results.append(("Barchart Adapter", test_barchart_adapter_no_ansi()))
    results.append(("Sparkline Adapter", test_sparkline_adapter_no_ansi()))
    results.append(("PacketTable Adapter", test_packettable_adapter_no_ansi()))
    results.append(("Textbox Adapter", test_textbox_adapter_no_ansi()))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status:10} - {name}")

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("✅ All adapters produce ANSI-free output")
        print("✅ Output is curses/py_cui compatible")
        print("✅ No more garbage characters in the UI!")
        print("\n📝 Next step: Run full dashboard visually to confirm fix")
        return 0
    else:
        print(f"\n❌ {total - passed} TEST(S) FAILED")
        print("⚠️  Fix failing adapters before proceeding")
        return 1


if __name__ == "__main__":
    sys.exit(main())
