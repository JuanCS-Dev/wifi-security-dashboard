#!/usr/bin/env python3
"""
Integration test for PacketTable component with PacketAnalyzerPlugin.

This script validates:
1. PacketTable instantiation
2. Data flow from PacketAnalyzerPlugin
3. Rendering without errors
4. Content validation

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.components.packet_table import PacketTable
from src.plugins.packet_analyzer_plugin import PacketAnalyzerPlugin
from src.core.component import ComponentConfig, Position, ComponentType
from src.plugins.base import PluginConfig


def test_packet_table_integration():
    """Test complete integration of PacketTable + PacketAnalyzerPlugin"""
    print("="*80)
    print("TESTE DE INTEGRAÇÃO: PacketTable + PacketAnalyzerPlugin")
    print("="*80)

    # Step 1: Create PacketAnalyzerPlugin in mock mode
    print("\n[1] Criando PacketAnalyzerPlugin (mock mode)...")
    plugin_config = PluginConfig(
        name="packet_analyzer",
        enabled=True,
        rate_ms=2000,
        config={
            "interface": "wlan0",
            "capture_count": 100,
            "capture_timeout": 1,
            "mock_mode": True
        }
    )

    plugin = PacketAnalyzerPlugin(plugin_config)
    plugin.initialize()
    print(f"   ✓ Plugin status: {plugin.status}")
    print(f"   ✓ Backend: {plugin._backend}")

    # Step 2: Collect data from plugin
    print("\n[2] Coletando dados do plugin...")
    plugin_data = plugin.collect_data()
    print(f"   ✓ Data keys: {list(plugin_data.keys())}")
    print(f"   ✓ Protocols: {len(plugin_data.get('protocols', {}))} tipos")
    print(f"   ✓ Recent packets: {len(plugin_data.get('recent_packets', []))} pacotes")

    # Step 3: Create PacketTable component
    print("\n[3] Criando componente PacketTable...")
    component_config = ComponentConfig(
        type=ComponentType.PACKETTABLE,
        title="Packet Analyzer (Wireshark-style)",
        position=Position(x=0, y=43, width=120, height=18),
        rate_ms=2000,
        plugin="packet_analyzer",
        data_field="all",
        color="red",
        extra={
            "show_protocols": True,
            "show_recent": True,
            "max_protocols": 6,
            "max_recent": 5
        }
    )

    packet_table = PacketTable(component_config)
    print(f"   ✓ Component created: {packet_table}")

    # Step 4: Update component with plugin data
    print("\n[4] Atualizando componente com dados do plugin...")
    packet_table.update(plugin_data)
    print(f"   ✓ Component data updated")
    print(f"   ✓ Has data: {packet_table.data is not None}")

    # Step 5: Render component
    print("\n[5] Renderizando componente...")
    try:
        panel = packet_table.render()
        print(f"   ✓ Render successful: {type(panel).__name__}")

        # Check panel properties
        print(f"   ✓ Panel title: {panel.title if hasattr(panel, 'title') else 'N/A'}")
        print(f"   ✓ Panel border_style: {panel.border_style if hasattr(panel, 'border_style') else 'N/A'}")

        # Render to string to check content
        from rich.console import Console
        from io import StringIO

        console = Console(file=StringIO(), width=120)
        console.print(panel)
        output = console.file.getvalue()

        # Validate content
        print("\n[6] Validando conteúdo renderizado...")
        checks = [
            ("Top Protocols" in output, "Top Protocols section"),
            ("📦 Recent Packets" in output or "Recent Packets" in output, "Recent Packets section"),
            ("HTTPS" in output or "HTTP" in output, "Protocol names"),
            ("packets" in output.lower() or "pkts" in output.lower(), "'packets' keyword"),
        ]

        all_passed = True
        for check, description in checks:
            status = "✓" if check else "✗"
            print(f"   {status} {description}: {'PASS' if check else 'FAIL'}")
            if not check:
                all_passed = False

        # Print sample output
        print("\n[7] Sample output (primeiras 30 linhas):")
        print("-" * 80)
        for i, line in enumerate(output.split('\n')[:30], 1):
            print(f"{i:2d}: {line}")
        print("-" * 80)

        # Final result
        print("\n" + "="*80)
        if all_passed:
            print("✅ INTEGRAÇÃO COMPLETA: PacketTable renderizado com sucesso!")
            print("✅ FASE 1.4 CONCLUÍDA: Validação visual programática OK")
        else:
            print("⚠️  Alguns checks falharam - verificar output acima")
        print("="*80)

        return all_passed

    except Exception as e:
        print(f"   ✗ Render failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_packet_table_integration()
    sys.exit(0 if success else 1)
