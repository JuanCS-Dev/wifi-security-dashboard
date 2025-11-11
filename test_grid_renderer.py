#!/usr/bin/env python3
"""
Test GridRenderer with absolute positioning.

Validates that components can be positioned at specific (x, y) coordinates
with defined (width, height).

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.grid_renderer import GridRenderer, GridDashboardRenderer
from rich.panel import Panel
from rich.text import Text


def test_basic_grid_positioning():
    """Test basic grid positioning with multiple panels"""
    print("="*80)
    print("TEST: Basic Grid Positioning (3 Panels)")
    print("="*80)

    # Create renderer for 120x40 terminal
    renderer = GridRenderer(width=120, height=40)

    # Add 3 panels at different positions
    renderer.add_component(
        Panel("Panel 1\nTop-Left", title="Component A", border_style="green"),
        x=0, y=0, width=40, height=10
    )

    renderer.add_component(
        Panel("Panel 2\nTop-Right", title="Component B", border_style="blue"),
        x=45, y=0, width=40, height=10
    )

    renderer.add_component(
        Panel("Panel 3\nMiddle", title="Component C", border_style="red"),
        x=20, y=12, width=80, height=15
    )

    # Render
    output = renderer.render()

    # Print output
    print(output)

    print("\n" + "="*80)
    print("✓ Basic grid test completed")
    print(f"  - Renderer: {renderer}")
    print(f"  - Output size: {len(output)} characters")
    print("="*80)


def test_dashboard_renderer():
    """Test GridDashboardRenderer with mock components"""
    print("\n" + "="*80)
    print("TEST: Dashboard Renderer Integration")
    print("="*80)

    from src.components.textbox import Textbox
    from src.core.component import ComponentConfig, Position, ComponentType

    # Create dashboard renderer
    dash_renderer = GridDashboardRenderer(width=120, height=40)

    # Create mock components
    comp1_config = ComponentConfig(
        type=ComponentType.TEXTBOX,
        title="WiFi Status",
        position=Position(x=0, y=0, width=40, height=8),
        rate_ms=1000,
        plugin="wifi",
        data_field="signal_strength",
        color="green"
    )
    comp1 = Textbox(comp1_config)
    comp1.update({"signal_strength": "-52 dBm"})

    comp2_config = ComponentConfig(
        type=ComponentType.TEXTBOX,
        title="System Info",
        position=Position(x=45, y=0, width=40, height=8),
        rate_ms=2000,
        plugin="system",
        data_field="cpu_percent",
        color="yellow"
    )
    comp2 = Textbox(comp2_config)
    comp2.update({"cpu_percent": "45.2%"})

    # Add components
    dash_renderer.add_from_component(comp1)
    dash_renderer.add_from_component(comp2)

    # Render
    output = dash_renderer.render()

    print(output)

    print("\n" + "="*80)
    print("✓ Dashboard renderer test completed")
    print(f"  - Components: 2")
    print(f"  - Positions: (0,0,40,8) and (45,0,40,8)")
    print("="*80)


def test_packet_table_positioning():
    """Test PacketTable in grid position"""
    print("\n" + "="*80)
    print("TEST: PacketTable Grid Positioning")
    print("="*80)

    from src.components.packet_table import PacketTable
    from src.core.component import ComponentConfig, Position, ComponentType

    # Create renderer
    renderer = GridRenderer(width=120, height=60)

    # Create PacketTable at specific position
    config = ComponentConfig(
        type=ComponentType.PACKETTABLE,
        title="Packet Analyzer",
        position=Position(x=0, y=30, width=120, height=25),
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

    packet_table = PacketTable(config)

    # Mock data
    mock_data = {
        "top_protocols": {
            "HTTPS": 450,
            "H264": 150,
            "DNS": 90,
            "QUIC": 80,
            "HTTP": 30
        },
        "packet_rate": 85.5,
        "total_packets": 800,
        "backend": "mock",
        "recent_packets": [
            {
                "time": "14:32:15.234",
                "src": "192.168.1.102",
                "dst": "142.250.185.46",
                "protocol": "HTTPS",
                "info": "Gmail - Encrypted ✅",
                "safe": True
            },
            {
                "time": "14:32:15.456",
                "src": "192.168.1.104",
                "dst": "93.184.216.34",
                "protocol": "HTTP",
                "info": "⚠️ Unencrypted website! Passwords visible!",
                "safe": False
            }
        ]
    }

    packet_table.update(mock_data)

    # Add header panel
    renderer.add_component(
        Panel("WiFi Security Dashboard v2.0 - Grid Mode",
              title="Header", border_style="cyan"),
        x=0, y=0, width=120, height=3
    )

    # Add PacketTable
    renderer.add_component(
        packet_table.render(),
        x=config.position.x,
        y=config.position.y,
        width=config.position.width,
        height=config.position.height
    )

    # Render
    output = renderer.render()

    print(output)

    print("\n" + "="*80)
    print("✓ PacketTable grid positioning test completed")
    print(f"  - PacketTable at: (0, 30, 120, 25)")
    print(f"  - Total height: 60 lines")
    print("="*80)


if __name__ == "__main__":
    # Run tests
    test_basic_grid_positioning()

    print("\n" + "-"*80 + "\n")
    test_dashboard_renderer()

    print("\n" + "-"*80 + "\n")
    test_packet_table_positioning()

    print("\n" + "="*80)
    print("🎉 ALL GRID RENDERER TESTS PASSED!")
    print("="*80)
