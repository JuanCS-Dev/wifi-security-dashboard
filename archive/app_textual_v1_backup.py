#!/usr/bin/env python3
"""
WiFi Security Education Dashboard v3.0 - Textual Version

Complete UI refactoring using Textual framework for modern, reactive, flicker-free rendering.

Author: Juan-Dev - Soli Deo Gloria ✝️
Date: 2025-11-11

Usage:
    python app_textual.py                    # Run with default settings
    python app_textual.py --mock            # Run with mock data
    python app_textual.py --help            # Show help
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, Any

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static
from textual.reactive import reactive

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.plugins.system_plugin import SystemPlugin
from src.plugins.wifi_plugin import WiFiPlugin
from src.plugins.network_plugin import NetworkPlugin
from src.plugins.packet_analyzer_plugin import PacketAnalyzerPlugin
from src.plugins.base import PluginConfig
from src.widgets import NetworkChart, PacketTable


class CPUWidget(Static):
    """
    Reactive CPU usage widget.

    Automatically updates when cpu_percent changes.
    Shows visual bar with color-coded percentage.
    """

    cpu_percent = reactive(0.0)

    def watch_cpu_percent(self, new_value: float) -> None:
        """Called automatically when cpu_percent changes."""
        # Color-coded based on usage
        if new_value < 70:
            color = "green"
            status = "NORMAL"
        elif new_value < 90:
            color = "yellow"
            status = "HIGH"
        else:
            color = "red"
            status = "CRITICAL"

        # Visual progress bar (20 chars)
        bar_length = 20
        filled = int(bar_length * new_value / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        # Update widget content
        self.update(
            f"[bold bright_white]💻 CPU USAGE[/bold bright_white]\n"
            f"[{color}]{bar}[/{color}]\n"
            f"[bold {color}]{new_value:.1f}%[/bold {color}] [{color}]{status}[/{color}]"
        )


class RAMWidget(Static):
    """
    Reactive RAM usage widget.

    Shows memory usage with visual bar and percentage.
    """

    memory_percent = reactive(0.0)
    memory_used_mb = reactive(0.0)
    memory_total_mb = reactive(0.0)

    def watch_memory_percent(self, new_value: float) -> None:
        """Called automatically when memory_percent changes."""
        # Color-coded based on usage
        if new_value < 70:
            color = "green"
            status = "NORMAL"
        elif new_value < 90:
            color = "yellow"
            status = "HIGH"
        else:
            color = "red"
            status = "CRITICAL"

        # Visual progress bar (20 chars)
        bar_length = 20
        filled = int(bar_length * new_value / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        # Format memory values
        used_gb = self.memory_used_mb / 1024
        total_gb = self.memory_total_mb / 1024

        # Update widget content
        self.update(
            f"[bold bright_white]📊 RAM USAGE[/bold bright_white]\n"
            f"[{color}]{bar}[/{color}]\n"
            f"[bold {color}]{new_value:.1f}%[/bold {color}] [{color}]{status}[/{color}]\n"
            f"[dim]{used_gb:.1f}/{total_gb:.1f} GB[/dim]"
        )


class DiskWidget(Static):
    """
    Reactive Disk usage widget.

    Shows disk usage with visual bar and percentage.
    """

    disk_percent = reactive(0.0)
    disk_used_gb = reactive(0.0)
    disk_total_gb = reactive(0.0)

    def watch_disk_percent(self, new_value: float) -> None:
        """Called automatically when disk_percent changes."""
        # Color-coded based on usage
        if new_value < 70:
            color = "cyan"
            status = "GOOD"
        elif new_value < 90:
            color = "yellow"
            status = "WARNING"
        else:
            color = "red"
            status = "CRITICAL"

        # Visual progress bar (20 chars)
        bar_length = 20
        filled = int(bar_length * new_value / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        # Update widget content
        self.update(
            f"[bold bright_white]💾 DISK USAGE[/bold bright_white]\n"
            f"[{color}]{bar}[/{color}]\n"
            f"[bold {color}]{new_value:.1f}%[/bold {color}] [{color}]{status}[/{color}]\n"
            f"[dim]{self.disk_used_gb:.0f}/{self.disk_total_gb:.0f} GB[/dim]"
        )


class WiFiWidget(Static):
    """
    Reactive WiFi signal widget.

    Shows WiFi signal strength with visual indicator.
    """

    signal_strength_percent = reactive(0)
    ssid = reactive("N/A")
    signal_dbm = reactive(-100)

    def watch_signal_strength_percent(self, new_value: int) -> None:
        """Called automatically when signal strength changes."""
        # Color and visual based on signal strength
        if new_value >= 70:
            color = "green"
            bars = "📶"  # Full signal
            status = "EXCELLENT"
        elif new_value >= 50:
            color = "green"
            bars = "📶"  # Good signal
            status = "GOOD"
        elif new_value >= 30:
            color = "yellow"
            bars = "📶"  # Fair signal
            status = "FAIR"
        elif new_value > 0:
            color = "red"
            bars = "📶"  # Poor signal
            status = "WEAK"
        else:
            color = "dim"
            bars = "📵"  # No signal
            status = "NO SIGNAL"

        # Visual progress bar (20 chars)
        bar_length = 20
        filled = int(bar_length * new_value / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        # Update widget content
        self.update(
            f"[bold bright_white]{bars} WIFI SIGNAL[/bold bright_white]\n"
            f"[{color}]{bar}[/{color}]\n"
            f"[bold {color}]{new_value}%[/bold {color}] [{color}]{status}[/{color}]\n"
            f"[dim]{self.ssid} ({self.signal_dbm} dBm)[/dim]"
        )


class WiFiSecurityDashboard(App):
    """
    WiFi Security Education Dashboard v3.0

    Modern, reactive dashboard using Textual framework.
    Features:
    - Zero flickering (diff rendering)
    - Reactive widgets (auto-update)
    - Beautiful, aligned layouts (CSS)
    - Real-time metrics (10 FPS)
    """

    CSS = """
    #sidebar {
        width: 35;
        dock: left;
        background: $panel;
    }

    #main {
        width: 1fr;
        background: $surface;
    }

    CPUWidget, RAMWidget, DiskWidget, WiFiWidget {
        height: 9;
        border: solid green;
        margin: 1 1 1 2;
        padding: 1;
        background: $surface;
    }

    RAMWidget {
        border: solid green;
    }

    DiskWidget {
        border: solid cyan;
    }

    WiFiWidget {
        border: solid yellow;
    }

    Header {
        background: $accent;
    }

    Footer {
        background: $panel;
    }

    NetworkChart {
        height: 50%;
        border: solid cyan;
        margin: 1 1 0 1;
        background: $surface;
    }

    PacketTable {
        height: 50%;
        border: solid yellow;
        margin: 0 1 1 1;
        background: $surface;
    }
    """

    TITLE = "WiFi Security Dashboard v3.0 - Textual"

    # Keyboard bindings
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("p", "toggle_pause", "Pause"),
        ("h", "show_help", "Help"),
        ("?", "show_help", "Help"),
        ("r", "reset_charts", "Reset"),
        ("e", "toggle_educational", "Educational"),
    ]

    # Reactive state
    cpu_percent = reactive(0.0)
    paused = reactive(False)
    educational_mode = reactive(True)

    def __init__(self, mock_mode: bool = False):
        """
        Initialize dashboard.

        Args:
            mock_mode: If True, use mock data instead of real metrics
        """
        super().__init__()
        self.mock_mode = mock_mode
        self.system_plugin = None
        self.wifi_plugin = None
        self.network_plugin = None
        self.packet_analyzer_plugin = None

    def compose(self) -> ComposeResult:
        """Compose the dashboard layout."""
        yield Header(show_clock=True)

        with Horizontal():
            # Sidebar (left) - System metrics tiles
            with Container(id="sidebar"):
                yield CPUWidget(id="cpu-widget")
                yield RAMWidget(id="ram-widget")
                yield DiskWidget(id="disk-widget")
                yield WiFiWidget(id="wifi-widget")

            # Main area (right) - Charts and tables
            with Vertical(id="main"):
                yield NetworkChart(id="network-chart")
                yield PacketTable(id="packet-table")

        yield Footer()

    def on_mount(self) -> None:
        """Called when app is mounted. Setup plugins and timers."""
        # Initialize System Plugin
        system_config = PluginConfig(
            name="system",
            rate_ms=100,  # 10 FPS
            config={"mock_mode": self.mock_mode}
        )
        self.system_plugin = SystemPlugin(system_config)
        self.system_plugin.initialize()

        # Initialize WiFi Plugin
        wifi_config = PluginConfig(
            name="wifi",
            rate_ms=1000,  # 1 Hz
            config={"interface": "wlan0", "mock_mode": self.mock_mode}
        )
        self.wifi_plugin = WiFiPlugin(wifi_config)
        self.wifi_plugin.initialize()

        # Initialize Network Plugin
        network_config = PluginConfig(
            name="network",
            rate_ms=500,  # 2 Hz
            config={"interface": "wlan0", "mock_mode": self.mock_mode}
        )
        self.network_plugin = NetworkPlugin(network_config)
        self.network_plugin.initialize()

        # Initialize PacketAnalyzer Plugin
        packet_config = PluginConfig(
            name="packet_analyzer",
            rate_ms=2000,  # 0.5 Hz
            config={"interface": "wlan0", "mock_mode": self.mock_mode}
        )
        self.packet_analyzer_plugin = PacketAnalyzerPlugin(packet_config)
        self.packet_analyzer_plugin.initialize()

        # Setup interval timer (10 FPS = 100ms)
        self.set_interval(0.1, self.update_metrics)

        # Show startup message
        mode = "MOCK" if self.mock_mode else "REAL"
        self.notify(f"Dashboard started in {mode} mode", title="Welcome! 🎓")

    def update_metrics(self) -> None:
        """Update all metrics from plugins."""
        # Skip updates if paused
        if self.paused:
            return

        # Collect system data
        system_data = self.system_plugin.collect_data()

        # Update CPU widget
        cpu_widget = self.query_one("#cpu-widget", CPUWidget)
        cpu_widget.cpu_percent = system_data['cpu_percent']

        # Update RAM widget
        ram_widget = self.query_one("#ram-widget", RAMWidget)
        ram_widget.memory_percent = system_data['memory_percent']
        ram_widget.memory_used_mb = system_data['memory_used_mb']
        ram_widget.memory_total_mb = system_data['memory_total_mb']

        # Update Disk widget
        disk_widget = self.query_one("#disk-widget", DiskWidget)
        disk_widget.disk_percent = system_data['disk_percent']
        disk_widget.disk_used_gb = system_data['disk_used_gb']
        disk_widget.disk_total_gb = system_data['disk_total_gb']

        # Collect and update WiFi data
        wifi_data = self.wifi_plugin.collect_data()
        wifi_widget = self.query_one("#wifi-widget", WiFiWidget)
        wifi_widget.signal_strength_percent = wifi_data.get('signal_strength_percent', 0)
        wifi_widget.ssid = wifi_data.get('ssid', 'Not Connected')
        wifi_widget.signal_dbm = wifi_data.get('signal_strength_dbm', -100)

        # Collect and update Network data
        network_data = self.network_plugin.collect_data()
        network_chart = self.query_one("#network-chart", NetworkChart)
        network_chart.update_data({'network': network_data})

        # Collect and update Packet data
        packet_data = self.packet_analyzer_plugin.collect_data()
        packet_table = self.query_one("#packet-table", PacketTable)
        packet_table.update_data({'packet_analyzer': packet_data})

    def action_toggle_pause(self) -> None:
        """Toggle pause/resume updates."""
        self.paused = not self.paused
        status = "PAUSED" if self.paused else "RESUMED"
        color = "yellow" if self.paused else "green"
        self.notify(f"Updates {status}", title="⏸️ Pause" if self.paused else "▶️ Resume", severity="warning" if self.paused else "information")

    def action_show_help(self) -> None:
        """Show help overlay."""
        from src.screens.help_screen import HelpScreen
        self.push_screen(HelpScreen())

    def action_reset_charts(self) -> None:
        """Reset/clear all charts and tables."""
        # Clear NetworkChart history
        network_chart = self.query_one("#network-chart", NetworkChart)
        network_chart.rx_history.clear()
        network_chart.tx_history.clear()
        network_chart.rx_history.extend([0.0] * 60)
        network_chart.tx_history.extend([0.0] * 60)
        network_chart._refresh_plot()

        # Clear PacketTable
        packet_table = self.query_one("#packet-table", PacketTable)
        packet_table.clear_packets()

        self.notify("Charts and tables cleared", title="🔄 Reset", severity="information")

    def action_toggle_educational(self) -> None:
        """Toggle educational mode."""
        self.educational_mode = not self.educational_mode
        status = "ENABLED" if self.educational_mode else "DISABLED"
        self.notify(f"Educational mode {status}", title="🎓 Educational", severity="information")

    def action_quit(self) -> None:
        """Quit the application."""
        # Cleanup all plugins
        if self.system_plugin:
            self.system_plugin.cleanup()
        if self.wifi_plugin:
            self.wifi_plugin.cleanup()
        if self.network_plugin:
            self.network_plugin.cleanup()
        if self.packet_analyzer_plugin:
            self.packet_analyzer_plugin.cleanup()
        self.exit()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="WiFi Security Education Dashboard v3.0 - Textual",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python app_textual.py              # Run with real data
  python app_textual.py --mock       # Run with mock data (educational)
  python app_textual.py --help       # Show this help

Author: Juan-Dev - Soli Deo Gloria ✝️
        """
    )

    parser.add_argument(
        '--mock',
        '-m',
        action='store_true',
        help='Run in mock mode with simulated data (educational)'
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    # Create and run Textual app
    app = WiFiSecurityDashboard(mock_mode=args.mock)
    app.run()


if __name__ == "__main__":
    main()
