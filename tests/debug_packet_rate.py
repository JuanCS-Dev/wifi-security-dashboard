#!/usr/bin/env python3
"""
Debug script para investigar por que Packet Rate não renderiza.

Author: Dev Sênior Rafael
Date: 2025-11-11
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    print("=" * 70)
    print("DEBUG: Packet Rate Component")
    print("=" * 70)

    from src.core.dashboard import Dashboard
    from src.utils.mock_data_generator import MockDataGenerator

    # 1. Test mock data generation
    print("\n1️⃣  Testing mock data generation...")
    mock_gen = MockDataGenerator()
    network_data = mock_gen.get_network_stats()
    print(f"   Network data keys: {list(network_data.keys())}")
    print(f"   bandwidth_tx_mbps: {network_data.get('bandwidth_tx_mbps')}")

    if 'bandwidth_tx_mbps' not in network_data:
        print("   ❌ bandwidth_tx_mbps NOT FOUND in mock data!")
        return 1

    print("   ✅ bandwidth_tx_mbps present in mock data")

    # 2. Create dashboard and check Packet Rate component
    print("\n2️⃣  Checking Packet Rate component...")
    dashboard = Dashboard("config/dashboard_grid_complex.yml", pycui_mode=False, mock_mode=True)

    # Find Packet Rate component
    packet_rate = None
    for comp in dashboard.components:
        if "Packet Rate" in comp.config.title:
            packet_rate = comp
            break

    if not packet_rate:
        print("   ❌ Packet Rate component NOT FOUND!")
        return 1

    print(f"   ✅ Packet Rate component found")
    print(f"   - Title: {packet_rate.config.title}")
    print(f"   - Type: {packet_rate.config.type}")
    print(f"   - Plugin: {packet_rate.config.plugin}")
    print(f"   - Data field: {packet_rate.config.data_field}")
    print(f"   - Position: x={packet_rate.config.position.x}, y={packet_rate.config.position.y}, "
          f"w={packet_rate.config.position.width}, h={packet_rate.config.position.height}")

    # 3. Test adapter creation
    print("\n3️⃣  Testing adapter creation...")
    adapter = dashboard._create_adapter_for_component(packet_rate)

    if not adapter:
        print("   ❌ Adapter creation FAILED!")
        return 1

    print(f"   ✅ Adapter created: {type(adapter).__name__}")
    print(f"   - Max samples: {adapter.max_samples}")
    print(f"   - Marker: {adapter.marker}")
    print(f"   - History size: {len(adapter.history)}")

    # Create a fake widget (adapter needs widget to update)
    class FakeWidget:
        def __init__(self):
            self.text = ""
        def set_text(self, text):
            self.text = text

    adapter.widget = FakeWidget()
    print(f"   ✅ Fake widget attached to adapter")

    # 4. Test data update
    print("\n4️⃣  Testing data update...")

    # Simulate multiple updates - CALL ADAPTER, NOT COMPONENT
    for i in range(10):
        plugin_data = dashboard.plugin_manager.get_all_plugin_data()

        if 'network' not in plugin_data:
            print(f"   ❌ 'network' plugin data not available!")
            return 1

        network_vals = plugin_data['network']
        if 'bandwidth_tx_mbps' not in network_vals:
            print(f"   ❌ 'bandwidth_tx_mbps' field not in network plugin data!")
            print(f"   Available fields: {list(network_vals.keys())}")
            return 1

        # CRITICAL: Update ADAPTER, not component (adapter maintains history in py_cui mode)
        adapter.update_widget(plugin_data)

    print(f"   ✅ Updated 10 times")
    print(f"   - Current value: {packet_rate.data}")
    print(f"   - Adapter history size: {len(adapter.history)}")
    print(f"   - Adapter history: {list(adapter.history)}")

    # 5. Test chart generation
    print("\n5️⃣  Testing chart generation...")

    if len(adapter.history) == 0:
        print("   ⚠️  History is EMPTY - no data to generate chart!")
        print("   This could be why Packet Rate appears empty in UI")
        return 1

    chart = adapter._generate_chart()
    print(f"   ✅ Chart generated")
    print(f"   - Chart length: {len(chart)} chars")
    print(f"   - First 200 chars: {chart[:200]}")

    if len(chart) < 50:
        print("   ⚠️  Chart is very short - might appear empty!")
        return 1

    if "Packet Rate" not in chart:
        print("   ⚠️  Chart doesn't contain title!")

    print("\n" + "=" * 70)
    print("✅ ALL CHECKS PASSED")
    print("=" * 70)
    print("\nPacket Rate component should be working correctly.")
    print("If it still appears empty in UI, the issue is likely:")
    print("  1. Update timing (not enough time to accumulate data)")
    print("  2. Widget refresh rate")
    print("  3. py_cui rendering issue")

    return 0

if __name__ == "__main__":
    sys.exit(main())
