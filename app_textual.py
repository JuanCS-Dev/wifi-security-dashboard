#!/usr/bin/env python3
"""
WiFi Security Education Dashboard v3.0 - Textual Multi-Dashboard Version

Complete dashboard system with 5 screens:
- Consolidated Dashboard (overview of ALL systems)
- System Dashboard (CPU, RAM, Disk details)
- Network Dashboard (bandwidth charts + stats)
- WiFi Dashboard (signal + connection details)
- Packets Dashboard (packet table + protocol analysis)

Navigation: Press 0-4 to switch between dashboards, or Tab to cycle through them.

Author: Professor JuanCS-Dev - Soli Deo Gloria ✝️
Date: 2025-11-12
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, Any

from textual.app import App
from textual.reactive import reactive

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.plugins.system_plugin import SystemPlugin
from src.plugins.wifi_plugin import WiFiPlugin
from src.plugins.network_plugin import NetworkPlugin
from src.plugins.packet_analyzer_plugin import PacketAnalyzerPlugin
from src.plugins.network_topology_plugin import NetworkTopologyPlugin, MockNetworkTopologyPlugin
from src.plugins.base import PluginConfig

from src.screens import (
    LandingScreen,
    ConsolidatedDashboard,
    SystemDashboard,
    NetworkDashboard,
    WiFiDashboard,
    PacketsDashboard,
    HelpScreen,
    TutorialScreen,
)
from src.screens.topology_dashboard import TopologyDashboard


class WiFiSecurityDashboardApp(App):
    """
    WiFi Security Education Dashboard v3.0 - Multi-Screen Application

    Features:
    - 5 specialized dashboards (Consolidated, System, Network, WiFi, Packets)
    - Seamless navigation with keyboard shortcuts (0-4)
    - Real-time data updates (10 FPS)
    - Mock mode for safe educational demonstrations
    - Real mode for actual network monitoring

    Architecture:
    - Textual App (root) manages plugins and data collection
    - Screens (dashboards) handle visualization
    - Plugins provide data (System, WiFi, Network, PacketAnalyzer)
    - Event-driven updates via set_interval
    """

    # Load classic terminal theme
    CSS_PATH = "src/themes/terminal_native.tcss"
    
    CSS = """
    Screen {
        background: #000000;
    }
    """

    TITLE = "WiFi Security Dashboard v3.0 - Multi-Screen"

    # Global keyboard bindings (work on all screens)
    BINDINGS = [
        ("0", "switch_screen('consolidated')", "Overview"),
        ("1", "switch_screen('system')", "System"),
        ("2", "switch_screen('network')", "Network"),
        ("3", "switch_screen('wifi')", "WiFi"),
        ("4", "switch_screen('packets')", "Packets"),
        ("5", "switch_screen('topology')", "Topology"),
        ("escape", "back_to_menu", "Menu"),
        ("backspace", "back_to_menu", "Menu"),
        ("tab", "cycle_screen", "Next Screen"),
        ("m", "toggle_mode", "Toggle Mode"),
        ("h", "show_help", "Help"),
        ("?", "show_help", "Help"),
        ("p", "toggle_pause", "Pause"),
        ("q", "quit", "Quit"),
    ]

    # Reactive state
    paused = reactive(False)
    current_screen_index = reactive(0)

    def __init__(self, mock_mode: bool = False):
        """
        Initialize dashboard application.

        Args:
            mock_mode: If True, use mock data instead of real metrics
        """
        super().__init__()
        self.mock_mode = mock_mode

        # Plugins (initialized in on_mount)
        self.system_plugin = None
        self.wifi_plugin = None
        self.network_plugin = None
        self.packet_analyzer_plugin = None
        self.topology_plugin = None

        # Screen names for cycling
        self.screen_names = [
            "consolidated",
            "system",
            "network",
            "wifi",
            "packets",
            "topology",
        ]

    def on_mount(self) -> None:
        """Called when app is mounted. Setup plugins, screens, and timers."""
        # Initialize plugins
        self._initialize_plugins()

        # Install screens (but don't show them yet)
        mode = "mock" if self.mock_mode else "real"
        self.install_screen(LandingScreen(current_mode=mode), name="landing")
        self.install_screen(ConsolidatedDashboard(self.plugin_manager), name="consolidated")
        self.install_screen(SystemDashboard(), name="system")
        self.install_screen(NetworkDashboard(), name="network")
        self.install_screen(WiFiDashboard(), name="wifi")
        self.install_screen(PacketsDashboard(), name="packets")
        self.install_screen(TopologyDashboard(), name="topology")
        self.install_screen(HelpScreen(), name="help")
        self.install_screen(TutorialScreen(), name="tutorial")

        # Check if this is first run - show tutorial if needed
        if TutorialScreen.should_show_tutorial():
            self.push_screen("tutorial")
        
        # Start with landing page
        self.push_screen("landing")

        # Setup interval timer for data updates (10 FPS = 100ms)
        self.set_interval(0.1, self.update_all_metrics)

        # Show startup notification
        mode = "MOCK" if self.mock_mode else "REAL"
        self.notify(
            f"Dashboard started in {mode} mode\n"
            f"Press 0-4 to switch screens, Tab to cycle, h for help",
            title="🎓 WiFi Security Dashboard v3.0",
            timeout=5,
        )

    def _initialize_plugins(self) -> None:
        """Initialize all data collection plugins."""
        # System Plugin
        system_config = PluginConfig(
            name="system",
            rate_ms=100,  # 10 FPS
            config={"mock_mode": self.mock_mode}
        )
        self.system_plugin = SystemPlugin(system_config)
        self.system_plugin.initialize()

        # WiFi Plugin
        wifi_config = PluginConfig(
            name="wifi",
            rate_ms=1000,  # 1 Hz (WiFi data changes slowly)
            config={"interface": "wlan0", "mock_mode": self.mock_mode}
        )
        self.wifi_plugin = WiFiPlugin(wifi_config)
        self.wifi_plugin.initialize()

        # Network Plugin
        network_config = PluginConfig(
            name="network",
            rate_ms=500,  # 2 Hz
            config={"interface": "wlan0", "mock_mode": self.mock_mode}
        )
        self.network_plugin = NetworkPlugin(network_config)
        self.network_plugin.initialize()

        # PacketAnalyzer Plugin
        packet_config = PluginConfig(
            name="packet_analyzer",
            rate_ms=2000,  # 0.5 Hz (packet capture is slow)
            config={"interface": "wlan0", "mock_mode": self.mock_mode}
        )
        self.packet_analyzer_plugin = PacketAnalyzerPlugin(packet_config)
        self.packet_analyzer_plugin.initialize()
        
        # NetworkTopology Plugin
        topology_config = PluginConfig(
            name="topology",
            rate_ms=30000,  # Scan every 30 seconds
            config={"mock_mode": self.mock_mode}
        )
        if self.mock_mode:
            self.topology_plugin = MockNetworkTopologyPlugin(topology_config)
        else:
            self.topology_plugin = NetworkTopologyPlugin(topology_config)
        self.topology_plugin.initialize()
        
        # Create simple plugin manager for ConsolidatedDashboard
        class SimplePluginManager:
            def __init__(self, app):
                self.app = app
            def get_plugin_data(self, plugin_name):
                if plugin_name == 'system':
                    return self.app.system_plugin.collect_data()
                elif plugin_name == 'wifi':
                    return self.app.wifi_plugin.collect_data()
                elif plugin_name == 'network':
                    return self.app.network_plugin.collect_data()
                elif plugin_name == 'packet_analyzer':
                    return self.app.packet_analyzer_plugin.collect_data()
                return None
        
        self.plugin_manager = SimplePluginManager(self)

    def update_all_metrics(self) -> None:
        """
        Collect data from all plugins and update current screen.

        Called every 100ms (10 FPS) by set_interval timer.
        Only updates the currently visible screen for efficiency.
        """
        # Skip updates if paused
        if self.paused:
            return

        # Collect data from all plugins
        system_data = self.system_plugin.collect_data()
        wifi_data = self.wifi_plugin.collect_data()
        network_data = self.network_plugin.collect_data()
        packet_data = self.packet_analyzer_plugin.collect_data()

        # Update current screen based on which one is active
        current_screen = self.screen

        # Update appropriate screen
        if isinstance(current_screen, ConsolidatedDashboard):
            current_screen.update_metrics(
                system_data, wifi_data, network_data, packet_data
            )
        elif isinstance(current_screen, SystemDashboard):
            current_screen.update_metrics(system_data)
        elif isinstance(current_screen, NetworkDashboard):
            current_screen.update_metrics(network_data)
        elif isinstance(current_screen, WiFiDashboard):
            current_screen.update_metrics(wifi_data)
        elif isinstance(current_screen, PacketsDashboard):
            current_screen.update_metrics(packet_data)
        # HelpScreen doesn't need updates

    def action_switch_screen(self, screen_name: str) -> None:
        """
        Switch to a specific screen by name.

        Args:
            screen_name: Name of screen to switch to ("consolidated", "system", etc.)
        """
        if screen_name in self.screen_names:
            self.switch_screen(screen_name)
            self.current_screen_index = self.screen_names.index(screen_name)

            # Notify user of screen change
            screen_titles = {
                "consolidated": "📊 Consolidated Overview",
                "system": "💻 System Metrics",
                "network": "🌐 Network Analytics",
                "wifi": "📡 WiFi Details",
                "packets": "📦 Packet Analysis",
                "topology": "🗺️ Network Topology",
            }
            title = screen_titles.get(screen_name, screen_name.title())
            self.notify(f"Switched to: {title}", timeout=2)

    def action_cycle_screen(self) -> None:
        """Cycle to next screen (Tab key)."""
        self.current_screen_index = (self.current_screen_index + 1) % len(self.screen_names)
        next_screen = self.screen_names[self.current_screen_index]
        self.action_switch_screen(next_screen)

    def action_back_to_menu(self) -> None:
        """Go back to landing menu."""
        # Update landing screen with current mode
        mode = "mock" if self.mock_mode else "real"
        landing = self.get_screen("landing")
        if hasattr(landing, 'current_mode'):
            landing.current_mode = mode
            menu_widget = landing.query_one("#menu")
            if hasattr(menu_widget, 'current_mode'):
                menu_widget.current_mode = mode

        self.switch_screen("landing")
        self.notify("Back to main menu", timeout=1)

    def action_toggle_mode(self) -> None:
        """Toggle between mock and real mode."""
        self.mock_mode = not self.mock_mode
        new_mode = "mock" if self.mock_mode else "real"

        # Reinitialize plugins with new mode
        self._initialize_plugins()

        # Update landing screen
        try:
            landing = self.get_screen("landing")
            if hasattr(landing, 'current_mode'):
                landing.current_mode = new_mode
                menu_widget = landing.query_one("#menu")
                if hasattr(menu_widget, 'current_mode'):
                    menu_widget.current_mode = new_mode
        except:
            pass

        # Notify user
        mode_label = "MOCK (Educational)" if self.mock_mode else "REAL (Live Data)"
        self.notify(
            f"Switched to {mode_label}",
            title="🔄 Mode Changed",
            severity="information"
        )

    def action_show_help(self) -> None:
        """Show help screen overlay."""
        self.push_screen("help")

    def action_toggle_pause(self) -> None:
        """Toggle pause/resume updates."""
        self.paused = not self.paused
        status = "PAUSED" if self.paused else "RESUMED"
        severity = "warning" if self.paused else "information"
        icon = "⏸️ " if self.paused else "▶️ "
        self.notify(
            f"Updates {status}",
            title=f"{icon}{'Paused' if self.paused else 'Resumed'}",
            severity=severity,
        )

    def get_plugin_data(self, plugin_name: str) -> Dict[str, Any]:
        """
        Get data from a specific plugin.
        
        Args:
            plugin_name: Name of plugin (topology, system, wifi, etc.)
            
        Returns:
            Plugin data dictionary
        """
        if plugin_name == 'topology' and self.topology_plugin:
            return self.topology_plugin.get_data()
        elif plugin_name == 'system' and self.system_plugin:
            return self.system_plugin.collect_data()
        elif plugin_name == 'wifi' and self.wifi_plugin:
            return self.wifi_plugin.collect_data()
        elif plugin_name == 'network' and self.network_plugin:
            return self.network_plugin.collect_data()
        elif plugin_name == 'packet_analyzer' and self.packet_analyzer_plugin:
            return self.packet_analyzer_plugin.collect_data()
        return {}
    
    def action_quit(self) -> None:
        """Quit the application gracefully."""
        # Cleanup all plugins
        if self.system_plugin:
            self.system_plugin.cleanup()
        if self.wifi_plugin:
            self.wifi_plugin.cleanup()
        if self.network_plugin:
            self.network_plugin.cleanup()
        if self.packet_analyzer_plugin:
            self.packet_analyzer_plugin.cleanup()
        if self.topology_plugin:
            self.topology_plugin.stop()

        self.exit()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="WiFi Security Education Dashboard v3.0 - Multi-Screen Textual",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Dashboards:
  0 - Consolidated Overview (all metrics at once)
  1 - System Dashboard (CPU, RAM, Disk details)
  2 - Network Dashboard (bandwidth charts + stats)
  3 - WiFi Dashboard (signal + connection details)
  4 - Packets Dashboard (packet table + protocol analysis)

Navigation:
  0-4     Switch to specific dashboard
  Tab     Cycle through dashboards
  h or ?  Show help screen
  p       Pause/Resume updates
  q       Quit

Examples:
  python app_textual.py              # Run with real data
  python app_textual.py --mock       # Run with mock data (educational)

Author: Juan-Dev - Soli Deo Gloria ✝️
        """
    )

    parser.add_argument(
        '--mock',
        '-m',
        action='store_true',
        help='Run in mock mode with simulated data (educational, no root required)'
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    # Create and run Textual app
    app = WiFiSecurityDashboardApp(mock_mode=args.mock)
    app.run()


if __name__ == "__main__":
    main()
